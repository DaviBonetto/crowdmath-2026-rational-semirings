import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.semirings import generate_n0_q, generate_n0_qr, summarize_generation
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_001_outputs"

BOUNDED_WARNING = (
    "This is a bounded computational sample and does not prove "
    "any infinite mathematical property."
)

N0Q_CASES: list[tuple[str, Fraction]] = [
    ("q=2", Fraction(2)),
    ("q=1_2", Fraction(1, 2)),
    ("q=3_2", Fraction(3, 2)),
    ("q=2_3", Fraction(2, 3)),
]

N0QR_CASES: list[tuple[str, Fraction, Fraction]] = [
    ("q=2_3,r=3_5", Fraction(2, 3), Fraction(3, 5)),
    ("q=3_2,r=5_3", Fraction(3, 2), Fraction(5, 3)),
    ("q=1_2,r=1_3", Fraction(1, 2), Fraction(1, 3)),
]

MAX_DEGREE = 4
MAX_COEFF = 3
MAX_DEGREE_Q = 3
MAX_DEGREE_R = 3
MAX_COEFF_QR = 2


def rep_n0q_to_str(rep: tuple[int, ...]) -> str:
    return "(" + ", ".join(str(c) for c in rep) + ")"


def rep_n0qr_to_str(rep: tuple[tuple[int, int, int], ...]) -> str:
    if not rep:
        return "()"
    return "(" + ", ".join(f"({i},{j},{c})" for i, j, c in rep) + ")"


def run_n0q_case(
    label: str,
    q: Fraction,
    max_degree: int,
    max_coeff: int,
) -> dict[str, object]:
    elements = generate_n0_q(q, max_degree, max_coeff)
    summary = summarize_generation(elements)

    sorted_values = sorted(elements.keys(), key=fraction_sort_key)

    csv_rows: list[dict[str, str]] = []
    for val in sorted_values:
        sample_rep, count = elements[val]
        csv_rows.append(
            {
                "element": fraction_to_str(val),
                "decimal_approx": f"{float(val):.8f}",
                "num_representations": str(count),
                "sample_representation": rep_n0q_to_str(sample_rep),
            }
        )

    write_csv_rows(OUTPUT_DIR / f"n0q_{label}.csv", csv_rows)

    sample_elements = []
    for val in sorted_values[:20]:
        sample_rep, count = elements[val]
        sample_elements.append(
            {
                "element": fraction_to_str(val),
                "num_representations": count,
                "sample_representation": rep_n0q_to_str(sample_rep),
            }
        )

    json_data = {
        "object": "N0[q]",
        "parameters": {
            "q": fraction_to_str(q),
            "max_degree": max_degree,
            "max_coeff": max_coeff,
        },
        "summary": summary,
        "warning": BOUNDED_WARNING,
        "sample_elements": sample_elements,
    }

    write_json(OUTPUT_DIR / f"n0q_{label}.json", json_data)

    return {
        "label": label,
        "q": fraction_to_str(q),
        "distinct_elements": summary["total_distinct_elements"],
        "total_representations": summary["total_representations"],
        "collisions": summary["collisions"],
        "max_reps": summary["max_representations_for_one_element"],
    }


def run_n0qr_case(
    label: str,
    q: Fraction,
    r: Fraction,
    max_degree_q: int,
    max_degree_r: int,
    max_coeff: int,
) -> dict[str, object]:
    elements = generate_n0_qr(q, r, max_degree_q, max_degree_r, max_coeff)
    summary = summarize_generation(elements)

    sorted_values = sorted(elements.keys(), key=fraction_sort_key)

    csv_rows: list[dict[str, str]] = []
    for val in sorted_values:
        sample_rep, count = elements[val]
        csv_rows.append(
            {
                "element": fraction_to_str(val),
                "decimal_approx": f"{float(val):.8f}",
                "num_representations": str(count),
                "sample_representation": rep_n0qr_to_str(sample_rep),
            }
        )

    write_csv_rows(OUTPUT_DIR / f"n0qr_{label}.csv", csv_rows)

    sample_elements = []
    for val in sorted_values[:20]:
        sample_rep, count = elements[val]
        sample_elements.append(
            {
                "element": fraction_to_str(val),
                "num_representations": count,
                "sample_representation": rep_n0qr_to_str(sample_rep),
            }
        )

    json_data = {
        "object": "N0[q,r]",
        "parameters": {
            "q": fraction_to_str(q),
            "r": fraction_to_str(r),
            "max_degree_q": max_degree_q,
            "max_degree_r": max_degree_r,
            "max_coeff": max_coeff,
        },
        "summary": summary,
        "warning": BOUNDED_WARNING,
        "sample_elements": sample_elements,
    }

    write_json(OUTPUT_DIR / f"n0qr_{label}.json", json_data)

    return {
        "label": label,
        "q": fraction_to_str(q),
        "r": fraction_to_str(r),
        "distinct_elements": summary["total_distinct_elements"],
        "total_representations": summary["total_representations"],
        "collisions": summary["collisions"],
        "max_reps": summary["max_representations_for_one_element"],
    }


def build_summary_markdown(
    n0q_results: list[dict[str, object]],
    n0qr_results: list[dict[str, object]],
) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        r"Experiment 001 generates bounded finite samples of elements of "
        r"$\mathbb{N}_0[q]$ and $\mathbb{N}_0[q,r]$ using exact rational arithmetic "
        r"(`fractions.Fraction`). "
        "It records distinct values, representation counts, and collisions. "
        "A collision means that the same rational number is reached by more than one "
        "bounded polynomial coefficient tuple. "
        "Collisions indicate multiple bounded polynomial representations of the same "
        "rational element. They are useful computational signals, but they do not by "
        "themselves prove failure of unique factorization. "
        "This is infrastructure for future experiments on atoms, factorizations, units, and IDF."
    )

    sections.append(
        "## Parameters\n\n"
        f"**N0[q]:** `max_degree = {MAX_DEGREE}`, `max_coeff = {MAX_COEFF}`\n\n"
        f"**N0[q,r]:** `max_degree_q = {MAX_DEGREE_Q}`, `max_degree_r = {MAX_DEGREE_R}`, "
        f"`max_coeff = {MAX_COEFF_QR}`"
    )

    n0q_rows = [
        "| q | Distinct elements | Total reps | Collisions | Max reps per element |",
        "|---|---|---|---|---|",
    ]
    for res in n0q_results:
        n0q_rows.append(
            f"| {res['q']} | {res['distinct_elements']} | {res['total_representations']} "
            f"| {res['collisions']} | {res['max_reps']} |"
        )
    sections.append("## N0[q] Results\n\n" + "\n".join(n0q_rows))

    n0qr_rows = [
        "| q | r | Distinct elements | Total reps | Collisions | Max reps per element |",
        "|---|---|---|---|---|---|",
    ]
    for res in n0qr_results:
        n0qr_rows.append(
            f"| {res['q']} | {res['r']} | {res['distinct_elements']} | {res['total_representations']} "
            f"| {res['collisions']} | {res['max_reps']} |"
        )
    sections.append("## N0[q,r] Results\n\n" + "\n".join(n0qr_rows))

    sections.append(
        "## Warning\n\n"
        "> **This is a bounded computational sample. It does not prove atomicity, "
        "unique factorization, IDF behavior, or any infinite mathematical property.**\n\n"
        "All outputs are finite samples bounded by degree and coefficient constraints. "
        "No infinite properties (atomicity, UFM, IDF) are inferred from these results."
    )

    sections.append(
        "## Next Experiments\n\n"
        "- `exp_002_detect_units_in_bounded_samples.py` — identify units within bounded samples.\n"
        "- `exp_004_bounded_factorization_search.py` — search for additive factorizations within bounded sets.\n"
        "- `exp_005_candidate_atom_detection.py` — identify candidate atoms: elements with no nontrivial decomposition in the sample."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 001 — Bounded Element Generation for N0[q] and N0[q,r]",
        sections,
    )


def main() -> None:
    ensure_dir(OUTPUT_DIR)

    n0q_results: list[dict[str, object]] = []
    for label, q in N0Q_CASES:
        result = run_n0q_case(label, q, MAX_DEGREE, MAX_COEFF)
        n0q_results.append(result)

    n0qr_results: list[dict[str, object]] = []
    for label, q, r in N0QR_CASES:
        result = run_n0qr_case(label, q, r, MAX_DEGREE_Q, MAX_DEGREE_R, MAX_COEFF_QR)
        n0qr_results.append(result)

    build_summary_markdown(n0q_results, n0qr_results)

    csv_files = list(OUTPUT_DIR.glob("*.csv"))
    json_files = list(OUTPUT_DIR.glob("*.json"))
    summary_exists = (OUTPUT_DIR / "summary.md").exists()

    print("")
    print("Experiment 001 complete.")
    print(f"  Output directory : {OUTPUT_DIR}")
    print(f"  N0[q] cases      : {len(n0q_results)}")
    print(f"  N0[q,r] cases    : {len(n0qr_results)}")
    print(f"  CSV files        : {len(csv_files)}")
    print(f"  JSON files       : {len(json_files)}")
    print(f"  summary.md       : {'yes' if summary_exists else 'MISSING'}")
    print(f"  Proof files mod  : no")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  Collisions indicate multiple bounded polynomial representations")
    print("  of the same rational element — not a proof of non-unique factorization.")
    print("")


if __name__ == "__main__":
    main()
