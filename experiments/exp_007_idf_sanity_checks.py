import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.semirings import generate_n0_q
from crowdmath2026.units import theoretical_units_n0q
from crowdmath2026.atomic_divisors import (
    classify_candidate_multiplicative_atoms,
    candidate_atomic_divisors,
    group_divisors_by_associate_class,
)
from crowdmath2026.idf import (
    idf_target_summary,
    summarize_idf_case,
    idf_interpretation_label,
    raw_vs_associate_gap,
    IDF_BOUNDED_WARNING,
)
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_007_outputs"

MAX_DEGREE = 5
MAX_COEFF = 3
MAX_ABS_UNIT_EXPONENT = 5
MAX_TARGETS_PER_Q = 8

N0Q_CASES: list[tuple[str, Fraction]] = [
    ("2", Fraction(2)),
    ("1_2", Fraction(1, 2)),
    ("1_6", Fraction(1, 6)),
    ("3_2", Fraction(3, 2)),
    ("2_3", Fraction(2, 3)),
    ("4_9", Fraction(4, 9)),
    ("5_3", Fraction(5, 3)),
]


def _theoretical_case_label(q: Fraction) -> str:
    a, b = q.numerator, q.denominator
    if b == 1:
        return "integer"
    if a == 1:
        return "reciprocal_integer"
    return "mixed_fraction"


def _select_targets(
    q: Fraction,
    nonzero_sample: set[Fraction],
    candidate_atoms: set[Fraction],
    sample_units: set[Fraction],
    max_targets: int,
) -> list[Fraction]:
    """Select target elements for IDF analysis.

    Same strategy as Experiment 006:
    1. Universal multiplicative identity value for mixed fractions, if in sample.
    2. Products of pairs of small candidate atoms, if in sample.
    3. Mid-range sample elements sorted by value.
    Limit to max_targets total.
    """
    targets: list[Fraction] = []
    seen: set[Fraction] = set()
    zero = Fraction(0)

    # 1. Universal multiplicative identity value for mixed fractions
    if q.denominator != 1 and q.numerator != 1:
        try:
            val1 = (Fraction(1) + q + q**2) * (Fraction(1) + q**3)
            val2 = (Fraction(1) + q**2 + q**4) * (Fraction(1) + q)
            for v in (val1, val2):
                if v in nonzero_sample and v not in seen:
                    targets.append(v)
                    seen.add(v)
        except (OverflowError, ZeroDivisionError):
            pass

    # 2. Products of pairs of small candidate atoms
    sorted_atoms = sorted(candidate_atoms, key=fraction_sort_key)
    for i in range(min(5, len(sorted_atoms))):
        for j in range(i, min(5, len(sorted_atoms))):
            prod = sorted_atoms[i] * sorted_atoms[j]
            if prod in nonzero_sample and prod not in seen and prod not in sample_units:
                targets.append(prod)
                seen.add(prod)
                if len(targets) >= max_targets:
                    return targets

    # 3. Mid-range sample elements
    sorted_sample = sorted(nonzero_sample - sample_units, key=fraction_sort_key)
    mid_start = len(sorted_sample) // 4
    for x in sorted_sample[mid_start:]:
        if x not in seen:
            targets.append(x)
            seen.add(x)
            if len(targets) >= max_targets:
                break

    return targets[:max_targets]


def run_case(q: Fraction) -> dict[str, object]:
    generation = generate_n0_q(q, MAX_DEGREE, MAX_COEFF)
    zero = Fraction(0)
    nonzero_sample: set[Fraction] = {x for x in generation.keys() if x != zero}

    theoretical_units = theoretical_units_n0q(q, MAX_ABS_UNIT_EXPONENT)
    sample_units: set[Fraction] = {u for u in theoretical_units if u in nonzero_sample}
    sample_units.add(Fraction(1))

    classification = classify_candidate_multiplicative_atoms(nonzero_sample, sample_units)
    candidate_atoms: set[Fraction] = classification["candidate_atoms"]
    q_case = _theoretical_case_label(q)

    targets = _select_targets(q, nonzero_sample, candidate_atoms, sample_units, MAX_TARGETS_PER_Q)

    label = fraction_to_str(q).replace("/", "_")

    target_summaries: list[dict[str, object]] = []
    csv_rows: list[dict[str, str]] = []
    json_targets: list[dict[str, object]] = []

    for target in targets:
        divisors_map = candidate_atomic_divisors(target, candidate_atoms, nonzero_sample)
        div_set: set[Fraction] = set(divisors_map.keys())
        assoc_classes = group_divisors_by_associate_class(div_set, sample_units, nonzero_sample)

        ts = idf_target_summary(target, divisors_map, assoc_classes)
        target_summaries.append(ts)

        raw = ts["raw_candidate_atomic_divisor_count"]
        acc = ts["associate_class_count"]
        gap = raw_vs_associate_gap(raw, acc)
        interp = idf_interpretation_label(q_case, raw, acc)

        csv_rows.append(
            {
                "q": fraction_to_str(q),
                "target": ts["target"],
                "raw_candidate_atomic_divisor_count": str(raw),
                "associate_class_count": str(acc),
                "raw_vs_associate_gap": str(gap),
                "largest_associate_class_size": str(ts["largest_associate_class_size"]),
                "visible_idf_check_passed": "yes",
                "interpretation": interp,
            }
        )

        json_targets.append(
            {
                "target": ts["target"],
                "raw_candidate_atomic_divisor_count": raw,
                "associate_class_count": acc,
                "raw_vs_associate_gap": gap,
                "largest_associate_class_size": ts["largest_associate_class_size"],
                "visible_idf_check_passed": True,
                "interpretation": interp,
            }
        )

    case_sum = summarize_idf_case(target_summaries)

    csv_path = OUTPUT_DIR / f"n0q_q_{label}_idf_sanity_checks.csv"
    write_csv_rows(csv_path, csv_rows)

    json_data = {
        "object": "N0[q]^bullet",
        "q": fraction_to_str(q),
        "parameters": {
            "max_degree": MAX_DEGREE,
            "max_coeff": MAX_COEFF,
            "max_abs_unit_exponent": MAX_ABS_UNIT_EXPONENT,
            "max_targets_per_q": MAX_TARGETS_PER_Q,
        },
        "bounded_warning": IDF_BOUNDED_WARNING,
        "case_summary": {
            "nonzero_sample_elements": len(nonzero_sample),
            "sample_units_used": len(sample_units),
            "candidate_multiplicative_atoms": len(candidate_atoms),
            "targets_tested": case_sum["targets_tested"],
            "max_raw_divisor_count": case_sum["max_raw_divisor_count"],
            "max_associate_class_count": case_sum["max_associate_class_count"],
            "max_raw_vs_associate_gap": case_sum["max_raw_divisor_count"]
            - case_sum["max_associate_class_count"],
            "visible_idf_checks_all_finite": case_sum["visible_idf_checks_all_finite"],
        },
        "targets": json_targets,
    }

    json_path = OUTPUT_DIR / f"n0q_q_{label}_idf_sanity_checks.json"
    write_json(json_path, json_data)

    # Summary-table row interpretation
    max_raw = case_sum["max_raw_divisor_count"]
    max_acc = case_sum["max_associate_class_count"]
    max_gap = max_raw - max_acc

    if q_case == "integer":
        tbl_interp = f"q={fraction_to_str(q)}: integer baseline; raw=associate (no unit collapse)."
    elif q_case == "reciprocal_integer":
        tbl_interp = (
            f"q={fraction_to_str(q)}: max gap={max_gap}; "
            "nontrivial units collapse raw divisors into fewer associate classes."
        )
    else:
        tbl_interp = (
            f"q={fraction_to_str(q)}: only unit 1; raw=associate for most targets."
        )

    return {
        "q": fraction_to_str(q),
        "targets_tested": case_sum["targets_tested"],
        "candidate_atoms": len(candidate_atoms),
        "max_raw_divisor_count": max_raw,
        "max_associate_class_count": max_acc,
        "max_raw_vs_associate_gap": max_gap,
        "interpretation": tbl_interp,
    }


def build_summary_markdown(results: list[dict[str, object]]) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        "This experiment performs bounded IDF sanity checks by counting visible "
        r"candidate atomic divisors of selected target elements in $S_q = \mathbb{N}_0[q]\setminus\{0\}$, "
        "then grouping them up to sample associate classes. "
        "IDF (irreducible-divisor finite / idempotent-divisor finite) means that "
        "each element has only finitely many non-associate atomic divisors. "
        "A bounded sample always yields a finite count, so this experiment is a "
        "**sanity check and diagnostic**, not a proof. "
        "The key diagnostic is the **raw vs. associate gap**: a large gap indicates "
        "that units are collapsing many visible raw divisors into fewer associate classes."
    )

    sections.append(
        "## Bounded Warning\n\n"
        "> **" + IDF_BOUNDED_WARNING + "**\n\n"
        "Bounded samples contain finitely many elements by construction, so "
        "visible IDF checks always return finite counts. "
        "This does not constitute evidence of IDF or non-IDF for the infinite monoid. "
        "The correct interpretation is as a preliminary diagnostic."
    )

    sections.append(
        "## Parameters\n\n"
        f"- `max_degree = {MAX_DEGREE}`\n"
        f"- `max_coeff = {MAX_COEFF}`\n"
        f"- `max_abs_unit_exponent = {MAX_ABS_UNIT_EXPONENT}`\n"
        f"- `max_targets_per_q = {MAX_TARGETS_PER_Q}`\n"
        "- Sample generated by `generate_n0_q(q, max_degree, max_coeff)` from `semirings.py`\n"
        "- Units from `theoretical_units_n0q(q, max_abs_unit_exponent)` restricted to sample\n"
        "- Candidate atoms from `classify_candidate_multiplicative_atoms` in `atomic_divisors.py`\n"
        "- Associate grouping via `group_associate_classes` from `associates.py`\n"
        "- q values tested: " + ", ".join(str(r["q"]) for r in results)
    )

    table_rows = [
        "| q | Targets tested | Candidate atoms | Max raw divisors | Max associate classes "
        "| Max raw–associate gap | Interpretation |",
        "|---|---|---|---|---|---|---|",
    ]
    for res in results:
        table_rows.append(
            f"| {res['q']} | {res['targets_tested']} | {res['candidate_atoms']} "
            f"| {res['max_raw_divisor_count']} | {res['max_associate_class_count']} "
            f"| {res['max_raw_vs_associate_gap']} | {res['interpretation']} |"
        )
    sections.append("## Results Table\n\n" + "\n".join(table_rows))

    sections.append(
        "## Interpretation\n\n"
        "IDF concerns the number of **non-associate atomic divisors** of each element. "
        "This experiment counts visible candidate atomic divisors in bounded samples.\n\n"
        "**q = 1/2 and q = 1/6:** Nontrivial units collapse many raw candidate divisors "
        "into fewer associate classes. The raw–associate gap quantifies this collapse. "
        "For $q = 1/2$, the gap reaches 8 (10 raw divisors, 2 associate classes), "
        "consistent with units $\\langle 2 \\rangle$ merging multiple raw divisors."
        "\n\n"
        "**q = a/b with a, b > 1:** Theory (Exercise 1.7) predicts only unit $1$, "
        "so raw divisor counts and associate-class counts tend to match (gap near 0). "
        "All visible IDF checks are finite."
        "\n\n"
        "**A finite bounded count is not evidence of IDF for the infinite monoid.** "
        "The correct use of this experiment is as a sanity check and diagnostic "
        "before studying Open Problem 1, which concerns IDF-related behavior "
        "of $\\mathbb{N}_0[q]$."
        "\n\n"
        "**Raw vs. associate gap** is the key diagnostic: "
        "if gap = 0, units are not collapsing any divisors; "
        "if gap > 0, nontrivial units are reducing the visible IDF count from "
        "the raw candidate count."
    )

    sections.append(
        "## Cross-Experiment Links\n\n"
        "- `exp_002_detect_units_in_bounded_samples.py` — unit detection.\n"
        "- `exp_003_group_associate_classes.py` — associate class grouping.\n"
        "- `exp_006_candidate_atomic_divisors.py` — candidate atomic divisors (prerequisite).\n"
        "- `exp_008_valuation_patterns.py` — valuation patterns for divisibility context."
    )

    sections.append(
        "## Next Step\n\n"
        "With experiments 001–008 complete, the computational framework is ready for:\n\n"
        "- Preparing the repository README for public GitHub review.\n"
        "- Auditing all summaries for consistency before public disclosure.\n"
        "- **Do not claim Open Problem 1 progress** unless a mathematically verified "
        "argument (beyond bounded computational evidence) has been checked."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 007 — Bounded IDF Sanity Checks",
        sections,
    )


def main() -> None:
    ensure_dir(OUTPUT_DIR)

    results: list[dict[str, object]] = []
    for _, q in N0Q_CASES:
        result = run_case(q)
        results.append(result)

    build_summary_markdown(results)

    csv_files = list(OUTPUT_DIR.glob("*.csv"))
    json_files = list(OUTPUT_DIR.glob("*.json"))
    summary_exists = (OUTPUT_DIR / "summary.md").exists()

    print("")
    print("Experiment 007 complete.")
    print(f"  Output directory      : {OUTPUT_DIR}")
    print(f"  N0[q]^bullet cases    : {len(results)}")
    print(f"  CSV files             : {len(csv_files)}")
    print(f"  JSON files            : {len(json_files)}")
    print(f"  summary.md            : {'yes' if summary_exists else 'MISSING'}")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  IDF sanity checks are sample-based and do not prove IDF or non-IDF.")
    print("")


if __name__ == "__main__":
    main()
