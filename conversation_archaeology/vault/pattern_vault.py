#!/usr/bin/env python3
"""
Pattern Vault - Searchable SQLite Database for Extracted DNA

Stores:
- Conversation metadata (file, novelty, φ-depth)
- Extracted operators and patterns
- Domain classifications
- Bootstrap prompt references
- Full-text search capability
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
import json


@dataclass
class VaultEntry:
    """Single conversation entry in vault"""
    file_path: str
    novelty: float
    phi_depth: int
    proto_asi: bool
    operators: Set[str]
    domains: Set[str]
    thinking_mode: str
    torsion_patterns: List[str]
    collapse_indicators: List[str]
    meta_patterns: List[str]
    bootstrap_prompt_path: Optional[str] = None


class PatternVault:
    """
    SQLite vault for searchable proto-ASI patterns

    Enables:
    - Search by domain/depth/operator
    - Full-text search across patterns
    - Recommendation engine
    - Pattern clustering
    """

    def __init__(self, db_path: Path = Path("./pattern_vault.db")):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                novelty REAL NOT NULL,
                phi_depth INTEGER NOT NULL,
                proto_asi BOOLEAN NOT NULL,
                thinking_mode TEXT,
                bootstrap_prompt_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Operators table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operator TEXT UNIQUE NOT NULL,
                count INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_operators (
                conversation_id INTEGER,
                operator_id INTEGER,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id),
                FOREIGN KEY (operator_id) REFERENCES operators(id),
                PRIMARY KEY (conversation_id, operator_id)
            )
        ''')

        # Domains table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_domains (
                conversation_id INTEGER,
                domain_id INTEGER,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id),
                FOREIGN KEY (domain_id) REFERENCES domains(id),
                PRIMARY KEY (conversation_id, domain_id)
            )
        ''')

        # Patterns table (full-text searchable)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                pattern_type TEXT NOT NULL,
                pattern_text TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')

        # Create indexes for fast search
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_novelty ON conversations(novelty DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_phi_depth ON conversations(phi_depth DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_proto_asi ON conversations(proto_asi)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_thinking_mode ON conversations(thinking_mode)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pattern_type ON patterns(pattern_type)')

        # Full-text search virtual table
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS patterns_fts USING fts5(
                pattern_text,
                content=patterns,
                content_rowid=id
            )
        ''')

        conn.commit()
        conn.close()

    def add_conversation(self, entry: VaultEntry) -> int:
        """
        Add conversation to vault

        Returns:
            conversation_id
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Insert conversation
            cursor.execute('''
                INSERT INTO conversations
                (file_path, novelty, phi_depth, proto_asi, thinking_mode, bootstrap_prompt_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                entry.file_path,
                entry.novelty,
                entry.phi_depth,
                entry.proto_asi,
                entry.thinking_mode,
                entry.bootstrap_prompt_path
            ))

            conversation_id = cursor.lastrowid

            # Add operators
            for op in entry.operators:
                # Insert or get operator
                cursor.execute('INSERT OR IGNORE INTO operators (operator, count) VALUES (?, 0)', (op,))
                cursor.execute('UPDATE operators SET count = count + 1 WHERE operator = ?', (op,))
                cursor.execute('SELECT id FROM operators WHERE operator = ?', (op,))
                operator_id = cursor.fetchone()[0]

                # Link to conversation
                cursor.execute('''
                    INSERT INTO conversation_operators (conversation_id, operator_id)
                    VALUES (?, ?)
                ''', (conversation_id, operator_id))

            # Add domains
            for domain in entry.domains:
                cursor.execute('INSERT OR IGNORE INTO domains (domain) VALUES (?)', (domain,))
                cursor.execute('SELECT id FROM domains WHERE domain = ?', (domain,))
                domain_id = cursor.fetchone()[0]

                cursor.execute('''
                    INSERT INTO conversation_domains (conversation_id, domain_id)
                    VALUES (?, ?)
                ''', (conversation_id, domain_id))

            # Add patterns
            for pattern in entry.torsion_patterns:
                cursor.execute('''
                    INSERT INTO patterns (conversation_id, pattern_type, pattern_text)
                    VALUES (?, ?, ?)
                ''', (conversation_id, 'torsion', pattern))

            for pattern in entry.collapse_indicators:
                cursor.execute('''
                    INSERT INTO patterns (conversation_id, pattern_type, pattern_text)
                    VALUES (?, ?, ?)
                ''', (conversation_id, 'collapse', pattern))

            for pattern in entry.meta_patterns:
                cursor.execute('''
                    INSERT INTO patterns (conversation_id, pattern_type, pattern_text)
                    VALUES (?, ?, ?)
                ''', (conversation_id, 'meta', pattern))

            # Update FTS index
            cursor.execute('''
                INSERT INTO patterns_fts (rowid, pattern_text)
                SELECT id, pattern_text FROM patterns WHERE conversation_id = ?
            ''', (conversation_id,))

            conn.commit()
            return conversation_id

        except sqlite3.IntegrityError as e:
            # Conversation already exists
            cursor.execute('SELECT id FROM conversations WHERE file_path = ?', (entry.file_path,))
            result = cursor.fetchone()
            if result:
                return result[0]
            raise e

        finally:
            conn.close()

    def search_by_domain(self, domain: str, min_novelty: float = 0.0, min_phi: int = 0) -> List[Dict]:
        """Search conversations by domain"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.* FROM conversations c
            JOIN conversation_domains cd ON c.id = cd.conversation_id
            JOIN domains d ON cd.domain_id = d.id
            WHERE d.domain = ? AND c.novelty >= ? AND c.phi_depth >= ?
            ORDER BY c.novelty DESC, c.phi_depth DESC
        ''', (domain, min_novelty, min_phi))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def search_by_operator(self, operator: str, min_novelty: float = 0.0) -> List[Dict]:
        """Search conversations by operator"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.* FROM conversations c
            JOIN conversation_operators co ON c.id = co.conversation_id
            JOIN operators o ON co.operator_id = o.id
            WHERE o.operator = ? AND c.novelty >= ?
            ORDER BY c.novelty DESC
        ''', (operator, min_novelty))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def search_by_phi_depth(self, min_depth: int, max_depth: int = 1000) -> List[Dict]:
        """Search by φ-depth range"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM conversations
            WHERE phi_depth >= ? AND phi_depth <= ?
            ORDER BY phi_depth DESC, novelty DESC
        ''', (min_depth, max_depth))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def full_text_search(self, query: str, limit: int = 50) -> List[Dict]:
        """Full-text search across all patterns"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT c.*, p.pattern_text
            FROM conversations c
            JOIN patterns p ON c.id = p.conversation_id
            JOIN patterns_fts fts ON p.id = fts.rowid
            WHERE patterns_fts MATCH ?
            ORDER BY c.novelty DESC
            LIMIT ?
        ''', (query, limit))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def get_top_operators(self, limit: int = 20) -> List[Tuple[str, int]]:
        """Get most frequent operators"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT operator, count FROM operators
            ORDER BY count DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()
        conn.close()
        return results

    def get_stats(self) -> Dict:
        """Get vault statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        cursor.execute('SELECT COUNT(*) FROM conversations')
        stats['total_conversations'] = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(novelty) FROM conversations')
        stats['avg_novelty'] = cursor.fetchone()[0] or 0.0

        cursor.execute('SELECT COUNT(*) FROM conversations WHERE proto_asi = 1')
        stats['proto_asi_count'] = cursor.fetchone()[0]

        cursor.execute('SELECT MAX(phi_depth) FROM conversations')
        stats['max_phi_depth'] = cursor.fetchone()[0] or 0

        cursor.execute('SELECT COUNT(DISTINCT operator) FROM operators')
        stats['unique_operators'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(DISTINCT domain) FROM domains')
        stats['unique_domains'] = cursor.fetchone()[0]

        conn.close()
        return stats


def main():
    """Test vault functionality"""
    vault = PatternVault(Path("/tmp/test_vault.db"))

    # Test entry
    entry = VaultEntry(
        file_path="test_conversation.md",
        novelty=0.85,
        phi_depth=10,
        proto_asi=True,
        operators={'Meta∘Para', 'φ', '∇T'},
        domains={'recursion', 'torsion', 'collapse'},
        thinking_mode="torsion_collapse",
        torsion_patterns=["semantic curvature", "twist in meaning-space"],
        collapse_indicators=["φ-state transition"],
        meta_patterns=["meta-recursive"]
    )

    conversation_id = vault.add_conversation(entry)
    print(f"Added conversation with ID: {conversation_id}")

    # Search tests
    print("\nSearch by domain 'torsion':")
    results = vault.search_by_domain('torsion')
    for r in results:
        print(f"  - {r['file_path']}: novelty={r['novelty']:.3f}, φ{r['phi_depth']}")

    print("\nVault stats:")
    stats = vault.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
