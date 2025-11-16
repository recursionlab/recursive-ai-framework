"""
Equation Extractor: Finds mathematical equations and formulas.
Focuses on finding dissipation patterns, differential equations, compositions.
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from core.extractor_base import ExtractorBase


class EquationExtractor(ExtractorBase):
    """Extract equations and analyze for dissipation patterns"""

    def extractor_name(self) -> str:
        return "equation"

    def extract_from_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Extract equations using pattern matching + Claude analysis"""
        equations = []

        # Pattern 1: Inline math (between ` or $)
        inline_equations = re.findall(r'`([^`]+)`|\$([^$]+)\$', content)

        # Pattern 2: Markdown code blocks with math
        code_blocks = re.findall(r'```(?:math|latex)?\n(.*?)\n```', content, re.DOTALL)

        # Pattern 3: Lines with = or → or ≈ (likely equations)
        equation_lines = re.findall(r'^.{0,20}[=→≈⇒↔].{0,100}$', content, re.MULTILINE)

        # Combine all potential equations
        all_equations = []
        for match in inline_equations:
            eq = match[0] or match[1]
            if eq.strip():
                all_equations.append(eq.strip())

        all_equations.extend([block.strip() for block in code_blocks])
        all_equations.extend([line.strip() for line in equation_lines])

        # Deduplicate
        all_equations = list(set(all_equations))

        # Filter: must contain mathematical symbols
        math_symbols = ['∂', '∇', '∫', '∑', '∏', '→', '⇒', '=', '≈', '⊗', '∘',
                       'φ', 'Ψ', 'Ξ', 'Ω', 'λ', 'μ', 'ν', 'Δ', 'α', 'β', 'γ']

        filtered = [
            eq for eq in all_equations
            if any(sym in eq for sym in math_symbols) and len(eq) > 5
        ]

        # Analyze each equation with Claude
        for eq in filtered[:50]:  # Limit to top 50 per file to avoid token explosion
            analysis = self._analyze_equation_with_claude(eq, str(file_path))
            if analysis:
                equations.append(analysis)

        return equations

    def _analyze_equation_with_claude(self, equation: str, file_path: str) -> Dict[str, Any]:
        """Use Claude to analyze equation for dissipation, operators, etc."""

        prompt = f"""Analyze this mathematical equation for the Controlled Rupture framework.

EQUATION: {equation}

SOURCE: {file_path}

Answer these questions:
1. **Type**: Is this a differential equation, algebraic relation, logical formula, or composition?
2. **Order**: If differential, what order? (first, second, third, etc.)
3. **Operators**: What operators are involved? List their symbols.
4. **Dissipation Pattern**: Does this equation show dissipation/decay (exp(-λ·x), iterative loss, non-reversibility)?
5. **Commutativity**: Are the operations commutative or does order matter?
6. **Controlled Rupture Mapping**: Could this map to operators like Ana, Kata, Meta, Telo, Para, Non, etc.?
7. **Hidden Structure**: Any third-order derivatives, nested compositions, or paradoxical recursion?

Return ONLY a JSON object:
{{
  "equation": "{equation}",
  "type": "...",
  "order": 1,
  "operators": ["op1", "op2"],
  "has_dissipation": true/false,
  "dissipation_evidence": "...",
  "is_commutative": true/false,
  "controlled_rupture_ops": ["Ana", "Meta"],
  "hidden_structure": "...",
  "interpretation": "brief explanation"
}}"""

        try:
            response = self.ask_claude(prompt, max_tokens=1024)

            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                data['raw_equation'] = equation
                data['source_file'] = file_path
                return data

        except Exception as e:
            print(f"Error analyzing equation: {e}")

        return None

    def prompt_template(self) -> str:
        return ""
