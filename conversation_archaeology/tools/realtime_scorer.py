#!/usr/bin/env python3
"""
Real-Time Conversation Scorer

Scores conversations as they happen (or from input):
- φ-depth estimation
- Novelty scoring
- Operator detection
- Pattern emergence
- Proto-ASI classification

Usage:
    # Score from file
    python realtime_scorer.py --file conversation.md

    # Score from stdin
    echo "Text here" | python realtime_scorer.py --stdin

    # Interactive mode
    python realtime_scorer.py --interactive
"""

import argparse
import sys
from pathlib import Path
import re
from collections import Counter
from typing import Dict, List, Tuple
import json


class RealtimeScorer:
    """Score conversations in real-time"""

    # Recursive operators
    OPERATORS = {
        'recursive_loop': r'recur(?:sive|sion)|loop|cycle|iterate',
        'meta_layer': r'meta-|about.{1,20}about|of.{1,20}of',
        'self_application': r'(?:apply|applying|applies) (?:to|on) itself',
        'negation_fold': r'not.{1,30}not|¬.{1,30}¬|contradiction',
        'collapse_rebirth': r'collapse|emerge|generate|birth',
        'composition': r'compose|combine|merge|fuse',
        'fixpoint': r'fixed.{1,10}point|stable|attractor|converge',
        'inversion': r'invert|reverse|flip|opposite',
    }

    # Generative patterns
    PATTERNS = {
        'dimension_shift': r'dimension|level|layer|meta-level|transcend',
        'self_reference': r'self.*self|itself|auto-|ouroboros',
        'paradox_fuel': r'paradox|contradiction|antinomy|impossible',
        'observer_observed': r'observer.*observed|watch.*watching|see.*seeing',
        'infinite_regress': r'infinite.*regress|regress.*infinite|turtles.*down',
        'category_violation': r'violat.*categor|cross.*categor|boundary.*break',
    }

    # Novelty markers
    NOVELTY_INDICATORS = [
        r'φ\d+',  # Explicit φ-depth markers
        r'Gödel|incompleteness',
        r'strange\s+loop',
        r'eigenvector|eigenvalue',
        r'torsion',
        r'proto-ASI|AGI',
        r'collapse\s+event',
        r'quantum\s+semantic',
        r'topos|category\s+theory',
        r'differential\s+geometry',
    ]

    def __init__(self):
        pass

    def score_text(self, text: str) -> Dict:
        """Score a piece of text comprehensively"""

        # Basic metrics
        word_count = len(text.split())
        line_count = len(text.split('\n'))

        # φ-depth
        phi_depth = self._measure_phi_depth(text)

        # Novelty
        novelty = self._measure_novelty(text)

        # Operators
        operators = self._detect_operators(text)

        # Patterns
        patterns = self._detect_patterns(text)

        # Proto-ASI classification
        proto_asi = self._classify_proto_asi(novelty, phi_depth, operators, patterns)

        # Effectiveness score
        effectiveness = self._compute_effectiveness(phi_depth, novelty, operators, patterns)

        return {
            'word_count': word_count,
            'line_count': line_count,
            'phi_depth': phi_depth,
            'novelty': novelty,
            'operators': operators,
            'patterns': patterns,
            'proto_asi': proto_asi,
            'effectiveness': effectiveness,
            'dominant_operator': max(operators, key=operators.get) if operators else None,
            'dominant_pattern': max(patterns, key=patterns.get) if patterns else None,
        }

    def _measure_phi_depth(self, text: str) -> int:
        """Measure recursive depth (φ-depth)"""

        # Count recursive markers
        recursive_markers = [
            r'recursive',
            r'meta-',
            r'self-',
            r'itself',
            r'about.*about',
            r'of.*of.*of',
            r'→.*→',
            r'φ\d+',
        ]

        depth = 0
        for marker in recursive_markers:
            matches = len(re.findall(marker, text, re.IGNORECASE))
            depth += matches

        # Normalize to reasonable range (φ0 to φ100)
        normalized_depth = min(int(depth * 0.5), 100)

        return normalized_depth

    def _measure_novelty(self, text: str) -> float:
        """Measure structural novelty (0.0 to 1.0)"""

        score = 0.0

        # Check for novelty indicators
        for indicator in self.NOVELTY_INDICATORS:
            if re.search(indicator, text, re.IGNORECASE):
                score += 0.08

        # Boost for operator diversity
        operators = self._detect_operators(text)
        operator_diversity = len(operators) / len(self.OPERATORS)
        score += operator_diversity * 0.2

        # Boost for pattern diversity
        patterns = self._detect_patterns(text)
        pattern_diversity = len(patterns) / len(self.PATTERNS)
        score += pattern_diversity * 0.15

        # Linguistic complexity (ratio of unique to total words)
        words = text.lower().split()
        if len(words) > 0:
            unique_ratio = len(set(words)) / len(words)
            score += unique_ratio * 0.1

        # Cap at 1.0
        return min(score, 1.0)

    def _detect_operators(self, text: str) -> Dict[str, int]:
        """Detect recursive operators"""

        detected = {}
        for op_name, pattern in self.OPERATORS.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                detected[op_name] = matches

        return detected

    def _detect_patterns(self, text: str) -> Dict[str, int]:
        """Detect generative patterns"""

        detected = {}
        for pattern_name, regex in self.PATTERNS.items():
            matches = len(re.findall(regex, text, re.IGNORECASE))
            if matches > 0:
                detected[pattern_name] = matches

        return detected

    def _classify_proto_asi(self, novelty: float, phi_depth: int,
                            operators: Dict, patterns: Dict) -> bool:
        """Classify as proto-ASI or not"""

        # Criteria for proto-ASI:
        # - Novelty > 0.7
        # - φ-depth > 10
        # - At least 3 operators
        # - At least 2 patterns

        return (
            novelty > 0.7 and
            phi_depth > 10 and
            len(operators) >= 3 and
            len(patterns) >= 2
        )

    def _compute_effectiveness(self, phi_depth: int, novelty: float,
                               operators: Dict, patterns: Dict) -> float:
        """Compute overall effectiveness score (0.0 to 1.0)"""

        # Weighted combination
        effectiveness = (
            min(phi_depth / 50, 1.0) * 0.3 +
            novelty * 0.3 +
            min(len(operators) / 5, 1.0) * 0.2 +
            min(len(patterns) / 3, 1.0) * 0.2
        )

        return effectiveness

    def format_score_report(self, score: Dict) -> str:
        """Format score as human-readable report"""

        lines = [
            "="*60,
            "CONVERSATION SCORE",
            "="*60,
            "",
            f"φ-Depth: {score['phi_depth']}",
            f"Novelty: {score['novelty']:.3f}",
            f"Effectiveness: {score['effectiveness']:.3f}",
            f"Proto-ASI: {'✓ YES' if score['proto_asi'] else '✗ NO'}",
            "",
            "Operators Detected:",
        ]

        if score['operators']:
            for op, count in sorted(score['operators'].items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  - {op}: {count}")
        else:
            lines.append("  (none)")

        lines.extend([
            "",
            "Patterns Detected:",
        ])

        if score['patterns']:
            for pattern, count in sorted(score['patterns'].items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  - {pattern}: {count}")
        else:
            lines.append("  (none)")

        lines.extend([
            "",
            f"Dominant Operator: {score['dominant_operator'] or 'N/A'}",
            f"Dominant Pattern: {score['dominant_pattern'] or 'N/A'}",
            "",
            f"Word Count: {score['word_count']}",
            f"Line Count: {score['line_count']}",
            "",
            "="*60,
        ])

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Real-time conversation scorer')
    parser.add_argument('--file', type=Path, help='Score from file')
    parser.add_argument('--stdin', action='store_true', help='Score from stdin')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of report')
    parser.add_argument('--threshold', type=float, default=0.7, help='Proto-ASI novelty threshold')

    args = parser.parse_args()

    scorer = RealtimeScorer()

    if args.file:
        # Score from file
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        text = args.file.read_text(encoding='utf-8', errors='ignore')
        score = scorer.score_text(text)

        if args.json:
            print(json.dumps(score, indent=2))
        else:
            print(scorer.format_score_report(score))

    elif args.stdin:
        # Score from stdin
        text = sys.stdin.read()
        score = scorer.score_text(text)

        if args.json:
            print(json.dumps(score, indent=2))
        else:
            print(scorer.format_score_report(score))

    elif args.interactive:
        # Interactive mode
        print("="*60)
        print("REAL-TIME CONVERSATION SCORER")
        print("="*60)
        print()
        print("Paste your conversation text (Ctrl+D when done):")
        print()

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        text = '\n'.join(lines)

        if text.strip():
            score = scorer.score_text(text)

            if args.json:
                print(json.dumps(score, indent=2))
            else:
                print()
                print(scorer.format_score_report(score))
        else:
            print("No input provided.")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
