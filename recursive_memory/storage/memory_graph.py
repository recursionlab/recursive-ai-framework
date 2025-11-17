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
        # Validate inputs
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be non-empty string")

        # Sanitize user_id for filesystem safety
        safe_user_id = "".join(c for c in user_id if c.isalnum() or c in "._-")
        if not safe_user_id:
            raise ValueError(f"user_id '{user_id}' contains no valid characters")

        self.storage_dir = Path(storage_dir)
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise RuntimeError(f"Cannot create storage directory {storage_dir}: {e}")

        self.user_id = safe_user_id
        self.db_path = self.storage_dir / f"{safe_user_id}_memory.db"

        # Check if database exists and is valid
        if self.db_path.exists():
            self._verify_database_integrity()

        self._init_database()

    def _verify_database_integrity(self):
        """Verify database is not corrupted"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()

            if result[0] != "ok":
                # Database corrupted - create backup and raise error
                backup_path = self.db_path.with_suffix(".db.corrupted.backup")
                import shutil
                shutil.copy2(self.db_path, backup_path)
                raise RuntimeError(
                    f"Database corrupted. Backup saved to {backup_path}. "
                    f"Please restore from backup or delete to start fresh."
                )
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Database integrity check failed: {e}")

    def _init_database(self):
        """Initialize SQLite database with schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            # Enable foreign keys for referential integrity
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot connect to database {self.db_path}: {e}")

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

    def _create_backup(self):
        """Create backup of database before write operations"""
        if not self.db_path.exists():
            return

        try:
            import shutil
            from datetime import datetime

            # Keep only last 5 backups to save space
            backup_dir = self.storage_dir / "backups"
            backup_dir.mkdir(exist_ok=True)

            # Create timestamped backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"{self.user_id}_memory_{timestamp}.db"

            shutil.copy2(self.db_path, backup_path)

            # Clean old backups (keep last 5)
            backups = sorted(backup_dir.glob(f"{self.user_id}_memory_*.db"))
            if len(backups) > 5:
                for old_backup in backups[:-5]:
                    old_backup.unlink()

        except Exception as e:
            # Don't fail operation if backup fails, just warn
            print(f"⚠️  Warning: Could not create backup: {e}")

    def store_residue(self, residue) -> bool:
        """Store semantic residue to graph"""

        # Validate residue object
        if residue is None:
            print("❌ Error: Cannot store None residue")
            return False

        required_attrs = [
            'collapse_id', 'timestamp', 'trigger', 'old_frame', 'new_frame',
            'magnitude', 'depth_achieved', 'integration_weight',
            'context_summary', 'breakthrough_insight', 'operators_learned',
            'ontological_mutations'
        ]

        for attr in required_attrs:
            if not hasattr(residue, attr):
                print(f"❌ Error: Residue missing required attribute '{attr}'")
                return False

        # Create backup before write operation
        self._create_backup()

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Check for duplicate collapse_id
            cursor.execute(
                "SELECT COUNT(*) FROM residues WHERE collapse_id = ?",
                (residue.collapse_id,)
            )
            if cursor.fetchone()[0] > 0:
                print(f"⚠️  Warning: Residue {residue.collapse_id} already exists, skipping")
                return False

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
                str(residue.trigger)[:500],  # Limit length
                str(residue.old_frame)[:500],
                str(residue.new_frame)[:500],
                float(residue.magnitude),
                int(residue.depth_achieved),
                float(residue.integration_weight),
                str(residue.context_summary)[:2000],
                str(residue.breakthrough_insight)[:1000]
            ))

            # Insert operators
            for op in residue.operators_learned:
                if op and isinstance(op, str):
                    cursor.execute("""
                        INSERT INTO operators (collapse_id, operator_name)
                        VALUES (?, ?)
                    """, (residue.collapse_id, op[:100]))

            # Insert mutations
            for mutation in residue.ontological_mutations:
                if mutation and isinstance(mutation, str):
                    cursor.execute("""
                        INSERT INTO mutations (collapse_id, mutation_text)
                        VALUES (?, ?)
                    """, (residue.collapse_id, mutation[:500]))

            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            print(f"❌ Database integrity error storing residue: {e}")
            if conn:
                conn.rollback()
            return False

        except sqlite3.Error as e:
            print(f"❌ Database error storing residue: {e}")
            if conn:
                conn.rollback()
            return False

        except (ValueError, TypeError) as e:
            print(f"❌ Data validation error: {e}")
            if conn:
                conn.rollback()
            return False

        except Exception as e:
            print(f"❌ Unexpected error storing residue: {e}")
            if conn:
                conn.rollback()
            return False

        finally:
            if conn:
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
        # Validate inputs
        try:
            min_weight = float(min_weight)
            limit = int(limit)
        except (ValueError, TypeError):
            print("❌ Error: Invalid parameters for get_active_residues")
            return []

        if limit <= 0:
            return []

        conn = None
        try:
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
                try:
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

                except Exception as e:
                    print(f"⚠️  Warning: Error loading residue {row.get('collapse_id', 'unknown')}: {e}")
                    continue

            return residues

        except sqlite3.Error as e:
            print(f"❌ Database error reading residues: {e}")
            return []

        except Exception as e:
            print(f"❌ Unexpected error reading residues: {e}")
            return []

        finally:
            if conn:
                conn.close()

    def get_max_depth_achieved(self) -> int:
        """Get highest depth ever achieved"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT MAX(depth_achieved) FROM residues
            """)

            result = cursor.fetchone()
            if result and result[0] is not None:
                return int(result[0])
            return 0

        except sqlite3.Error as e:
            print(f"❌ Database error getting max depth: {e}")
            return 0

        except Exception as e:
            print(f"❌ Unexpected error getting max depth: {e}")
            return 0

        finally:
            if conn:
                conn.close()

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
