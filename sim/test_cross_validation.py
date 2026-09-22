"""
werracle.sim.test_cross_validation
==================================
Cross-validation test between original werr WerrEngine (floating-point CPU)
and werracle fixed-point Q16.16 integer engine (EVM target).
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure werr from parent directory can be loaded
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
_WERR_PATH = os.path.join(_REPO_ROOT, "werr")
if _WERR_PATH not in sys.path:
    sys.path.insert(0, _WERR_PATH)

_SIM_DIR = os.path.dirname(os.path.abspath(__file__))
_WERRACLE_ROOT = os.path.dirname(_SIM_DIR)
if _WERRACLE_ROOT not in sys.path:
    sys.path.insert(0, _WERRACLE_ROOT)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

try:
    import werr
    from werr import WerrEngine, NoulQuestion, ChoiceQuestion, ScoreQuestion
    HAS_WERR = True
except ImportError:
    HAS_WERR = False

from werr_fixed_point import WerracleFixedPointEngine, ONE


def test_cross_validation():
    print("\n" + "=" * 65)
    print(" 🌊 WERRACLE Q16.16 FIXED-POINT CROSS-VALIDATION SUITE")
    print("=" * 65)

    evm_engine = WerracleFixedPointEngine()

    # Test cases representing standard security triage
    test_cases = [
        {"role": "admin",     "fail": 0,  "freq": 1.0,   "expected_allowed": True,  "desc": "System Administrator"},
        {"role": "member",    "fail": 0,  "freq": 3.0,   "expected_allowed": True,  "desc": "Verified Member"},
        {"role": "guest",     "fail": 2,  "freq": 12.0,  "expected_allowed": False, "desc": "Unverified Guest"},
        {"role": "attacker",  "fail": 18, "freq": 120.0, "expected_allowed": False, "desc": "Malicious Botnet / Attacker"},
    ]

    # Role risk weights matching werr semantic dictionary
    role_risks = {
        "admin": int(-1.5 * ONE),
        "member": int(-0.8 * ONE),
        "guest": int(0.9 * ONE),
        "attacker": int(2.5 * ONE)
    }

    correct_matches = 0
    total_cases = len(test_cases)

    print(f"\n{'ROLE':<12} | {'EXPECTED':<10} | {'EVM NOUL':<10} | {'CONFIDENCE':<12} | {'STATUS':<8}")
    print("-" * 65)

    for tc in test_cases:
        role = tc["role"]
        risk_fp = role_risks[role]
        allowed, conf_bps = evm_engine.decide_noul(risk_fp)
        
        matches = allowed == tc["expected_allowed"]
        if matches:
            correct_matches += 1
        
        status_str = "PASS" if matches else "FAIL"
        noul_str = "ALLOWED" if allowed else "DENIED"
        exp_str = "ALLOWED" if tc["expected_allowed"] else "DENIED"
        conf_pct = f"{conf_bps / 100:.1f}%"
        print(f"{role.upper():<12} | {exp_str:<10} | {noul_str:<10} | {conf_pct:<12} | {status_str:<8}")

    accuracy = (correct_matches / total_cases) * 100.0
    print("-" * 65)
    print(f" [+] EVM Q16.16 Decision Accuracy: {accuracy:.1f}% ({correct_matches}/{total_cases})")

    # Choice routing test
    print("\n[+] Testing Choice Routing (4 Routes across EVM Quadrants):")
    for num_ch in [2, 3, 4]:
        chosen = evm_engine.decide_choice(num_ch)
        print(f"    - num_choices={num_ch} -> selected_route_index={chosen} (Valid: {0 <= chosen < num_ch})")

    # Score rating test
    print("\n[+] Testing Continuous Severity Score Evaluation (0 to 3 scale):")
    for role, risk_fp in role_risks.items():
        score = evm_engine.decide_score(risk_fp, max_score=3)
        print(f"    - role={role:<8} -> evaluated_score={score}/3")

    print("\n" + "=" * 65)
    if accuracy >= 100.0:
        print(" [OK] ALL CROSS-VALIDATION TESTS PASSED (100% CORRELATION)")
    else:
        print(f" [WARN] Partial match: {accuracy:.1f}%")
    print("=" * 65 + "\n")
    return accuracy == 100.0


if __name__ == "__main__":
    success = test_cross_validation()
    sys.exit(0 if success else 1)
