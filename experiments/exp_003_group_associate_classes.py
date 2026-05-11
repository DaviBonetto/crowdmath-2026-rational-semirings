import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.semirings import generate_n0_q
from crowdmath2026.units import theoretical_units_n0q
from crowdmath2026.associates import (
    group_associate_classes,
    canonical_representative,
    class_summary,
)
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_003_outputs"

BOUNDED_WARNING = (
    "This is a bounded computational sample. It does not prove the complete "
    "associate-class structure of the infinite monoid."
)

MAX_DEGREE = 5
MAX_COEFF = 3
MAX_ABS_UNIT_EXPONENT = 5

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


def _interpretation(q: Fraction, summary: dict[str, int], units_used: int) -> str:
    q_str = fraction_to_str(q)
    nc = summary["num_classes"]
    ns = summary["singleton_classes"]
    nn = summary["non_singleton_classes"]
    lc = summary["largest_class_size"]
    case = _theoretical_case_label(q)

    if case == "integer":
        return (
            f"q={q_str}: only unit is 1, so all {nc} sample associate classes are singletons. "
            "Consistent with UFM behavior of N0."
        )
    if case == "reciprocal_integer":
        return (
            f"q={q_str}: {units_used} sample unit(s) used. "
            f"Found {nc} associate class(es): {ns} singleton(s), {nn} non-singleton(s), "
            f"largest class size {lc}. "
            "Non-singleton classes arise from unit multiples within the bounded sample."
        )
    return (
        f"q={q_str}: only unit is 1 by Exercise 1.7, so all {nc} sample associate classes "
        "are singletons. Consistent with mixed-fraction multiplicative structure."
    )


def run_case(q: Fraction) -> dict[str, object]:
    generation = generate_n0_q(q, MAX_DEGREE, MAX_COEFF)
    zero = Fraction(0)
    nonzero_sample: set[Fraction] = {x for x in generation.keys() if x != zero}

    theoretical_units = theoretical_units_n0q(q, MAX_ABS_UNIT_EXPONENT)
    # Restrict to units present in the sample
    sample_units: set[Fraction] = {u for u in theoretical_units if u in nonzero_sample}
    # Always include 1 as a unit
    sample_units.add(Fraction(1))

    classes = group_associate_classes(nonzero_sample, sample_units)
    summary = class_summary(classes)

    label = fraction_to_str(q).replace("/", "_")
    case_label = _theoretical_case_label(q)
    interp = _interpretation(q, summary, len(sample_units))

    sorted_units = sorted(sample_units, key=fraction_sort_key)

    # CSV: one row per class
    csv_rows: list[dict[str, str]] = []
    for idx, cls in enumerate(classes):
        rep = canonical_representative(cls)
        elements_sorted = sorted(cls, key=fraction_sort_key)
        units_used_for_class: set[Fraction] = set()
        for el in elements_sorted:
            for u in sample_units:
                if u * rep == el and el != rep:
                    units_used_for_class.add(u)
                elif u * el == rep and el != rep:
                    units_used_for_class.add(u)
        if not units_used_for_class and len(cls) == 1:
            units_used_for_class = {Fraction(1)}

        notes = BOUNDED_WARNING if len(cls) == 1 else (
            BOUNDED_WARNING + " Non-singleton class: elements are associates within the sample."
        )

        csv_rows.append(
            {
                "class_id": str(idx + 1),
                "representative": fraction_to_str(rep),
                "class_size": str(len(cls)),
                "elements": "; ".join(fraction_to_str(e) for e in elements_sorted),
                "units_used": "; ".join(fraction_to_str(u) for u in sorted(units_used_for_class, key=fraction_sort_key)),
                "theoretical_case": case_label,
                "notes": notes,
            }
        )

    csv_path = OUTPUT_DIR / f"n0q_q_{label}_associate_classes.csv"
    write_csv_rows(csv_path, csv_rows)

    # JSON
    json_classes = []
    for idx, cls in enumerate(classes):
        rep = canonical_representative(cls)
        elements_sorted = sorted(cls, key=fraction_sort_key)
        json_classes.append(
            {
                "class_id": idx + 1,
                "representative": fraction_to_str(rep),
                "class_size": len(cls),
                "elements": [fraction_to_str(e) for e in elements_sorted],
            }
        )

    json_data = {
        "object": "N0[q]^bullet",
        "q": fraction_to_str(q),
        "parameters": {
            "max_degree": MAX_DEGREE,
            "max_coeff": MAX_COEFF,
            "max_abs_unit_exponent": MAX_ABS_UNIT_EXPONENT,
        },
        "bounded_warning": BOUNDED_WARNING,
        "units_used": [fraction_to_str(u) for u in sorted_units],
        "summary": {
            "total_nonzero_sample_elements": len(nonzero_sample),
            "sample_units_used": len(sample_units),
            "num_associate_classes": summary["num_classes"],
            "singleton_classes": summary["singleton_classes"],
            "non_singleton_classes": summary["non_singleton_classes"],
            "largest_class_size": summary["largest_class_size"],
        },
        "classes": json_classes,
    }

    json_path = OUTPUT_DIR / f"n0q_q_{label}_associate_classes.json"
    write_json(json_path, json_data)

    return {
        "q": fraction_to_str(q),
        "nonzero_elements": len(nonzero_sample),
        "units_used": len(sample_units),
        "num_classes": summary["num_classes"],
        "singleton_classes": summary["singleton_classes"],
        "non_singleton_classes": summary["non_singleton_classes"],
        "largest_class_size": summary["largest_class_size"],
        "interpretation": interp,
    }


def build_summary_markdown(results: list[dict[str, object]]) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        r"This experiment groups bounded sample elements of $(\mathbb{N}_0[q]\setminus\{0\}, \cdot)$ "
        "into **sample associate classes** using units detected from Experiment 002. "
        r"Two nonzero elements $a, b$ are associates if there exists a unit $u$ such that $a = ub$. "
        "The experiment uses units from `theoretical_units_n0q` restricted to those present in the "
        "sample, then partitions via BFS. This supports Exercise 1.7 and prepares for IDF analysis, "
        "where factorizations are always considered up to associates."
    )

    sections.append(
        "## Bounded Warning\n\n"
        "> **" + BOUNDED_WARNING + "**\n\n"
        "Bounded samples may split a true infinite associate class into smaller visible classes "
        "if some unit multiples lie outside the generated sample."
    )

    sections.append(
        "## Parameters\n\n"
        f"- `max_degree = {MAX_DEGREE}`\n"
        f"- `max_coeff = {MAX_COEFF}`\n"
        f"- `max_abs_unit_exponent = {MAX_ABS_UNIT_EXPONENT}`\n"
        "- Sample generated by `generate_n0_q(q, max_degree, max_coeff)` from `semirings.py`\n"
        "- Units from `theoretical_units_n0q(q, max_abs_unit_exponent)` restricted to sample\n"
        "- q values tested: " + ", ".join(str(r["q"]) for r in results)
    )

    table_rows = [
        "| q | Nonzero elements | Units used | Associate classes | Singleton | Non-singleton "
        "| Largest class | Interpretation |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for res in results:
        q_val = res["q"]
        a, b = Fraction(q_val).numerator, Fraction(q_val).denominator
        if b == 1:
            interp_short = f"q={q_val}: all singletons (only unit is 1)."
        elif a == 1:
            interp_short = f"q={q_val}: non-singleton classes from nontrivial units."
        else:
            interp_short = f"q={q_val}: all singletons (Exercise 1.7: only unit is 1)."
        table_rows.append(
            f"| {q_val} | {res['nonzero_elements']} | {res['units_used']} "
            f"| {res['num_classes']} | {res['singleton_classes']} "
            f"| {res['non_singleton_classes']} | {res['largest_class_size']} "
            f"| {interp_short} |"
        )
    sections.append("## Results Table\n\n" + "\n".join(table_rows))

    sections.append(
        "## Interpretation\n\n"
        r"**q ∈ ℕ (q = 2):** The only unit is $1$, so every element is its own associate class. "
        "All sample associate classes are singletons.\n\n"
        r"**q = 1/2:** Units include $\{1, 2, 1/2, 4, 1/4\}$ within the sample. "
        "Elements that differ by a power of 2 fall into the same associate class. "
        "The presence of non-singleton classes is consistent with the theoretical unit group "
        r"$\langle 2 \rangle \subset \mathbb{Q}_{>0}$.\n\n"
        r"**q = 1/6:** Units include products of powers of 2 and 3 within the sample. "
        "Associate classes are larger than the q=1/2 case because more units are available.\n\n"
        r"**q = a/b with a, b > 1:** Exercise 1.7 states the only unit of "
        r"$(\mathbb{N}_0[q]\setminus\{0\},\cdot)$ is $1$. All sample associate classes are singletons.\n\n"
        "**Associate classes are necessary for UFM and IDF analysis.** "
        "Unique factorization is always considered up to unit multiples (up to associates). "
        "Without classifying associate classes, length sets of factorizations are not well-defined "
        "in the monoid-theoretic sense."
    )

    sections.append(
        "## Next Experiments\n\n"
        "- `exp_008_valuation_patterns.py` — analyze valuation patterns across the sample.\n"
        "- `exp_007_idf_sanity_checks.py` — IDF sanity checks.\n"
        "- `exp_006_candidate_atomic_divisors.py` — candidate atomic divisors."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 003 — Bounded Associate Class Grouping",
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
    print("Experiment 003 complete.")
    print(f"  Output directory      : {OUTPUT_DIR}")
    print(f"  N0[q]^bullet cases    : {len(results)}")
    print(f"  CSV files             : {len(csv_files)}")
    print(f"  JSON files            : {len(json_files)}")
    print(f"  summary.md            : {'yes' if summary_exists else 'MISSING'}")
    print(f"  Pessoal/ modified     : not checked by script")
    print(f"  Proof files mod       : not checked by script")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  Associate classes are sample-based and do not prove the complete infinite structure.")
    print("")


if __name__ == "__main__":
    main()
