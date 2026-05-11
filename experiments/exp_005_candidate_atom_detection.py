import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.semirings import generate_n0_q
from crowdmath2026.factorization import (
    classify_candidate_atoms,
    theoretical_atoms_n0q,
    compare_candidates_to_theory,
)
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_005_outputs"

BOUNDED_WARNING = (
    "This is a bounded computational sample. It does not prove atomicity, "
    "unique factorization, IDF behavior, or any infinite mathematical property."
)

MAX_DEGREE = 5
MAX_COEFF = 3

N0Q_CASES: list[tuple[str, Fraction]] = [
    ("2", Fraction(2)),
    ("1_2", Fraction(1, 2)),
    ("3_2", Fraction(3, 2)),
    ("2_3", Fraction(2, 3)),
    ("4_9", Fraction(4, 9)),
    ("5_3", Fraction(5, 3)),
]


def safe_q_label(q: Fraction) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}_{q.denominator}"


def run_case(
    q: Fraction,
) -> dict[str, object]:
    generation = generate_n0_q(q, MAX_DEGREE, MAX_COEFF)
    elements: set[Fraction] = set(generation.keys())

    classification = classify_candidate_atoms(elements)
    candidates: set[Fraction] = set(classification["candidate_atoms"])

    theoretical = theoretical_atoms_n0q(q, MAX_DEGREE)
    comparison = compare_candidates_to_theory(candidates, theoretical)

    label = safe_q_label(q)
    zero = Fraction(0)

    sorted_elements = sorted(elements, key=fraction_sort_key)

    csv_rows: list[dict[str, str]] = []
    for val in sorted_elements:
        if val == zero:
            classification_str = "zero"
            witness_str = ""
            is_theoretical = "no"
            notes = "Zero is not an atom in any monoid."
        elif val in candidates:
            classification_str = "candidate_atom"
            witness_str = ""
            is_theoretical = "yes" if val in theoretical else "no"
            if val in comparison["false_positives"]:
                notes = (
                    "Sample candidate atom not predicted by theory within degree bound. "
                    "May be a false positive caused by bounded search limits."
                )
            else:
                notes = BOUNDED_WARNING
        else:
            classification_str = "decomposable"
            witness_str = classification["decomposable"].get(fraction_to_str(val), "")
            is_theoretical = "yes" if val in theoretical else "no"
            notes = BOUNDED_WARNING

        csv_rows.append(
            {
                "element": fraction_to_str(val),
                "decimal_approx": f"{float(val):.8f}",
                "classification": classification_str,
                "decomposition_witness": witness_str,
                "is_theoretical_atom_within_degree_bound": is_theoretical,
                "notes": notes,
            }
        )

    csv_path = OUTPUT_DIR / f"n0q_q_{label}_candidate_atoms.csv"
    write_csv_rows(csv_path, csv_rows)

    sample_decomps: dict[str, str] = {}
    for el_str, witness in list(classification["decomposable"].items())[:10]:
        sample_decomps[el_str] = witness

    json_data = {
        "object": "N0[q]",
        "q": fraction_to_str(q),
        "parameters": {
            "max_degree": MAX_DEGREE,
            "max_coeff": MAX_COEFF,
        },
        "bounded_warning": BOUNDED_WARNING,
        "summary": {
            "total_distinct_elements": classification["total_elements"],
            "nonzero_elements": classification["nonzero_elements"],
            "candidate_atom_count": classification["candidate_atom_count"],
            "decomposable_count": classification["decomposable_count"],
            "theoretical_atom_count_within_degree": len(theoretical),
            "true_positive_count": len(comparison["true_positives"]),
            "false_positive_count": len(comparison["false_positives"]),
            "missed_theoretical_atom_count": len(comparison["missed_theoretical_atoms"]),
        },
        "candidate_atoms": sorted(
            [fraction_to_str(x) for x in candidates], key=lambda s: float(Fraction(s))
        ),
        "theoretical_atoms_within_degree": sorted(
            [fraction_to_str(x) for x in theoretical], key=lambda s: float(Fraction(s))
        ),
        "false_positives": sorted(
            [fraction_to_str(x) for x in comparison["false_positives"]],
            key=lambda s: float(Fraction(s)),
        ),
        "missed_theoretical_atoms": sorted(
            [fraction_to_str(x) for x in comparison["missed_theoretical_atoms"]],
            key=lambda s: float(Fraction(s)),
        ),
        "sample_decompositions": sample_decomps,
    }

    json_path = OUTPUT_DIR / f"n0q_q_{label}_candidate_atoms.json"
    write_json(json_path, json_data)

    return {
        "q": fraction_to_str(q),
        "total_distinct_elements": classification["total_elements"],
        "candidate_atom_count": classification["candidate_atom_count"],
        "decomposable_count": classification["decomposable_count"],
        "theoretical_atoms_within_degree": len(theoretical),
        "true_positives": len(comparison["true_positives"]),
        "false_positives": len(comparison["false_positives"]),
        "missed_theoretical_atoms": len(comparison["missed_theoretical_atoms"]),
    }


def build_summary_markdown(results: list[dict[str, object]]) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        r"This experiment performs bounded candidate atom detection in additive monoids "
        r"$\mathbb{N}_0[q]$. "
        "For each element $x$ in a finite generated sample, it searches for a decomposition "
        r"$x = a + b$ with $a, b$ nonzero and in the same sample. "
        "Elements for which no such decomposition is found are called **candidate atoms**. "
        "The results are compared against the theoretical atom sets from Exercise 1.8 (Resource 1)."
    )

    sections.append(
        "## Bounded Warning\n\n"
        "> **" + BOUNDED_WARNING + "**\n\n"
        "False positives occur when a theoretically non-atomic element appears indecomposable "
        "because its decomposition requires elements outside the bounded sample. "
        "This is expected behavior for $q = 1/n$ cases near the degree boundary."
    )

    sections.append(
        "## Parameters\n\n"
        f"- `max_degree = {MAX_DEGREE}`\n"
        f"- `max_coeff = {MAX_COEFF}`\n"
        f"- Sample generated by `generate_n0_q(q, max_degree, max_coeff)` from `semirings.py`\n"
        "- q values tested: " + ", ".join(fraction_to_str(q) for _, q in N0Q_CASES)
    )

    table_rows = [
        "| q | Distinct elements | Candidate atoms | Decomposable | "
        "Theoretical atoms (degree bound) | False positives | Missed theoretical atoms |",
        "|---|---|---|---|---|---|---|",
    ]
    for res in results:
        table_rows.append(
            f"| {res['q']} | {res['total_distinct_elements']} | "
            f"{res['candidate_atom_count']} | {res['decomposable_count']} | "
            f"{res['theoretical_atoms_within_degree']} | "
            f"{res['false_positives']} | {res['missed_theoretical_atoms']} |"
        )
    sections.append("## Results Table\n\n" + "\n".join(table_rows))

    sections.append(
        "## Interpretation\n\n"
        "**q = 2:** "
        r"$\mathbb{N}_0[2] = \mathbb{N}_0$. The only theoretical atom is $1$. "
        "Bounded detection should identify $1$ as the main candidate atom; "
        "any other candidate atoms would indicate insufficient sample closure.\n\n"
        "**q = 1/2:** "
        "Theory (Exercise 1.8) states this monoid has no atoms. "
        "Bounded samples may still show false positive candidate atoms near the upper degree boundary "
        r"because the required decomposition $q^n = 2 \cdot q^{n+1}$ requires $q^{n+1}$ "
        "which lies outside the sample when $n = $ `max_degree`.\n\n"
        "**q = a/b with a, b ≥ 2 (cases 3/2, 2/3, 4/9, 5/3):** "
        r"Theory states the atoms are exactly $\{q^n : n \in \mathbb{N}_0\}$. "
        "Bounded computation identifies these powers as candidate atoms within the degree range. "
        "Mismatches occur at the boundary because some decompositions require higher powers "
        "outside the sample.\n\n"
        "**Candidate atoms are not proven atoms.** "
        "They are elements that appear indecomposable within the bounded sample. "
        "**Decomposition witnesses are useful evidence** of non-atomic behavior "
        "inside the bounded sample."
    )

    sections.append(
        "## Next Experiments\n\n"
        "- `exp_004_bounded_factorization_search.py` — search for longer additive factorizations.\n"
        "- `exp_002_detect_units_in_bounded_samples.py` — identify units in bounded samples.\n"
        "- `exp_003_group_associate_classes.py` — group elements by associate classes.\n"
        "- `exp_008_valuation_patterns.py` — analyze valuation patterns across the sample."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 005 — Candidate Atom Detection",
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
    print("Experiment 005 complete.")
    print(f"  Output directory : {OUTPUT_DIR}")
    print(f"  N0[q] cases      : {len(results)}")
    print(f"  CSV files        : {len(csv_files)}")
    print(f"  JSON files       : {len(json_files)}")
    print(f"  summary.md       : {'yes' if summary_exists else 'MISSING'}")
    print(f"  Proof files mod  : not checked by script")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  Candidate atoms are sample-based and do not prove atomicity.")
    print("")


if __name__ == "__main__":
    main()
