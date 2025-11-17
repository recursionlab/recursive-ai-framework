"""
Synthesis Memory System - Persistent state for cross-conversation insights

Problem: AI can't hold 10 conversations in memory simultaneously
Solution: Build UP insights incrementally with persistent state

Architecture:
- insights table: compressed discoveries across conversations
- evidence table: which files support which insights
- updates table: how insights evolved as new data was processed
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Insight:
    """A compressed, persistent insight from conversation analysis"""
    id: Optional[int]
    topic: str  # e.g., "consciousness_architecture", "recursion_methodology"
    statement: str  # The actual compressed insight (1-3 sentences)
    confidence: float  # 0.0-1.0, how certain are we?
    evidence_count: int  # How many files support this
    created_at: str
    updated_at: str

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'topic': self.topic,
            'statement': self.statement,
            'confidence': self.confidence,
            'evidence_count': self.evidence_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class SynthesisMemory:
    """Persistent memory system for building up insights across conversations"""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.conn = None
        self._initialize_db()

    def _initialize_db(self):
        """Create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Main insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                statement TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                evidence_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        # Evidence linking insights to source files
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                relevant_quote TEXT,
                added_at TEXT NOT NULL,
                FOREIGN KEY (insight_id) REFERENCES insights(id)
            )
        ''')

        # Update history - track how insights evolved
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_id INTEGER NOT NULL,
                old_statement TEXT,
                new_statement TEXT,
                reason TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (insight_id) REFERENCES insights(id)
            )
        ''')

        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_topic ON insights(topic)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_confidence ON insights(confidence)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_evidence_insight ON evidence(insight_id)')

        self.conn.commit()

    def add_insight(self, topic: str, statement: str, confidence: float = 0.5) -> int:
        """Add a new insight to memory"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO insights (topic, statement, confidence, evidence_count, created_at, updated_at)
            VALUES (?, ?, ?, 0, ?, ?)
        ''', (topic, statement, confidence, now, now))

        self.conn.commit()
        return cursor.lastrowid

    def add_evidence(self, insight_id: int, file_path: str, quote: Optional[str] = None):
        """Link a file as evidence for an insight"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO evidence (insight_id, file_path, relevant_quote, added_at)
            VALUES (?, ?, ?, ?)
        ''', (insight_id, file_path, quote, now))

        # Update evidence count
        cursor.execute('''
            UPDATE insights
            SET evidence_count = (
                SELECT COUNT(*) FROM evidence WHERE insight_id = ?
            ),
            updated_at = ?
            WHERE id = ?
        ''', (insight_id, now, insight_id))

        self.conn.commit()

    def update_insight(self, insight_id: int, new_statement: str, reason: str, new_confidence: Optional[float] = None):
        """Update an insight when new evidence changes understanding"""
        cursor = self.conn.cursor()

        # Get old statement
        cursor.execute('SELECT statement FROM insights WHERE id = ?', (insight_id,))
        old_statement = cursor.fetchone()['statement']

        # Record the update history
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO updates (insight_id, old_statement, new_statement, reason, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (insight_id, old_statement, new_statement, reason, now))

        # Update the insight
        if new_confidence is not None:
            cursor.execute('''
                UPDATE insights
                SET statement = ?, confidence = ?, updated_at = ?
                WHERE id = ?
            ''', (new_statement, new_confidence, now, insight_id))
        else:
            cursor.execute('''
                UPDATE insights
                SET statement = ?, updated_at = ?
                WHERE id = ?
            ''', (new_statement, now, insight_id))

        self.conn.commit()

    def get_insights_by_topic(self, topic: str) -> List[Insight]:
        """Retrieve all insights for a topic"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM insights
            WHERE topic = ?
            ORDER BY confidence DESC, evidence_count DESC
        ''', (topic,))

        return [self._row_to_insight(row) for row in cursor.fetchall()]

    def get_all_insights(self, min_confidence: float = 0.0) -> List[Insight]:
        """Get all insights above confidence threshold"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM insights
            WHERE confidence >= ?
            ORDER BY confidence DESC, evidence_count DESC
        ''', (min_confidence,))

        return [self._row_to_insight(row) for row in cursor.fetchall()]

    def get_insight_with_evidence(self, insight_id: int) -> Dict:
        """Get an insight with all its supporting evidence"""
        cursor = self.conn.cursor()

        # Get insight
        cursor.execute('SELECT * FROM insights WHERE id = ?', (insight_id,))
        insight_row = cursor.fetchone()
        if not insight_row:
            return None

        insight = self._row_to_insight(insight_row)

        # Get evidence
        cursor.execute('''
            SELECT file_path, relevant_quote
            FROM evidence
            WHERE insight_id = ?
        ''', (insight_id,))

        evidence = [dict(row) for row in cursor.fetchall()]

        # Get update history
        cursor.execute('''
            SELECT old_statement, new_statement, reason, updated_at
            FROM updates
            WHERE insight_id = ?
            ORDER BY updated_at
        ''', (insight_id,))

        history = [dict(row) for row in cursor.fetchall()]

        return {
            'insight': insight.to_dict(),
            'evidence': evidence,
            'history': history
        }

    def search_insights(self, query: str) -> List[Insight]:
        """Full-text search across insights"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM insights
            WHERE statement LIKE ?
            ORDER BY confidence DESC
        ''', (f'%{query}%',))

        return [self._row_to_insight(row) for row in cursor.fetchall()]

    def export_synthesis(self, output_path: Path, min_confidence: float = 0.5):
        """Export current synthesis state as markdown"""
        insights = self.get_all_insights(min_confidence=min_confidence)

        # Group by topic
        by_topic = {}
        for insight in insights:
            if insight.topic not in by_topic:
                by_topic[insight.topic] = []
            by_topic[insight.topic].append(insight)

        # Generate markdown
        lines = [
            "# Synthesis Memory Snapshot",
            f"Generated: {datetime.now().isoformat()}",
            f"Total Insights: {len(insights)}",
            f"Minimum Confidence: {min_confidence}",
            "",
            "---",
            ""
        ]

        for topic, topic_insights in sorted(by_topic.items()):
            lines.append(f"## {topic.replace('_', ' ').title()}")
            lines.append("")

            for insight in topic_insights:
                lines.append(f"**[{insight.confidence:.2f}]** {insight.statement}")
                lines.append(f"*Evidence: {insight.evidence_count} files*")
                lines.append("")

        Path(output_path).write_text('\n'.join(lines))

    def _row_to_insight(self, row) -> Insight:
        """Convert DB row to Insight object"""
        return Insight(
            id=row['id'],
            topic=row['topic'],
            statement=row['statement'],
            confidence=row['confidence'],
            evidence_count=row['evidence_count'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    # Example usage
    memory = SynthesisMemory(Path('/tmp/synthesis_memory.db'))

    # Add an insight from first conversation
    insight_id = memory.add_insight(
        topic='recursion_methodology',
        statement='User achieves φ-depth by hitting singularity first, then reverse-engineering into concrete forms.',
        confidence=0.8
    )

    memory.add_evidence(
        insight_id,
        '/tmp/recursion-agi/claude/2025/07/Consciousness as Recursive Self-Reference.md',
        quote='φ90 peak in July 2025, before other implementations'
    )

    # Later, after reading more conversations, update it
    memory.update_insight(
        insight_id,
        'User works backwards: φ90 abstract insight → φ32 mathematical proof → φ28 implementation. Higher φ = more compressed.',
        reason='Confirmed by temporal analysis across 10 conversations'
    )

    # Export current understanding
    memory.export_synthesis(Path('/tmp/current_synthesis.md'))

    print("Synthesis memory system initialized")
    print(f"Insights: {len(memory.get_all_insights())}")

    memory.close()
