#!/usr/bin/env python3
"""
Conversation Consumption CLI - The BRRR Machine

Takes ANY input (file, directory, stdin) and consumes it.
Doesn't care if you have 6 or 6 million conversations.
"""

import sys
import argparse
from pathlib import Path
from typing import Iterator, Tuple
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.universal_parser import UniversalParser, Turn


class ConversationConsumer:
    """
    Scale-agnostic conversation consumption engine

    Philosophy: It doesn't matter what you feed it or how much.
    It just keeps consuming.
    """

    def __init__(self, verbose: bool = False):
        self.parser = UniversalParser()
        self.verbose = verbose
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'total_turns': 0,
            'formats_seen': set()
        }

    def consume_stdin(self) -> Iterator[Tuple[str, Turn]]:
        """
        Consume conversation from stdin (paste bulk text, it goes BRRR)

        Yields (source_id, turn) pairs
        """
        import tempfile

        # Read from stdin and parse
        print("📝 Reading from stdin... (Ctrl+D to finish)")

        try:
            content = sys.stdin.read()

            # Write to temp file for parsing
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(content)
                temp_path = Path(f.name)

            # Parse the temp file
            source_id = "stdin"
            for turn in self.parser.parse_file(temp_path):
                self.stats['total_turns'] += 1
                yield (source_id, turn)

            # Cleanup
            temp_path.unlink()
            self.stats['files_processed'] += 1

        except Exception as e:
            print(f"❌ Error consuming stdin: {e}")
            self.stats['files_failed'] += 1

    def consume_file(self, file_path: Path) -> Iterator[Tuple[str, Turn]]:
        """
        Consume single conversation file

        Yields (source_id, turn) pairs
        """
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            self.stats['files_failed'] += 1
            return

        if not file_path.is_file():
            print(f"⚠️  Skipping non-file: {file_path}")
            return

        try:
            # Detect format
            format_type = self.parser.detect_format(file_path)
            self.stats['formats_seen'].add(format_type.value)

            # Parse and yield turns
            source_id = str(file_path)
            turn_count = 0

            for turn in self.parser.parse_file(file_path):
                self.stats['total_turns'] += 1
                turn_count += 1
                yield (source_id, turn)

            self.stats['files_processed'] += 1

            if self.verbose:
                print(f"✓ {file_path.name}: {turn_count} turns ({format_type.value})")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            self.stats['files_failed'] += 1

    def consume_directory(self, dir_path: Path, recursive: bool = True) -> Iterator[Tuple[str, Turn]]:
        """
        Consume entire directory of conversations

        Walks directory, auto-detects formats, yields turns.
        Works with 6 or 6 million files - streaming all the way.

        Yields (source_id, turn) pairs
        """
        if not dir_path.exists():
            print(f"❌ Directory not found: {dir_path}")
            return

        if not dir_path.is_dir():
            print(f"⚠️  Not a directory: {dir_path}")
            return

        # File extensions we'll try to parse
        extensions = {'.json', '.md', '.txt', '.markdown', '.log'}

        # Walk directory (recursively or not)
        pattern = '**/*' if recursive else '*'
        files = [
            f for f in dir_path.glob(pattern)
            if f.is_file() and (f.suffix.lower() in extensions or f.suffix == '')
        ]

        total_files = len(files)
        print(f"📂 Found {total_files} potential conversation files in {dir_path}")
        print(f"🔄 Processing... (streaming, no memory limits)")

        # Process each file (streaming)
        for i, file_path in enumerate(files, 1):
            if not self.verbose and i % 100 == 0:
                # Progress indicator every 100 files
                print(f"   ... processed {i}/{total_files} files ({self.stats['total_turns']} turns so far)")

            # Yield all turns from this file
            yield from self.consume_file(file_path)

        # Final stats
        print(f"\n✓ Directory processing complete:")
        print(f"  • Files processed: {self.stats['files_processed']}")
        print(f"  • Files failed: {self.stats['files_failed']}")
        print(f"  • Total turns: {self.stats['total_turns']}")
        print(f"  • Formats seen: {', '.join(self.stats['formats_seen'])}")

    def consume(self, source: str) -> Iterator[Tuple[str, Turn]]:
        """
        Universal consume method

        Args:
            source: File path, directory path, or "-" for stdin

        Yields (source_id, turn) pairs
        """
        if source == "-":
            # Read from stdin
            yield from self.consume_stdin()
        else:
            path = Path(source)
            if path.is_file():
                yield from self.consume_file(path)
            elif path.is_dir():
                yield from self.consume_directory(path)
            else:
                print(f"❌ Invalid source: {source}")


def main():
    parser = argparse.ArgumentParser(
        description="Conversation Archaeology Consumer - The BRRR Machine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file (any format)
  %(prog)s conversation.json

  # Entire directory (recursive)
  %(prog)s ~/my_conversations/

  # From stdin (paste bulk text)
  cat bulk_text.md | %(prog)s -

  # Non-recursive directory
  %(prog)s ~/exports/ --no-recursive

Philosophy:
  Doesn't matter what you feed it.
  Doesn't matter how much.
  It just consumes.
        """
    )

    parser.add_argument(
        'source',
        help='Conversation source (file, directory, or "-" for stdin)'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        default=True,
        help='Recursively process directories (default: True)'
    )

    parser.add_argument(
        '--no-recursive',
        action='store_false',
        dest='recursive',
        help='Do not recursively process directories'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output (show each file processed)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse conversations but don\'t store (testing)'
    )

    args = parser.parse_args()

    # Create consumer
    consumer = ConversationConsumer(verbose=args.verbose)

    # Consume conversations
    print("🔥 BRRR Machine starting...")
    print(f"📖 Source: {args.source}")
    print()

    try:
        turn_count = 0
        for source_id, turn in consumer.consume(args.source):
            turn_count += 1

            # For now, just count (later we'll feed to alchemy pipeline)
            if args.dry_run and args.verbose:
                print(f"  Turn {turn_count} ({turn.role}): {len(turn.content)} chars")

        print(f"\n✅ Processing complete!")
        print(f"   Total turns consumed: {consumer.stats['total_turns']}")
        print(f"   Files processed: {consumer.stats['files_processed']}")
        if consumer.stats['files_failed'] > 0:
            print(f"   ⚠️  Files failed: {consumer.stats['files_failed']}")

    except KeyboardInterrupt:
        print(f"\n\n⏸️  Interrupted by user")
        print(f"   Turns processed before interrupt: {consumer.stats['total_turns']}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
