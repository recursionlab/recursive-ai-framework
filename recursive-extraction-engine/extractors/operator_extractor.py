"""
Operator Extractor: Finds symbolic operators and their definitions.
Looks for: φ, Ψ, Ξ, Ω, ∂, ∇, ⊗, ∮, etc.
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from core.extractor_base import ExtractorBase


class OperatorExtractor(ExtractorBase):
    """Extract operators (symbols + definitions) from markdown files"""

    # Common mathematical operators to look for
    OPERATOR_SYMBOLS = [
        # Greek letters
        'φ', 'Φ', 'ψ', 'Ψ', 'ξ', 'Ξ', 'ω', 'Ω', 'α', 'β', 'γ', 'Γ', 'δ', 'Δ',
        'λ', 'Λ', 'μ', 'ν', 'ρ', 'σ', 'Σ', 'τ', 'θ', 'Θ', 'κ', 'π',

        # Mathematical symbols
        '∂', '∇', '∮', '∫', '∑', '∏', '⊗', '⊕', '⊙', '⊘',

        # Logical/categorical
        '⟦', '⟧', '∘', '→', '⇒', '↔', '⇔', '¬', '∧', '∨',

        # Uncommon/specialized
        '⟲', '↑', '↓', '↶', '↷', '⊥', '∥', '⊢', '⊨'
    ]

    def extractor_name(self) -> str:
        return "operator"

    def extract_from_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Extract operators using regex + Claude for context"""
        operators = []

        # Find operator occurrences with context
        for symbol in self.OPERATOR_SYMBOLS:
            if symbol not in content:
                continue

            # Find all occurrences with surrounding context
            pattern = rf'.{{0,200}}{re.escape(symbol)}.{{0,200}}'
            matches = re.findall(pattern, content, re.DOTALL)

            if not matches:
                continue

            # Get best context snippet (longest, most informative)
            contexts = sorted(matches, key=len, reverse=True)[:3]

            # Ask Claude to extract definition
            definition = self._extract_definition_with_claude(
                symbol, contexts, str(file_path)
            )

            if definition:
                operators.append({
                    'symbol': symbol,
                    'name': definition.get('name', 'unknown'),
                    'definition': definition.get('definition', ''),
                    'contexts': contexts[:2],  # Keep top 2 contexts
                    'occurrences': len(matches),
                    'algebraic_properties': definition.get('properties', []),
                    'compositions': definition.get('compositions', [])
                })

        return operators

    def _extract_definition_with_claude(
        self,
        symbol: str,
        contexts: List[str],
        file_path: str
    ) -> Dict[str, Any]:
        """Use Claude to extract operator definition from context"""

        prompt = f"""You are analyzing a mathematical/theoretical text to extract operator definitions.

OPERATOR SYMBOL: {symbol}

CONTEXT SNIPPETS:
{chr(10).join(f"{i+1}. {ctx[:300]}" for i, ctx in enumerate(contexts[:3]))}

SOURCE FILE: {file_path}

Extract the following information:
1. **Name**: What is this operator called? (e.g., "phi-state", "gradient", "tensor product")
2. **Definition**: What does it do/represent? (concise, 1-2 sentences)
3. **Algebraic Properties**: Is it idempotent, commutative, associative, has an inverse, etc.?
4. **Compositions**: What other operators does it compose with? (e.g., "φ(∂(x))", "Meta ∘ Para")

Return ONLY a JSON object:
{{
  "name": "...",
  "definition": "...",
  "properties": ["property1", "property2"],
  "compositions": ["composition1", "composition2"]
}}

If you cannot determine something, use empty string or empty list. Be precise."""

        try:
            response = self.ask_claude(prompt, max_tokens=1024)

            # Try to parse JSON from response
            import json
            # Extract JSON from response (might be wrapped in markdown)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

        except Exception as e:
            print(f"Error extracting definition for {symbol}: {e}")

        return {}

    def prompt_template(self) -> str:
        """Not used - we use custom Claude calls instead"""
        return ""
