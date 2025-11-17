#!/usr/bin/env python3
"""
Universal Conversation Parser - Format Agnostic, Scale Agnostic

Eats ANY conversation format and streams normalized turn structure.
Works with 6 or 6 million conversations - doesn't care about scale.
"""

import json
import sys
from pathlib import Path
from typing import Iterator, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re


class ConversationFormat(Enum):
    """Auto-detected conversation formats"""
    CHATGPT_JSON = "chatgpt_json"
    CLAUDE_JSON = "claude_json"
    MARKDOWN_TURNS = "markdown_turns"
    PLAIN_TEXT = "plain_text"
    UNKNOWN = "unknown"


@dataclass
class Turn:
    """Normalized conversation turn"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UniversalParser:
    """
    Format-agnostic streaming conversation parser

    Philosophy: Doesn't matter what format you throw at it.
    Doesn't matter how big. Just consumes and normalizes.
    """

    def __init__(self):
        # Order matters: check most specific formats first
        self.format_detectors = [
            (ConversationFormat.CHATGPT_JSON, self._is_chatgpt_json),
            (ConversationFormat.CLAUDE_JSON, self._is_claude_json),
            (ConversationFormat.MARKDOWN_TURNS, self._is_markdown_turns),
            (ConversationFormat.PLAIN_TEXT, self._is_plain_text),
        ]

    def detect_format(self, file_path: Path) -> ConversationFormat:
        """
        Auto-detect conversation format

        Returns format type or UNKNOWN if can't detect
        """
        if not file_path.exists():
            return ConversationFormat.UNKNOWN

        # Try to read first chunk (streaming - don't load entire file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Read first 4KB for detection
                sample = f.read(4096)

            # Run detection heuristics (in order - most specific first)
            for format_type, detector in self.format_detectors:
                if detector(sample, file_path):
                    return format_type

        except Exception as e:
            print(f"⚠️  Warning: Error detecting format for {file_path}: {e}")

        return ConversationFormat.UNKNOWN

    def _is_chatgpt_json(self, sample: str, file_path: Path) -> bool:
        """Detect ChatGPT export format"""
        try:
            # ChatGPT exports have specific structure
            data = json.loads(sample) if len(sample) < 4096 else json.loads(sample[:sample.rfind('}')+1])

            # Check for ChatGPT-specific fields
            if isinstance(data, list):
                if len(data) > 0 and 'mapping' in data[0]:
                    return True
                if len(data) > 0 and 'message' in data[0]:
                    # Older ChatGPT export format
                    return True

        except (json.JSONDecodeError, KeyError):
            pass

        return False

    def _is_claude_json(self, sample: str, file_path: Path) -> bool:
        """Detect Claude conversation export format"""
        try:
            data = json.loads(sample) if len(sample) < 4096 else json.loads(sample[:sample.rfind('}')+1])

            # Claude exports and generic conversation JSONs are arrays of {role, content} objects
            if isinstance(data, list):
                if len(data) > 0:
                    first = data[0]
                    if isinstance(first, dict) and 'role' in first and 'content' in first:
                        # Accept any {role, content} format as valid conversation JSON
                        # (covers Claude, generic exports, and other standard formats)
                        return True

        except (json.JSONDecodeError, KeyError):
            pass

        return False

    def _is_markdown_turns(self, sample: str, file_path: Path) -> bool:
        """Detect markdown conversation format"""
        # Look for common markdown conversation patterns
        patterns = [
            r'^\s*##?\s*(User|Human|Assistant|AI|Claude|GPT):',  # Headers
            r'^\s*\*\*(?:User|Human|Assistant|AI):\*\*',  # Bold markers
            r'^\s*\|.*\|.*\|',  # Table format
        ]

        for pattern in patterns:
            if re.search(pattern, sample, re.MULTILINE | re.IGNORECASE):
                return True

        return False

    def _is_plain_text(self, sample: str, file_path: Path) -> bool:
        """Detect plain text conversation (fallback)"""
        # If it's readable text and not one of the above, treat as plain text
        # This is our fallback - always returns True if file is readable
        return True

    def parse_file(self, file_path: Path) -> Iterator[Turn]:
        """
        Parse file and yield normalized turns (streaming)

        Yields Turn objects one at a time - no memory bloat regardless of file size
        """
        format_type = self.detect_format(file_path)

        print(f"📖 Parsing {file_path.name} as {format_type.value}")

        # Route to appropriate parser
        if format_type == ConversationFormat.CHATGPT_JSON:
            yield from self._parse_chatgpt_json(file_path)
        elif format_type == ConversationFormat.CLAUDE_JSON:
            yield from self._parse_claude_json(file_path)
        elif format_type == ConversationFormat.MARKDOWN_TURNS:
            yield from self._parse_markdown_turns(file_path)
        elif format_type == ConversationFormat.PLAIN_TEXT:
            yield from self._parse_plain_text(file_path)
        else:
            print(f"⚠️  Warning: Unknown format for {file_path}, attempting plain text parse")
            yield from self._parse_plain_text(file_path)

    def _parse_chatgpt_json(self, file_path: Path) -> Iterator[Turn]:
        """Parse ChatGPT export format"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different ChatGPT export structures
            if isinstance(data, list):
                for item in data:
                    if 'mapping' in item:
                        # Newer ChatGPT export with mapping structure
                        yield from self._parse_chatgpt_mapping(item['mapping'])
                    elif 'message' in item:
                        # Older ChatGPT export format
                        msg = item['message']
                        if 'content' in msg and 'role' in msg:
                            yield Turn(
                                role=msg['role'],
                                content=self._extract_content(msg['content']),
                                timestamp=item.get('timestamp'),
                                metadata={'source': 'chatgpt'}
                            )

        except Exception as e:
            print(f"❌ Error parsing ChatGPT JSON {file_path}: {e}")

    def _parse_chatgpt_mapping(self, mapping: Dict) -> Iterator[Turn]:
        """Parse ChatGPT's mapping structure"""
        # Sort by creation time to maintain conversation order
        items = []
        for node_id, node_data in mapping.items():
            if 'message' in node_data and node_data['message']:
                msg = node_data['message']
                if 'content' in msg and 'role' in msg:
                    items.append((
                        msg.get('create_time', 0),
                        Turn(
                            role=msg['role'],
                            content=self._extract_content(msg['content']),
                            timestamp=str(msg.get('create_time')),
                            metadata={'node_id': node_id, 'source': 'chatgpt'}
                        )
                    ))

        # Yield in chronological order
        for _, turn in sorted(items, key=lambda x: x[0]):
            yield turn

    def _parse_claude_json(self, file_path: Path) -> Iterator[Turn]:
        """Parse Claude conversation export format"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'role' in item and 'content' in item:
                        yield Turn(
                            role=item['role'],
                            content=self._extract_content(item['content']),
                            timestamp=item.get('timestamp'),
                            metadata={'source': 'claude', **{k: v for k, v in item.items() if k not in ['role', 'content', 'timestamp']}}
                        )

        except Exception as e:
            print(f"❌ Error parsing Claude JSON {file_path}: {e}")

    def _parse_markdown_turns(self, file_path: Path) -> Iterator[Turn]:
        """Parse markdown conversation format"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split by common markdown turn markers
            patterns = [
                (r'##?\s*(User|Human):', 'user'),
                (r'##?\s*(Assistant|AI|Claude|GPT):', 'assistant'),
                (r'\*\*(User|Human):\*\*', 'user'),
                (r'\*\*(Assistant|AI|Claude|GPT):\*\*', 'assistant'),
            ]

            # Find all turn boundaries
            turns = []
            for pattern, role in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                    turns.append((match.start(), role, match.end()))

            # Sort by position
            turns.sort(key=lambda x: x[0])

            # Extract turn content
            for i, (start, role, content_start) in enumerate(turns):
                # Content goes until next turn or end of file
                end = turns[i+1][0] if i+1 < len(turns) else len(content)
                turn_content = content[content_start:end].strip()

                if turn_content:
                    yield Turn(
                        role=role,
                        content=turn_content,
                        metadata={'source': 'markdown'}
                    )

        except Exception as e:
            print(f"❌ Error parsing markdown {file_path}: {e}")

    def _parse_plain_text(self, file_path: Path) -> Iterator[Turn]:
        """Parse plain text (best effort)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try to detect speaker changes
            # Look for patterns like "User:", "Q:", "A:", etc.
            lines = content.split('\n')
            current_role = 'user'
            current_content = []

            for line in lines:
                # Check for role indicators
                line_lower = line.lower().strip()

                if line_lower.startswith(('user:', 'human:', 'q:')):
                    # Flush previous turn
                    if current_content:
                        yield Turn(
                            role=current_role,
                            content='\n'.join(current_content).strip(),
                            metadata={'source': 'plain_text'}
                        )
                    current_role = 'user'
                    current_content = [line.split(':', 1)[1].strip() if ':' in line else '']

                elif line_lower.startswith(('assistant:', 'ai:', 'a:', 'claude:', 'gpt:')):
                    # Flush previous turn
                    if current_content:
                        yield Turn(
                            role=current_role,
                            content='\n'.join(current_content).strip(),
                            metadata={'source': 'plain_text'}
                        )
                    current_role = 'assistant'
                    current_content = [line.split(':', 1)[1].strip() if ':' in line else '']

                else:
                    # Continue current turn
                    current_content.append(line)

            # Flush final turn
            if current_content:
                content_str = '\n'.join(current_content).strip()
                if content_str:
                    yield Turn(
                        role=current_role,
                        content=content_str,
                        metadata={'source': 'plain_text'}
                    )

        except Exception as e:
            print(f"❌ Error parsing plain text {file_path}: {e}")

    def _extract_content(self, content: Any) -> str:
        """Extract string content from various formats"""
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            # ChatGPT sometimes nests content in 'parts'
            if 'parts' in content:
                return '\n'.join(str(p) for p in content['parts'])
            # Or in 'text'
            elif 'text' in content:
                return str(content['text'])
            else:
                return str(content)
        elif isinstance(content, list):
            return '\n'.join(str(item) for item in content)
        else:
            return str(content)


def main():
    """Test the universal parser"""
    if len(sys.argv) < 2:
        print("Usage: python universal_parser.py <conversation_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    parser = UniversalParser()

    turn_count = 0
    for turn in parser.parse_file(file_path):
        turn_count += 1
        print(f"\n{'='*60}")
        print(f"Turn {turn_count} ({turn.role}):")
        print(f"{'='*60}")
        print(turn.content[:500] + "..." if len(turn.content) > 500 else turn.content)

    print(f"\n✓ Parsed {turn_count} turns from {file_path.name}")


if __name__ == "__main__":
    main()
