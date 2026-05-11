"""
run_all_experiments.py
----------------------
Runs all 8 bounded computational experiments for MIT-CrowdMath-2026
in the correct dependency order.

Usage:
    python run_all_experiments.py

Requirements:
    Python 3.11+. No external packages.

Estimated runtime:
    exp_001 – exp_005, exp_008 : < 5 seconds each
    exp_006                    : ~4 minutes
    exp_007                    : ~3 minutes
    Total                      : ~8–10 minutes

Outputs are written to experiments/results/.
Each experiment overwrites its previous output.
"""

import subprocess
import sys
import time
from pathlib import Path


EXPERIMENTS = [
    ("exp_001", "experiments/exp_001_generate_semiring_elements.py",    "fast"),
    ("exp_005", "experiments/exp_005_candidate_atom_detection.py",       "fast"),
    ("exp_004", "experiments/exp_004_bounded_factorization_search.py",   "fast"),
    ("exp_002", "experiments/exp_002_detect_units_in_bounded_samples.py","fast"),
    ("exp_003", "experiments/exp_003_group_associate_classes.py",        "fast"),
    ("exp_008", "experiments/exp_008_valuation_patterns.py",            "fast"),
    ("exp_006", "experiments/exp_006_candidate_atomic_divisors.py",      "slow (~4 min)"),
    ("exp_007", "experiments/exp_007_idf_sanity_checks.py",             "slow (~3 min)"),
]


def separator(char: str = "-", width: int = 60) -> str:
    return char * width


def run_experiments() -> int:
    repo_root = Path(__file__).resolve().parent
    python = sys.executable

    print()
    print(separator("="))
    print("  MIT-CrowdMath-2026 -- Experiment Runner")
    print(separator("="))
    print()
    print("  WARNING: Bounded computational evidence only.")
    print("  Results do not prove properties of infinite monoids.")
    print()
    print(f"  Repository root : {repo_root}")
    print(f"  Python          : {python}")
    print(f"  Experiments     : {len(EXPERIMENTS)}")
    print()
    print(separator())
    print()

    results: list[tuple[str, str, float]] = []
    failed: list[str] = []

    for label, script_path, speed in EXPERIMENTS:
        script = repo_root / script_path
        if not script.exists():
            print(f"  ✗ {label}  MISSING: {script_path}")
            results.append((label, "MISSING", 0.0))
            failed.append(label)
            continue

        speed_note = f"  [{speed}]" if "slow" in speed else ""
        print(f"  -> Running {label}{speed_note}")

        t0 = time.monotonic()
        proc = subprocess.run(
            [python, str(script)],
            cwd=str(repo_root),
            capture_output=False,
        )
        elapsed = time.monotonic() - t0

        if proc.returncode == 0:
            status = "pass"
            mark = "PASS"
        else:
            status = "FAIL"
            mark = "FAIL"
            failed.append(label)

        results.append((label, status, elapsed))
        print(f"  [{mark}] {label}  {status}  ({elapsed:.1f}s)")
        print()

    print(separator())
    print()
    print("  Summary")
    print()
    passed = sum(1 for _, s, _ in results if s == "pass")
    total = len(results)

    for label, status, elapsed in results:
        mark = "PASS" if status == "pass" else "FAIL"
        print(f"    [{mark}]  {label:<10}  {status:<8}  {elapsed:6.1f}s")

    print()
    print(f"  {passed}/{total} experiments passed.")

    if failed:
        print()
        print(f"  FAILED: {', '.join(failed)}")
        print()
        return 1

    print()
    print("  All experiments passed. Outputs written to experiments/results/.")
    print()
    print(separator("═"))
    return 0


if __name__ == "__main__":
    sys.exit(run_experiments())
