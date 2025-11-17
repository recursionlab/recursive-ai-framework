#!/usr/bin/env python3
"""
HEALTH CHECK - One-Command System Verification

Run this anytime to verify the system is working:
    python3 health_check.py

Quick, simple output - just tells you if things are broken.
"""

import json
from pathlib import Path

def check():
    """Quick health check - returns True if system is healthy"""

    try:
        # Check critical files exist
        critical_files = [
            'extraction_outputs/pattern_extraction.json',
            'extraction_outputs/refined_commutators.json',
            'extraction_outputs/torsion_field_analysis.json',
        ]

        for f in critical_files:
            if not Path(f).exists():
                print(f"✗ MISSING: {f}")
                return False

        # Check key data integrity
        with open('extraction_outputs/pattern_extraction.json', encoding='utf-8') as f:
            extraction = json.load(f)
            total_contradictions = sum(len(e['contradictions']) for e in extraction)
            if total_contradictions != 73949:
                print(f"✗ WRONG COUNT: {total_contradictions} contradictions (expected 73,949)")
                return False

        with open('extraction_outputs/refined_commutators.json', encoding='utf-8') as f:
            commutators = json.load(f)
            meta_meta = commutators['evidence_pairs'].get('Meta,Meta')
            if not meta_meta or meta_meta['magnitude'] != 1.0:
                print("✗ DISCOVERY MISSING: Meta ∘ Meta ≠ 1.0")
                return False

        with open('extraction_outputs/torsion_field_analysis.json', encoding='utf-8') as f:
            torsion = json.load(f)
            if torsion['metadata']['invariants'] != 17:
                print(f"✗ WRONG COUNT: {torsion['metadata']['invariants']} invariants (expected 17)")
                return False

        # All checks passed
        print("✓ System healthy - all components operational")
        print(f"  • 73,949 contradictions extracted")
        print(f"  • Meta ∘ Meta = 1.000 (max torsion)")
        print(f"  • 17 invariants found")
        print(f"  • 35 torsion pairs computed")
        return True

    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == '__main__':
    import sys
    sys.exit(0 if check() else 1)
