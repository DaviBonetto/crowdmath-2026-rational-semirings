import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.semirings import generate_n0_q
from crowdmath2026.units import theoretical_units_n0q
from crowdmath2026.associates import (
    canonical_representative,
    group_associate_classes,
)
from crowdmath2026.atomic_divisors import (
    classify_candidate_multiplicative_atoms,
    candidate_atomic_divisors,
    group_divisors_by_associate_class,
)
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_006_outputs"

BOUNDED_WARNING = (
    "This is a bounded computational sample. It does not prove the complete "
    "atomic divisor structure of the infinite monoid."
)

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
    """Select target elements for atomic divisor analysis.

    Strategy (priority order):
    1. The universal multiplicative identity value (1+q+q^2)(1+q^3) if in sample.
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
            lhs = Fraction(1) + q + q**2 + q**3
            rhs = Fraction(1) + q + q**2
            # (1+q+q^2)(1+q^3) and (1+q^2+q^4)(1+q) — pick the first
            val1 = (Fraction(1) + q + q**2) * (Fraction(1) + q**3)
            val2 = (Fraction(1) + q**2 + q**4) * (Fraction(1) + q)
            for v in (val1, val2):
                if v in nonzero_sample and v not in seen:
                    targets.append(v)
                    seen.add(v)
        except (OverflowError, ZeroDivisionError):
            pass

    # 2. Products of pairs of two smallest candidate atoms
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

    targets = _select_targets(q, nonzero_sample, candidate_atoms, sample_units, MAX_TARGETS_PER_Q)

    label = fraction_to_str(q).replace("/", "_")
    case_label = _theoretical_case_label(q)

    csv_rows: list[dict[str, str]] = []
    json_targets: list[dict[str, object]] = []

    max_div_count = 0
    max_assoc_count = 0

    for target in targets:
        divisors_map = candidate_atomic_divisors(target, candidate_atoms, nonzero_sample)
        div_set: set[Fraction] = set(divisors_map.keys())

        assoc_classes = group_divisors_by_associate_class(div_set, sample_units, nonzero_sample)
        div_count = len(div_set)
        assoc_count = len(assoc_classes)

        max_div_count = max(max_div_count, div_count)
        max_assoc_count = max(max_assoc_count, assoc_count)

        sorted_divs = sorted(div_set, key=fraction_sort_key)
        sorted_quots = [fraction_to_str(divisors_map[a]) for a in sorted_divs]

        notes = BOUNDED_WARNING
        if div_count == 0:
            notes = (
                BOUNDED_WARNING + " No candidate atomic divisors found within the bounded sample."
            )

        csv_rows.append(
            {
                "q": fraction_to_str(q),
                "target": fraction_to_str(target),
                "target_decimal_approx": f"{float(target):.8f}",
                "candidate_atomic_divisor_count": str(div_count),
                "associate_class_count": str(assoc_count),
                "sample_divisors": "; ".join(fraction_to_str(a) for a in sorted_divs),
                "sample_quotients": "; ".join(sorted_quots),
                "notes": notes,
            }
        )

        json_targets.append(
            {
                "target": fraction_to_str(target),
                "candidate_atomic_divisors": [fraction_to_str(a) for a in sorted_divs],
                "quotient_witnesses": {fraction_to_str(a): fraction_to_str(divisors_map[a]) for a in sorted_divs},
                "associate_classes": [
                    sorted([fraction_to_str(el) for el in cls], key=lambda s: float(Fraction(s)))
                    for cls in assoc_classes
                ],
                "candidate_atomic_divisor_count": div_count,
                "associate_class_count": assoc_count,
            }
        )

    csv_path = OUTPUT_DIR / f"n0q_q_{label}_candidate_atomic_divisors.csv"
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
        "bounded_warning": BOUNDED_WARNING,
        "sample_summary": {
            "nonzero_sample_elements": len(nonzero_sample),
            "sample_units_used": len(sample_units),
            "candidate_multiplicative_atoms": len(candidate_atoms),
        },
        "targets": json_targets,
    }

    json_path = OUTPUT_DIR / f"n0q_q_{label}_candidate_atomic_divisors.json"
    write_json(json_path, json_data)

    # Row for summary table
    if _theoretical_case_label(q) == "integer":
        interp_short = f"q={fraction_to_str(q)}: integer; divisors align with prime factorization."
    elif _theoretical_case_label(q) == "reciprocal_integer":
        interp_short = (
            f"q={fraction_to_str(q)}: nontrivial units reduce associate-class count."
        )
    else:
        interp_short = (
            f"q={fraction_to_str(q)}: only unit 1; divisor classes are singletons."
        )

    return {
        "q": fraction_to_str(q),
        "nonzero_elements": len(nonzero_sample),
        "sample_units": len(sample_units),
        "candidate_atoms": len(candidate_atoms),
        "targets_tested": len(targets),
        "max_divisor_count": max_div_count,
        "max_assoc_class_count": max_assoc_count,
        "interpretation": interp_short,
    }


def build_summary_markdown(results: list[dict[str, object]]) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        r"This experiment searches for **candidate atomic divisors** of selected target elements "
        r"in bounded samples of $S_q = \mathbb{N}_0[q]\setminus\{0\}$ "
        "under multiplication. "
        r"An element $a \in S_q$ is a **candidate multiplicative atom** if it is a nonunit "
        r"with no nontrivial multiplicative factorization within the bounded sample. "
        r"A **candidate atomic divisor** of a target $x$ is a candidate atom $a$ such that "
        r"$x/a$ also lies in the sample. "
        "Candidate atomic divisors are grouped up to sample associate classes. "
        "This experiment prepares for Experiment 007 (IDF sanity checks)."
    )

    sections.append(
        "## Bounded Warning\n\n"
        "> **" + BOUNDED_WARNING + "**\n\n"
        "Bounded samples may miss atomic divisors whose quotient lies outside the generated "
        "sample. Candidate atoms are not proven atoms: a factorization may exist outside the "
        "bounded search range."
    )

    sections.append(
        "## Parameters\n\n"
        f"- `max_degree = {MAX_DEGREE}`\n"
        f"- `max_coeff = {MAX_COEFF}`\n"
        f"- `max_abs_unit_exponent = {MAX_ABS_UNIT_EXPONENT}`\n"
        f"- `max_targets_per_q = {MAX_TARGETS_PER_Q}`\n"
        "- Sample generated by `generate_n0_q(q, max_degree, max_coeff)` from `semirings.py`\n"
        "- Units from `theoretical_units_n0q(q, max_abs_unit_exponent)` restricted to sample\n"
        "- Associate grouping via `group_associate_classes` from `associates.py`\n"
        "- q values tested: " + ", ".join(str(r["q"]) for r in results)
    )

    table_rows = [
        "| q | Nonzero elements | Sample units | Candidate atoms | Targets | Max divisors | Max assoc classes | Interpretation |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for res in results:
        table_rows.append(
            f"| {res['q']} | {res['nonzero_elements']} | {res['sample_units']} "
            f"| {res['candidate_atoms']} | {res['targets_tested']} "
            f"| {res['max_divisor_count']} | {res['max_assoc_class_count']} "
            f"| {res['interpretation']} |"
        )
    sections.append("## Results Table\n\n" + "\n".join(table_rows))

    sections.append(
        "## Interpretation\n\n"
        "This experiment prepares for IDF sanity checks by building the candidate atomic "
        "divisor picture for each $q$ case.\n\n"
        r"**Atomic divisors must be counted up to associates.** "
        "If two candidate atoms $a$ and $b$ are associates (i.e. $a = ub$ for a sample unit $u$), "
        "they count as one divisor in factorization length sets.\n\n"
        r"**q = 1/2 and q = 1/6:** Nontrivial units merge visible divisors into fewer associate "
        "classes. The number of associate classes of atomic divisors may be strictly smaller "
        "than the raw count of candidate atoms dividing a target.\n\n"
        r"**q = a/b with a, b > 1:** Theory (Exercise 1.7) predicts only unit $1$. "
        "Divisor associate classes are singleton in the bounded sample.\n\n"
        "**Candidate atoms are not proven atoms.** "
        "A bounded sample candidate atom may fail to be a true atom if a multiplicative "
        "factorization exists outside the sample.\n\n"
        "**Bounded samples may miss divisors** whose quotient requires elements outside "
        "the generated sample."
    )

    sections.append(
        "## Next Experiment\n\n"
        "- `exp_007_idf_sanity_checks.py` — IDF sanity checks using candidate atomic divisors."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 006 — Candidate Atomic Divisors",
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
    print("Experiment 006 complete.")
    print(f"  Output directory      : {OUTPUT_DIR}")
    print(f"  N0[q]^bullet cases    : {len(results)}")
    print(f"  CSV files             : {len(csv_files)}")
    print(f"  JSON files            : {len(json_files)}")
    print(f"  summary.md            : {'yes' if summary_exists else 'MISSING'}")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  Candidate atomic divisors are sample-based and do not prove IDF behavior.")
    print("")


if __name__ == "__main__":
    main()
