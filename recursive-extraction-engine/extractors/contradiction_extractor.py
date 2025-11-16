"""
Contradiction Extractor: Finds productive contradictions (J'≠0 candidates).
Looks for incompatible definitions, paradoxes, "both true" statements.
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from core.extractor_base import ExtractorBase


class ContradictionExtractor(ExtractorBase):
    """Extract contradictions and classify as sterile or productive (J'≠0)"""

    PARADOX_KEYWORDS = [
        'paradox', 'contradiction', 'incompatible', 'both true', 'neither true',
        'simultaneously', 'yet also', 'but also', 'at the same time',
        'self-reference', 'strange loop', 'infinite regress', 'circular',
        'Gödel', 'incomplete', 'undecidable', 'inconsistent', 'coherent'
    ]

    def extractor_name(self) -> str:
        return "contradiction"

    def extract_from_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Find contradictions using keyword search + Claude analysis"""
        contradictions = []

        # Find sections mentioning paradox/contradiction
        for keyword in self.PARADOX_KEYWORDS:
            pattern = rf'.{{0,300}}{keyword}.{{0,300}}'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)

            for match in matches[:10]:  # Limit per keyword
                analysis = self._analyze_contradiction_with_claude(
                    match, keyword, str(file_path)
                )
                if analysis:
                    contradictions.append(analysis)

        # Also look for definitional conflicts
        # Pattern: "X is A" ... "X is not A" or "X is B" where B conflicts with A
        definitions = self._find_definitional_conflicts(content)
        for conflict in definitions:
            analysis = self._analyze_contradiction_with_claude(
                conflict['context'], 'definitional_conflict', str(file_path)
            )
            if analysis:
                analysis['conflict_term'] = conflict['term']
                contradictions.append(analysis)

        # Deduplicate by similarity
        return self._deduplicate_contradictions(contradictions)

    def _find_definitional_conflicts(self, content: str) -> List[Dict[str, Any]]:
        """Find cases where same term has incompatible definitions"""
        conflicts = []

        # Pattern: "X is Y" or "X = Y"
        definition_pattern = r'([A-Z][a-z]+(?:\([^)]*\))?)\s+(?:is|=|≈)\s+([^.!?\n]+)'
        definitions = re.findall(definition_pattern, content)

        # Group by term
        term_defs = {}
        for term, definition in definitions:
            if term not in term_defs:
                term_defs[term] = []
            term_defs[term].append(definition.strip())

        # Find terms with multiple different definitions
        for term, defs in term_defs.items():
            if len(set(defs)) > 1:
                conflicts.append({
                    'term': term,
                    'definitions': list(set(defs)),
                    'context': f"{term} has multiple definitions: {', '.join(defs[:3])}"
                })

        return conflicts

    def _analyze_contradiction_with_claude(
        self,
        context: str,
        keyword: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Use Claude to classify contradiction as sterile or productive"""

        prompt = f"""Analyze this potential contradiction for the J'≠0 framework.

CONTEXT: {context[:800]}

KEYWORD: {keyword}
SOURCE: {file_path}

Questions:
1. **Is there an actual contradiction?** (yes/no)
2. **Type**: Logical, definitional, temporal, paradoxical, self-referential?
3. **Sterile or Productive?**
   - Sterile: Just an error, confusion, or uninteresting paradox
   - Productive (J'≠0): Generative tension that produces new concepts/insights
4. **J Anomaly Score**: 0.0 (sterile) to 1.0 (highly productive)
5. **Generative Output**: What new concepts/insights emerged from this contradiction?
6. **Controlled Rupture Operators**: Which operators create/resolve this? (Meta ∘ Non, Para, etc.)

Return ONLY a JSON object:
{{
  "has_contradiction": true/false,
  "contradiction_type": "...",
  "is_productive": true/false,
  "j_anomaly_score": 0.0-1.0,
  "explanation": "brief explanation of the contradiction",
  "generative_output": ["concept1", "concept2"],
  "operator_pattern": "Meta ∘ Non ∘ Meta"
}}

If no meaningful contradiction, return {{"has_contradiction": false}}"""

        try:
            response = self.ask_claude(prompt, max_tokens=1024)

            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())

                # Only return if has contradiction
                if data.get('has_contradiction'):
                    data['context_snippet'] = context[:200]
                    data['source_file'] = file_path
                    data['trigger_keyword'] = keyword
                    return data

        except Exception as e:
            print(f"Error analyzing contradiction: {e}")

        return None

    def _deduplicate_contradictions(self, contradictions: List[Dict]) -> List[Dict]:
        """Remove near-duplicates based on context similarity"""
        # Simple dedup by first 100 chars of context
        seen = set()
        unique = []

        for c in contradictions:
            snippet = c.get('context_snippet', '')[:100]
            if snippet not in seen:
                seen.add(snippet)
                unique.append(c)

        return unique

    def prompt_template(self) -> str:
        return ""
