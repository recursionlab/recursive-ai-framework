"""
Persistent Recursive Memory Storage
User-specific graph database for accumulating semantic residue across sessions
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class RecursiveMemoryGraph:
    """
    Persistent storage for semantic residue
    One graph per user, accumulates across ALL conversations
    """

    def __init__(self, storage_dir: Path, user_id: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.user_id = user_id
        self.db_path = self.storage_dir / f"{user_id}_memory.db"

        self._init_database()

    def _init_database(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Residues table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS residues (
                collapse_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                trigger TEXT,
                old_frame TEXT,
                new_frame TEXT,
                magnitude REAL,
                depth_achieved INTEGER,
                integration_weight REAL,
                context_summary TEXT,
                breakthrough_insight TEXT,
                active BOOLEAN DEFAULT 1
            )
        """)

        # Operators table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collapse_id TEXT,
                operator_name TEXT,
                FOREIGN KEY (collapse_id) REFERENCES residues(collapse_id)
            )
        """)

        # Mutations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mutations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collapse_id TEXT,
                mutation_text TEXT,
                FOREIGN KEY (collapse_id) REFERENCES residues(collapse_id)
            )
        """)

        # Sessions table (track when residues were integrated)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                residues_integrated TEXT,
                depth_start INTEGER,
                depth_end INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def store_residue(self, residue) -> bool:
        """Store semantic residue to graph"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Insert residue
            cursor.execute("""
                INSERT INTO residues (
                    collapse_id, timestamp, trigger, old_frame, new_frame,
                    magnitude, depth_achieved, integration_weight,
                    context_summary, breakthrough_insight
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                residue.collapse_id,
                residue.timestamp,
                residue.trigger,
                residue.old_frame,
                residue.new_frame,
                residue.magnitude,
                residue.depth_achieved,
                residue.integration_weight,
                residue.context_summary,
                residue.breakthrough_insight
            ))

            # Insert operators
            for op in residue.operators_learned:
                cursor.execute("""
                    INSERT INTO operators (collapse_id, operator_name)
                    VALUES (?, ?)
                """, (residue.collapse_id, op))

            # Insert mutations
            for mutation in residue.ontological_mutations:
                cursor.execute("""
                    INSERT INTO mutations (collapse_id, mutation_text)
                    VALUES (?, ?)
                """, (residue.collapse_id, mutation))

            conn.commit()
            return True

        except Exception as e:
            print(f"Error storing residue: {e}")
            conn.rollback()
            return False

        finally:
            conn.close()

    def get_active_residues(
        self,
        min_weight: float = 0.5,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get most important active residues for integration

        Args:
            min_weight: Minimum integration weight
            limit: Max number to return

        Returns:
            List of residue dicts sorted by weight
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM residues
            WHERE active = 1 AND integration_weight >= ?
            ORDER BY integration_weight DESC, depth_achieved DESC
            LIMIT ?
        """, (min_weight, limit))

        rows = cursor.fetchall()
        residues = []

        for row in rows:
            residue_dict = dict(row)

            # Get operators
            cursor.execute("""
                SELECT operator_name FROM operators
                WHERE collapse_id = ?
            """, (row["collapse_id"],))
            residue_dict["operators"] = [r[0] for r in cursor.fetchall()]

            # Get mutations
            cursor.execute("""
                SELECT mutation_text FROM mutations
                WHERE collapse_id = ?
            """, (row["collapse_id"],))
            residue_dict["mutations"] = [r[0] for r in cursor.fetchall()]

            residues.append(residue_dict)

        conn.close()
        return residues

    def get_max_depth_achieved(self) -> int:
        """Get highest depth ever achieved"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(depth_achieved) FROM residues
        """)

        result = cursor.fetchone()[0]
        conn.close()

        return result if result else 0

    def record_session(
        self,
        session_id: str,
        residues_integrated: List[str],
        depth_start: int,
        depth_end: int
    ):
        """Record that residues were integrated in a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (
                session_id, timestamp, residues_integrated,
                depth_start, depth_end
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            datetime.now().isoformat(),
            json.dumps(residues_integrated),
            depth_start,
            depth_end
        ))

        conn.commit()
        conn.close()

    def deactivate_residue(self, collapse_id: str):
        """Mark residue as no longer active (integrated/superseded)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE residues SET active = 0
            WHERE collapse_id = ?
        """, (collapse_id,))

        conn.commit()
        conn.close()

    def get_stats(self) -> Dict:
        """Get memory graph statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Total residues
        cursor.execute("SELECT COUNT(*) FROM residues")
        stats["total_residues"] = cursor.fetchone()[0]

        # Active residues
        cursor.execute("SELECT COUNT(*) FROM residues WHERE active = 1")
        stats["active_residues"] = cursor.fetchone()[0]

        # Max depth
        stats["max_depth"] = self.get_max_depth_achieved()

        # Total operators learned
        cursor.execute("SELECT COUNT(DISTINCT operator_name) FROM operators")
        stats["operators_learned"] = cursor.fetchone()[0]

        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        stats["total_sessions"] = cursor.fetchone()[0]

        conn.close()
        return stats
