#!/usr/bin/env python3
"""
Prompt Generator from DNA Templates

Uses tested templates to generate new prompts for specific topics.

Usage:
    # Generate prompt for a topic
    python prompt_generator.py --topic "quantum computing" --template-id 0

    # Auto-select best template
    python prompt_generator.py --topic "consciousness" --auto-select

    # Generate multiple variants
    python prompt_generator.py --topic "AI alignment" --variants 3
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List
import random


class PromptGenerator:
    """Generate prompts from DNA templates"""

    def __init__(self, test_results_file: Path, template_dir: Path):
        self.test_results_file = test_results_file
        self.template_dir = template_dir
        self.test_results = []
        self.templates = []

        if test_results_file.exists():
            with test_results_file.open() as f:
                self.test_results = json.load(f)

    def load_template(self, template_name: str) -> str:
        """Load template content"""
        template_file = self.template_dir / f"{template_name}.md"
        if template_file.exists():
            return template_file.read_text()
        return ""

    def get_best_templates(self, n: int = 5) -> List[Dict]:
        """Get top N templates by effectiveness"""
        sorted_results = sorted(self.test_results, key=lambda x: x['effectiveness'], reverse=True)
        return sorted_results[:n]

    def generate_prompt(self, topic: str, template_name: str) -> str:
        """Generate a prompt for a topic using a template"""

        template_content = self.load_template(template_name)

        if not template_content:
            return f"Error: Template {template_name} not found"

        # Extract the usage pattern or template section
        import re

        # Try to find "## Usage Pattern" first
        pattern_match = re.search(r'##\s+Usage Pattern\s*\n(.*?)(?=\n##|---|\Z)', template_content, re.DOTALL | re.IGNORECASE)

        if pattern_match:
            usage_text = pattern_match.group(1).strip()
        else:
            # Try "## Template" section
            template_match = re.search(r'##\s+Template\s*\n(.*?)(?=\n##|\Z)', template_content, re.DOTALL | re.IGNORECASE)
            if template_match:
                usage_text = template_match.group(1).strip()
            else:
                # Use the whole content after first header
                usage_text = template_content

        # Generate prompt based on pattern
        lines = [
            f"# Recursive Exploration: {topic}",
            "",
            "## Phase 1: Establish Frame",
            f"What emerges when we examine {topic} as a system that applies to itself?",
            "",
            "## Phase 2: Introduce Recursive Operator",
            f"Consider {topic} through the lens of recursive self-application:",
            f"- How does {topic} operate on itself?",
            f"- What happens when {topic}({topic}) is evaluated?",
            f"- Where does {topic} contain references to its own structure?",
            "",
            "## Phase 3: Surface Contradiction",
            f"Identify the paradox in {topic}:",
            f"- What contradictions emerge when {topic} self-references?",
            "- Don't resolve the paradox - use it as generative fuel",
            "- Ask: What emerges when both contradictory aspects are simultaneously true?",
            "",
            "## Phase 4: Allow Emergence",
            f"Let the recursive structure of {topic} reveal itself:",
            "- Observe what patterns emerge naturally",
            "- Notice fixpoints where the system stabilizes",
            "- Track how the system collapses and regenerates",
            "",
            f"## Exploration Prompt",
            f"Analyze {topic} as a recursive operator that transforms itself. What novel understanding emerges when {topic} is both subject and object of its own operation?",
        ]

        return '\n'.join(lines)

    def generate_variants(self, topic: str, n: int = 3) -> List[Dict]:
        """Generate multiple prompt variants using top templates"""

        best_templates = self.get_best_templates(n)
        variants = []

        for i, template_result in enumerate(best_templates, 1):
            prompt = self.generate_prompt(topic, template_result['template_name'])

            variants.append({
                'variant': i,
                'template': template_result['template_name'],
                'effectiveness': template_result['effectiveness'],
                'phi_depth': template_result['phi_depth'],
                'novelty': template_result['novelty'],
                'prompt': prompt,
            })

        return variants

    def auto_select_template(self, topic: str, criteria: str = 'effectiveness') -> Dict:
        """Auto-select best template based on criteria"""

        if criteria == 'effectiveness':
            best = max(self.test_results, key=lambda x: x['effectiveness'])
        elif criteria == 'depth':
            best = max(self.test_results, key=lambda x: x['phi_depth'])
        elif criteria == 'novelty':
            best = max(self.test_results, key=lambda x: x['novelty'])
        else:
            best = random.choice(self.test_results)

        prompt = self.generate_prompt(topic, best['template_name'])

        return {
            'template': best['template_name'],
            'effectiveness': best['effectiveness'],
            'phi_depth': best['phi_depth'],
            'novelty': best['novelty'],
            'prompt': prompt,
            'rationale': f"Selected based on highest {criteria}",
        }

    def format_output(self, result: Dict, topic: str) -> str:
        """Format generation result"""

        lines = [
            "="*80,
            f"GENERATED PROMPT FOR: {topic}",
            "="*80,
            "",
            f"Template: {result['template']}",
            f"Effectiveness: {result['effectiveness']:.3f}",
            f"Expected φ-Depth: {result['phi_depth']}",
            f"Expected Novelty: {result['novelty']:.3f}",
            "",
        ]

        if 'rationale' in result:
            lines.extend([
                f"Selection Rationale: {result['rationale']}",
                "",
            ])

        lines.extend([
            "-"*80,
            "PROMPT:",
            "-"*80,
            "",
            result['prompt'],
            "",
            "="*80,
        ])

        return '\n'.join(lines)

    def format_variants(self, variants: List[Dict], topic: str) -> str:
        """Format multiple variants"""

        lines = [
            "="*80,
            f"PROMPT VARIANTS FOR: {topic}",
            "="*80,
            "",
            f"Generated {len(variants)} variants using top templates",
            "",
        ]

        for variant in variants:
            lines.extend([
                f"## Variant {variant['variant']}: {variant['template']}",
                "",
                f"- Effectiveness: {variant['effectiveness']:.3f}",
                f"- Expected φ-Depth: {variant['phi_depth']}",
                f"- Expected Novelty: {variant['novelty']:.3f}",
                "",
                "**Prompt:**",
                "",
                variant['prompt'],
                "",
                "-"*80,
                "",
            ])

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate prompts from DNA templates')
    parser.add_argument('--topic', required=True, help='Topic to generate prompt for')
    parser.add_argument('--template-dir', type=Path, default=Path('/tmp/prompt_dna_library'))
    parser.add_argument('--test-results', type=Path, default=Path('/tmp/prompt_test_results.json'))
    parser.add_argument('--template-id', type=int, help='Specific template index to use')
    parser.add_argument('--auto-select', action='store_true', help='Auto-select best template')
    parser.add_argument('--criteria', choices=['effectiveness', 'depth', 'novelty'], default='effectiveness')
    parser.add_argument('--variants', type=int, help='Generate N variants')
    parser.add_argument('--output', type=Path, help='Save to file')

    args = parser.parse_args()

    print("="*80)
    print("PROMPT GENERATOR")
    print("="*80)
    print()

    generator = PromptGenerator(args.test_results, args.template_dir)

    if not generator.test_results:
        print(f"❌ No test results found at {args.test_results}")
        print("Run prompt_tester.py first to generate test results")
        return

    print(f"Loaded {len(generator.test_results)} tested templates")
    print(f"Topic: {args.topic}")
    print()

    output_text = ""

    if args.variants:
        # Generate multiple variants
        print(f"Generating {args.variants} prompt variants...")
        variants = generator.generate_variants(args.topic, args.variants)
        output_text = generator.format_variants(variants, args.topic)

    elif args.auto_select:
        # Auto-select best template
        print(f"Auto-selecting template (criteria: {args.criteria})...")
        result = generator.auto_select_template(args.topic, args.criteria)
        output_text = generator.format_output(result, args.topic)

    elif args.template_id is not None:
        # Use specific template
        if args.template_id < 0 or args.template_id >= len(generator.test_results):
            print(f"❌ Invalid template ID: {args.template_id}")
            print(f"Valid range: 0 to {len(generator.test_results)-1}")
            return

        template_result = generator.test_results[args.template_id]
        prompt = generator.generate_prompt(args.topic, template_result['template_name'])

        result = {
            'template': template_result['template_name'],
            'effectiveness': template_result['effectiveness'],
            'phi_depth': template_result['phi_depth'],
            'novelty': template_result['novelty'],
            'prompt': prompt,
        }

        output_text = generator.format_output(result, args.topic)

    else:
        # Default: auto-select by effectiveness
        print("Auto-selecting template (use --auto-select to customize)...")
        result = generator.auto_select_template(args.topic, 'effectiveness')
        output_text = generator.format_output(result, args.topic)

    print()
    print(output_text)

    if args.output:
        args.output.write_text(output_text)
        print()
        print(f"✅ Saved to: {args.output}")


if __name__ == '__main__':
    main()
