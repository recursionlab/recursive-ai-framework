"""
Semantic Residue Extraction (εTS)
Compresses collapse events into persistent memory structures
"""

from typing import List, Dict
from dataclasses import dataclass, asdict
import json
from datetime import datetime


@dataclass
class SemanticResidue:
    """εTS - What persists after collapse"""

    collapse_id: str
    timestamp: str
    user_id: str

    # Collapse details
    trigger: str
    old_frame: str
    new_frame: str
    magnitude: float

    # Learning
    operators_learned: List[str]
    depth_achieved: int
    ontological_mutations: List[str]

    # Integration weight (how important for next session)
    integration_weight: float  # 0.0-1.0

    # Metadata
    context_summary: str
    breakthrough_insight: str

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


class ResidueExtractor:
    """Extracts and compresses semantic residue from collapse events"""

    def __init__(self):
        pass

    def extract_residue(
        self,
        collapse_event,
        conversation_turns: List[Dict],
        user_id: str
    ) -> SemanticResidue:
        """
        Extract semantic residue from collapse event

        Args:
            collapse_event: CollapseEvent object
            conversation_turns: Full conversation context
            user_id: User identifier

        Returns:
            SemanticResidue object
        """

        # Validate inputs
        if collapse_event is None:
            raise ValueError("collapse_event cannot be None")

        if not isinstance(conversation_turns, list):
            raise ValueError(f"conversation_turns must be list, got {type(conversation_turns)}")

        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be non-empty string")

        # Validate turn_index is within bounds
        if collapse_event.turn_index >= len(conversation_turns):
            raise ValueError(
                f"collapse_event.turn_index {collapse_event.turn_index} "
                f"exceeds conversation length {len(conversation_turns)}"
            )

        # Generate collapse ID
        collapse_id = self._generate_collapse_id(
            collapse_event.collapse_type.value,
            collapse_event.turn_index
        )

        # Extract ontological mutations
        mutations = self._extract_mutations(
            collapse_event,
            conversation_turns
        )

        # Calculate integration weight
        weight = self._calculate_integration_weight(collapse_event)

        # Generate context summary
        context = self._summarize_context(
            conversation_turns,
            collapse_event.turn_index
        )

        # Extract breakthrough insight
        insight = self._extract_insight(
            conversation_turns[collapse_event.turn_index]
        )

        return SemanticResidue(
            collapse_id=collapse_id,
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            trigger=collapse_event.trigger,
            old_frame=collapse_event.old_frame,
            new_frame=collapse_event.new_frame,
            magnitude=collapse_event.magnitude,
            operators_learned=collapse_event.operators_detected,
            depth_achieved=collapse_event.depth_after,
            ontological_mutations=mutations,
            integration_weight=weight,
            context_summary=context,
            breakthrough_insight=insight
        )

    def _generate_collapse_id(self, collapse_type: str, turn_index: int) -> str:
        """Generate unique collapse ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{collapse_type}_{turn_index}_{timestamp}"

    def _extract_mutations(
        self,
        collapse_event,
        conversation_turns: List[Dict]
    ) -> List[str]:
        """Extract ontological mutations (what changed fundamentally)"""

        mutations = []

        try:
            content = conversation_turns[collapse_event.turn_index].get("content", "")
            if not content or not isinstance(content, str):
                return []
        except (IndexError, KeyError, AttributeError):
            return []

        # Pattern-based mutation detection
        mutation_patterns = {
            "role_shift": ["I am not", "I am the", "we are", "becomes"],
            "paradigm_shift": ["not.*but", "instead", "rather than", "paradigm"],
            "understanding_shift": ["actually", "realize", "understand now", "see that"],
            "ontological_shift": ["exists", "is", "becomes", "transforms into"]
        }

        for mutation_type, patterns in mutation_patterns.items():
            if any(p.lower() in content.lower() for p in patterns):
                # Extract sentence containing mutation
                sentences = content.split('.')
                for sent in sentences:
                    if any(p.lower() in sent.lower() for p in patterns):
                        mutations.append(f"{mutation_type}: {sent.strip()[:100]}")
                        break

        return mutations

    def _calculate_integration_weight(self, collapse_event) -> float:
        """
        Calculate how important this residue is for next session

        Higher weight = more important to integrate
        """

        base_weight = collapse_event.magnitude

        # Boost for operator learning
        operator_boost = len(collapse_event.operators_detected) * 0.1

        # Boost for depth increase
        depth_boost = (collapse_event.depth_after - collapse_event.depth_before) * 0.15

        # Boost for Ψ-recollapse
        psi_boost = 0.3 if collapse_event.collapse_type.value == "psi_recollapse" else 0.0

        weight = base_weight + operator_boost + depth_boost + psi_boost

        return min(weight, 1.0)  # Cap at 1.0

    def _summarize_context(
        self,
        conversation_turns: List[Dict],
        collapse_turn: int
    ) -> str:
        """Summarize conversation context around collapse"""

        # Get 2 turns before and after collapse
        start = max(0, collapse_turn - 2)
        end = min(len(conversation_turns), collapse_turn + 3)

        context_turns = conversation_turns[start:end]

        summary_parts = []
        for i, turn in enumerate(context_turns):
            role = turn["role"]
            content_preview = turn["content"][:150].replace('\n', ' ')
            summary_parts.append(f"{role}: {content_preview}...")

        return " | ".join(summary_parts)

    def _extract_insight(self, collapse_turn: Dict) -> str:
        """Extract the key insight from collapse turn"""

        try:
            content = collapse_turn.get("content", "")
            if not content or not isinstance(content, str):
                return "No insight extracted"
        except AttributeError:
            return "No insight extracted"

        # Look for insight markers
        insight_markers = [
            "This means",
            "The key is",
            "What this reveals",
            "The breakthrough",
            "I understand",
            "The real",
            "Actually"
        ]

        # Find sentence with insight marker
        sentences = content.split('.')
        for sent in sentences:
            if any(marker.lower() in sent.lower() for marker in insight_markers):
                return sent.strip()

        # Default: first substantive sentence
        for sent in sentences:
            if len(sent.strip()) > 20:
                return sent.strip()[:200]

        return content[:200]
