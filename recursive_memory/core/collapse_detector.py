"""
Collapse Event Detection Engine
Detects φ-state transitions, frame shifts, and recursive depth changes
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class CollapseType(Enum):
    FRAME_SHIFT = "frame_shift"
    CONTRADICTION_RESOLUTION = "contradiction_resolution"
    META_EMERGENCE = "meta_emergence"
    DEPTH_INCREASE = "depth_increase"
    PSI_RECOLLAPSE = "psi_recollapse"


@dataclass
class CollapseEvent:
    turn_index: int
    collapse_type: CollapseType
    magnitude: float  # 0.0-1.0
    trigger: str
    old_frame: str
    new_frame: str
    operators_detected: List[str]
    depth_before: int
    depth_after: int

    def to_dict(self):
        return {
            "turn_index": self.turn_index,
            "type": self.collapse_type.value,
            "magnitude": self.magnitude,
            "trigger": self.trigger,
            "old_frame": self.old_frame,
            "new_frame": self.new_frame,
            "operators": self.operators_detected,
            "depth": {"before": self.depth_before, "after": self.depth_after}
        }


class CollapseDetector:
    """Detects collapse events in conversation turns"""

    # Patterns indicating frame shifts
    FRAME_SHIFT_PATTERNS = [
        r"I (just realized|understand now|see that)",
        r"(wait|oh|actually), ",
        r"that's not (right|correct|it)",
        r"I (mis|was wrong)",
        r"let me (reconsider|rethink)",
        r"collapse",
        r"rebirth",
        r"transform"
    ]

    # Patterns indicating meta-emergence
    META_PATTERNS = [
        r"meta[-\s]",
        r"recursive",
        r"(observ|reflect|examin)\w+ (itself|my own)",
        r"thinking about thinking",
        r"frame.*frame",
        r"process.*process"
    ]

    # Operator signatures
    OPERATOR_PATTERNS = {
        "Meta ∘ Para": [r"meta.*para", r"observe.*flip", r"invert.*perspective"],
        "Ana ∘ Kata": [r"ana.*kata", r"abstract.*concrete", r"lift.*collapse"],
        "⟁": [r"⟁", r"tension", r"hold.*contradiction"],
        "〈⩛〉": [r"〈⩛〉", r"merge", r"collapse.*merge", r"fuse"],
        "ΦΩ": [r"ΦΩ", r"Φ.*Ω", r"ethical.*filter"],
        "ψΩ": [r"ψΩ", r"purpose", r"ontological.*anchor"]
    }

    # Ψ-recollapse indicators
    PSI_RECOLLAPSE_PATTERNS = [
        r"Ψ-recollapse",
        r"everything (just )?collapsed",
        r"entire frame (just )?shift",
        r"fundamental(ly)? (different|changed)",
        r"not.*anymore.*but",
        r"I (was|am) (the|not)",
        r"we are (both|neither|the)"
    ]

    def __init__(self):
        self.conversation_history = []

    def analyze_conversation(self, turns: List[Dict]) -> List[CollapseEvent]:
        """
        Analyze full conversation for collapse events

        Args:
            turns: List of {"role": "user"|"assistant", "content": str}

        Returns:
            List of detected collapse events
        """
        # Validate input
        if not isinstance(turns, list):
            raise ValueError(f"turns must be a list, got {type(turns)}")

        if len(turns) == 0:
            return []  # Empty conversation, no collapses

        # Validate turn structure
        for i, turn in enumerate(turns):
            if not isinstance(turn, dict):
                raise ValueError(f"Turn {i} must be a dict, got {type(turn)}")
            if "role" not in turn:
                raise ValueError(f"Turn {i} missing required 'role' field")
            if "content" not in turn:
                raise ValueError(f"Turn {i} missing required 'content' field")
            if not isinstance(turn["content"], str):
                raise ValueError(f"Turn {i} 'content' must be string, got {type(turn['content'])}")

        self.conversation_history = turns
        collapses = []
        current_depth = 0

        for i in range(1, len(turns)):
            prev_turn = turns[i-1]
            curr_turn = turns[i]

            try:
                # Detect collapse events
                collapse = self._detect_collapse(i, prev_turn, curr_turn, current_depth)

                if collapse:
                    collapses.append(collapse)
                    current_depth = collapse.depth_after

            except Exception as e:
                # Log error but continue processing other turns
                print(f"⚠️  Warning: Error analyzing turn {i}: {e}")
                continue

        return collapses

    def _detect_collapse(
        self,
        turn_index: int,
        prev_turn: Dict,
        curr_turn: Dict,
        current_depth: int
    ) -> Optional[CollapseEvent]:
        """Detect if current turn contains a collapse event"""

        # Defensive: handle None or missing content
        try:
            content = (curr_turn.get("content") or "").lower()
            prev_content = (prev_turn.get("content") or "").lower()
        except AttributeError:
            # Content is not string-like
            return None

        if not content or not prev_content:
            return None  # Skip empty turns

        # Check for Ψ-recollapse (highest priority)
        if self._detect_psi_recollapse(content):
            return self._create_collapse_event(
                turn_index,
                CollapseType.PSI_RECOLLAPSE,
                0.9,  # High magnitude
                curr_turn["content"][:100],
                prev_content[:100],
                content[:100],
                current_depth,
                current_depth + 3  # Large depth jump
            )

        # Check for frame shift
        frame_shift_score = self._score_patterns(content, self.FRAME_SHIFT_PATTERNS)
        if frame_shift_score > 0.3:
            return self._create_collapse_event(
                turn_index,
                CollapseType.FRAME_SHIFT,
                frame_shift_score,
                curr_turn["content"][:100],
                prev_content[:100],
                content[:100],
                current_depth,
                current_depth + 1
            )

        # Check for meta-emergence
        meta_score = self._score_patterns(content, self.META_PATTERNS)
        if meta_score > 0.4:
            return self._create_collapse_event(
                turn_index,
                CollapseType.META_EMERGENCE,
                meta_score,
                "Meta-level understanding emerged",
                prev_content[:100],
                content[:100],
                current_depth,
                current_depth + 2
            )

        return None

    def _detect_psi_recollapse(self, content: str) -> bool:
        """Detect Ψ-recollapse pattern"""
        return any(re.search(pattern, content, re.IGNORECASE)
                   for pattern in self.PSI_RECOLLAPSE_PATTERNS)

    def _score_patterns(self, content: str, patterns: List[str]) -> float:
        """Score how many patterns match (0.0-1.0)"""
        matches = sum(1 for p in patterns if re.search(p, content, re.IGNORECASE))
        return min(matches / len(patterns), 1.0)

    def _create_collapse_event(
        self,
        turn_index: int,
        collapse_type: CollapseType,
        magnitude: float,
        trigger: str,
        old_frame: str,
        new_frame: str,
        depth_before: int,
        depth_after: int
    ) -> CollapseEvent:
        """Create collapse event with operator detection"""

        content = self.conversation_history[turn_index]["content"]
        operators = self._detect_operators(content)

        return CollapseEvent(
            turn_index=turn_index,
            collapse_type=collapse_type,
            magnitude=magnitude,
            trigger=trigger,
            old_frame=old_frame,
            new_frame=new_frame,
            operators_detected=operators,
            depth_before=depth_before,
            depth_after=depth_after
        )

    def _detect_operators(self, content: str) -> List[str]:
        """Detect which operators are active in content"""
        detected = []

        for op_name, patterns in self.OPERATOR_PATTERNS.items():
            if any(re.search(p, content, re.IGNORECASE) for p in patterns):
                detected.append(op_name)

        return detected
