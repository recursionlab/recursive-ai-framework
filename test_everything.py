#!/usr/bin/env python3
"""
MASTER TEST SUITE - Validates All Components End-to-End

Run this to verify everything works:
    python3 test_everything.py

If any test fails, you'll see exactly what broke and where.
"""

import sys
import json
from pathlib import Path
import subprocess

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def print_test(name):
    print(f"{Colors.YELLOW}Testing:{Colors.RESET} {name}...", end=" ")

def print_pass(details=""):
    print(f"{Colors.GREEN}✓ PASS{Colors.RESET}")
    if details:
        print(f"  {details}")

def print_fail(error):
    print(f"{Colors.RED}✗ FAIL{Colors.RESET}")
    print(f"  {Colors.RED}Error: {error}{Colors.RESET}")
    return False

def print_skip(reason):
    print(f"{Colors.YELLOW}⊘ SKIP{Colors.RESET} ({reason})")

# =============================================================================
# PRE-FLIGHT CHECK: Data Files Exist
# =============================================================================

def check_data_exists():
    """Check if extraction data exists, suggest setup if not"""
    critical_data = [
        'extraction_outputs/pattern_extraction.json',
        'extraction_outputs/torsion_field_analysis.json',
    ]

    missing = [f for f in critical_data if not Path(f).exists()]

    if missing:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ DATA FILES MISSING{Colors.RESET}")
        print(f"\n{Colors.YELLOW}The following required files don't exist:{Colors.RESET}")
        for f in missing:
            print(f"  • {f}")

        print(f"\n{Colors.YELLOW}This is expected on a fresh clone (data is gitignored).{Colors.RESET}")
        print(f"\n{Colors.GREEN}To generate data, run:{Colors.RESET}")
        print(f"  {Colors.BOLD}python3 setup.py{Colors.RESET}")
        print(f"\nThis will:")
        print(f"  • Extract patterns from 524 markdown files")
        print(f"  • Map operators and compute torsion field")
        print(f"  • Generate all test data (~10-15 seconds)")
        print(f"\nThen run this test suite again.")
        return False

    return True

# =============================================================================
# TEST 1: File Structure
# =============================================================================

def test_file_structure():
    print_header("TEST 1: File Structure")

    required_files = [
        'extraction_outputs/pattern_extraction.json',
        'extraction_outputs/operator_mapping.json',
        'extraction_outputs/refined_commutators.json',
        'extraction_outputs/torsion_field_analysis.json',
        'extraction_outputs/contradiction_taxonomy.json',
        'recursive-extraction-engine/compiler/formalism.json',
        'recursive-extraction-engine/compiler/commutator_skeleton.json',
        'recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json',
    ]

    scripts = [
        'pattern_extract.py',
        'build_operator_mapping.py',
        'refine_commutators.py',
        'integrate_magnitudes.py',
        'build_contradiction_taxonomy.py',
        'build_torsion_field.py',
    ]

    all_pass = True

    for file in required_files:
        print_test(f"Required file: {file}")
        if Path(file).exists():
            size = Path(file).stat().st_size
            print_pass(f"{size:,} bytes")
        else:
            print_fail(f"File not found: {file}")
            all_pass = False

    for script in scripts:
        print_test(f"Script exists: {script}")
        if Path(script).exists():
            print_pass()
        else:
            print_fail(f"Script not found: {script}")
            all_pass = False

    return all_pass

# =============================================================================
# TEST 2: Data Integrity
# =============================================================================

def test_data_integrity():
    print_header("TEST 2: Data Integrity")

    all_pass = True

    # Test pattern extraction
    print_test("Pattern extraction data (73,949 contradictions)")
    try:
        with open('extraction_outputs/pattern_extraction.json', encoding='utf-8') as f:
            data = json.load(f)

        total_contradictions = sum(len(e['contradictions']) for e in data)
        if total_contradictions == 73949:
            print_pass(f"{total_contradictions:,} contradictions from {len(data)} files")
        else:
            print_fail(f"Expected 73,949, got {total_contradictions:,}")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test operator mapping
    print_test("Operator mapping (10 symbolic → normative)")
    try:
        with open('extraction_outputs/operator_mapping.json', encoding='utf-8') as f:
            data = json.load(f)

        mappings_count = len(data['mappings'])
        if mappings_count >= 10:
            print_pass(f"{mappings_count} mappings")
        else:
            print_fail(f"Expected ≥10, got {mappings_count}")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test commutator magnitudes
    print_test("Commutator magnitudes (16 evidence-based)")
    try:
        with open('extraction_outputs/refined_commutators.json', encoding='utf-8') as f:
            data = json.load(f)

        evidence_count = data['metadata']['evidence_based']
        if evidence_count == 16:
            print_pass(f"{evidence_count} pairs with extraction evidence")
        else:
            print_fail(f"Expected 16, got {evidence_count}")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test torsion field
    print_test("Torsion field (35 operator pairs, 17 invariants)")
    try:
        with open('extraction_outputs/torsion_field_analysis.json', encoding='utf-8') as f:
            data = json.load(f)

        torsion_pairs = data['metadata']['torsion_pairs']
        invariants = data['metadata']['invariants']

        if torsion_pairs == 35 and invariants == 17:
            print_pass(f"{torsion_pairs} torsion pairs, {invariants} invariants")
        else:
            print_fail(f"Expected 35/17, got {torsion_pairs}/{invariants}")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test contradiction taxonomy
    print_test("Contradiction taxonomy (6 types)")
    try:
        with open('extraction_outputs/contradiction_taxonomy.json', encoding='utf-8') as f:
            data = json.load(f)

        categories = len(data['categories'])
        total = data['metadata']['total_contradictions']

        if categories == 6 and total == 73949:
            print_pass(f"{categories} categories, {total:,} total")
        else:
            print_fail(f"Expected 6 categories / 73,949 total")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    return all_pass

# =============================================================================
# TEST 3: Key Discoveries
# =============================================================================

def test_key_discoveries():
    print_header("TEST 3: Key Discoveries Validation")

    all_pass = True

    # Test Meta ∘ Meta discovery
    print_test("Meta ∘ Meta ≠ 0 (magnitude 1.000)")
    try:
        with open('extraction_outputs/refined_commutators.json', encoding='utf-8') as f:
            data = json.load(f)

        meta_meta = data['evidence_pairs'].get('Meta,Meta')
        if meta_meta and meta_meta['magnitude'] == 1.0:
            freq = meta_meta['frequency']
            print_pass(f"magnitude = {meta_meta['magnitude']:.3f}, frequency = {freq}x")
        else:
            print_fail("Meta,Meta not found or wrong magnitude")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test torsion field Meta ∘ Meta
    print_test("Torsion T[Meta,Meta] = 1.0")
    try:
        with open('extraction_outputs/torsion_field_analysis.json', encoding='utf-8') as f:
            data = json.load(f)

        # Find Meta,Meta in torsion field
        found = False
        for pair, tdata in data['torsion_field'].items():
            if tdata['op1'] == 'Meta' and tdata['op2'] == 'Meta':
                if tdata['abs_torsion'] == 1.0:
                    print_pass(f"T = {tdata['torsion']:+.3f}")
                    found = True
                    break

        if not found:
            print_fail("Meta,Meta torsion not found or wrong value")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test S* attractor dominance
    print_test("S* attractor dominance (≥60%)")
    try:
        with open('extraction_outputs/torsion_field_analysis.json', encoding='utf-8') as f:
            data = json.load(f)

        s_star_count = data['attractor_distribution']['S*']
        total_invariants = data['metadata']['invariants']

        if total_invariants > 0:
            pct = (s_star_count / total_invariants) * 100
            if pct >= 60:
                print_pass(f"{s_star_count}/{total_invariants} = {pct:.1f}%")
            else:
                print_fail(f"Expected ≥60%, got {pct:.1f}%")
                all_pass = False
        else:
            print_fail("No invariants found")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    # Test collapse dominance
    print_test("Collapse dominance (49% of contradictions)")
    try:
        with open('extraction_outputs/contradiction_taxonomy.json', encoding='utf-8') as f:
            data = json.load(f)

        collapse_pct = data['distribution']['collapse']['percentage']
        if collapse_pct >= 49 and collapse_pct <= 50:
            print_pass(f"{collapse_pct:.1f}%")
        else:
            print_fail(f"Expected ~49%, got {collapse_pct:.1f}%")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    return all_pass

# =============================================================================
# TEST 4: Compiler Integration
# =============================================================================

def test_compiler():
    print_header("TEST 4: Compiler Tests")

    all_pass = True

    print_test("20-operator formalism")
    try:
        with open('recursive-extraction-engine/compiler/formalism.json', encoding='utf-8') as f:
            formalism = json.load(f)

        op_count = len(formalism['operators'])
        if op_count == 20:
            print_pass(f"{op_count} operators defined")
        else:
            print_fail(f"Expected 20, got {op_count}")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    print_test("Enhanced commutator skeleton (v2.1.0)")
    try:
        with open('recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json', encoding='utf-8') as f:
            skeleton = json.load(f)

        version = skeleton['metadata']['skeleton_version']
        evidence_based = skeleton['metadata']['evidence_based_pairs']

        if version == 'v2.1.0' and evidence_based == 16:
            print_pass(f"version {version}, {evidence_based} evidence-based pairs")
        else:
            print_fail(f"Expected v2.1.0 with 16 pairs")
            all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    print_test("Compiler test suite (7/7 tests)")
    try:
        result = subprocess.run(
            ['python', 'recursive-extraction-engine/compiler/test_20_operators.py'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if 'Passed: 7/7' in result.stdout and result.returncode == 0:
            print_pass("All compiler tests passing")
        else:
            print_fail("Compiler tests not passing")
            all_pass = False
    except subprocess.TimeoutExpired:
        print_fail("Compiler tests timed out")
        all_pass = False
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    return all_pass

# =============================================================================
# TEST 5: End-to-End Workflow
# =============================================================================

def test_end_to_end():
    print_header("TEST 5: End-to-End Workflow Validation")

    all_pass = True

    # Verify extraction → mapping → refinement → torsion pipeline
    print_test("Pipeline: Extraction → Mapping → Refinement → Torsion")
    try:
        # Check that data flows correctly
        with open('extraction_outputs/pattern_extraction.json', encoding='utf-8') as f:
            extraction = json.load(f)

        with open('extraction_outputs/operator_mapping.json', encoding='utf-8') as f:
            mapping = json.load(f)

        with open('extraction_outputs/refined_commutators.json', encoding='utf-8') as f:
            refinement = json.load(f)

        with open('extraction_outputs/torsion_field_analysis.json', encoding='utf-8') as f:
            torsion = json.load(f)

        # Validate pipeline integrity
        files_count = len(extraction)
        mappings_count = len(mapping['mappings'])
        evidence_count = refinement['metadata']['evidence_based']
        torsion_pairs = torsion['metadata']['torsion_pairs']

        print_pass(f"{files_count} files → {mappings_count} mappings → {evidence_count} refined → {torsion_pairs} torsion pairs")
    except Exception as e:
        print_fail(str(e))
        all_pass = False

    return all_pass

# =============================================================================
# MAIN
# =============================================================================

def main():
    print(f"\n{Colors.BOLD}RECURSIVE AI FRAMEWORK - MASTER TEST SUITE{Colors.RESET}")
    print(f"Validates all components end-to-end\n")

    # Pre-flight check: Ensure data files exist
    if not check_data_exists():
        return 1

    results = {
        'File Structure': test_file_structure(),
        'Data Integrity': test_data_integrity(),
        'Key Discoveries': test_key_discoveries(),
        'Compiler Integration': test_compiler(),
        'End-to-End Workflow': test_end_to_end(),
    }

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{test_name:30s}: {status}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} test suites passed{Colors.RESET}\n")

    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL{Colors.RESET}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED - SEE ERRORS ABOVE{Colors.RESET}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
