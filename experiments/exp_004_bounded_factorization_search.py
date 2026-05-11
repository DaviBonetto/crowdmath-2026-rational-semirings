import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.factorization import (
    theoretical_atoms_n0q,
    additive_factorizations,
    factorization_lengths,
    factorization_to_str,
    multiplicative_universal_identity,
)
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_004_outputs"

BOUNDED_WARNING = (
    "This is a bounded computational sample. It does not prove atomicity, "
    "unique factorization, IDF behavior, or any infinite mathematical property."
)

MAX_ATOM_DEGREE = 5
MAX_FACTORIZATION_LENGTH = 12
MAX_SOLUTIONS = 50

N0Q_CASES: list[tuple[str, Fraction]] = [
    ("2", Fraction(2)),
    ("1/2", Fraction(1, 2)),
    ("3/2", Fraction(3, 2)),
    ("2/3", Fraction(2, 3)),
    ("4/9", Fraction(4, 9)),
    ("5/3", Fraction(5, 3)),
]

MULTIPLICATIVE_CASES: list[tuple[str, Fraction]] = [
    ("3/2", Fraction(3, 2)),
    ("2/3", Fraction(2, 3)),
    ("4/9", Fraction(4, 9)),
    ("5/3", Fraction(5, 3)),
]


def _theoretical_case_label(q: Fraction) -> str:
    a, b = q.numerator, q.denominator
    if b == 1:
        return "integer"
    if a == 1:
        return "reciprocal_integer"
    return "mixed_fraction"


def _additive_target(q: Fraction) -> Fraction | None:
    a, b = q.numerator, q.denominator
    if b == 1:
        return Fraction(6)
    if a == 1:
        return None
    return Fraction(a)


def _additive_interpretation(
    q: Fraction,
    factorizations: list[tuple[Fraction, ...]],
    atoms: set[Fraction],
) -> str:
    a, b = q.numerator, q.denominator
    if b == 1:
        n = len(factorizations)
        return (
            f"q={fraction_to_str(q)}: N0[q]=N0. Expected one factorization using atom 1. "
            f"Found {n} factorization(s). Consistent with UFM behavior of N0."
        )
    if a == 1:
        return (
            f"q={fraction_to_str(q)}: N0[q] has no atoms by Exercise 1.8. "
            "Additive factorization search is not meaningful. Skipped."
        )
    n = len(factorizations)
    lengths = factorization_lengths(factorizations)
    return (
        f"q={fraction_to_str(q)}: additive identity a=bq gives {a}={b}*({fraction_to_str(q)}). "
        f"Found {n} bounded factorization(s) with length set {lengths}. "
        "Multiple lengths are consistent with non-unique additive factorization (Exercise 1.7). "
        "This is a bounded witness, not a proof."
    )


def run_additive_cases() -> tuple[list[dict], list[dict]]:
    csv_rows: list[dict[str, str]] = []
    json_cases: list[dict] = []

    for label, q in N0Q_CASES:
        atoms_set = theoretical_atoms_n0q(q, MAX_ATOM_DEGREE)
        atoms_list = sorted(atoms_set, key=fraction_sort_key)
        target = _additive_target(q)
        case_label = _theoretical_case_label(q)

        if target is None:
            factorizations = []
            lengths: list[int] = []
            f1 = ""
            f2 = ""
        else:
            factorizations = additive_factorizations(
                target, atoms_list, MAX_FACTORIZATION_LENGTH, MAX_SOLUTIONS
            )
            lengths = factorization_lengths(factorizations)
            f1 = factorization_to_str(factorizations[0]) if len(factorizations) > 0 else ""
            f2 = factorization_to_str(factorizations[1]) if len(factorizations) > 1 else ""

        interpretation = _additive_interpretation(q, factorizations, atoms_set)

        csv_rows.append(
            {
                "q": fraction_to_str(q),
                "target": fraction_to_str(target) if target is not None else "N/A",
                "theoretical_case": case_label,
                "atoms_used": ", ".join(fraction_to_str(a) for a in atoms_list),
                "num_factorizations_found": str(len(factorizations)),
                "length_set": str(lengths),
                "sample_factorization_1": f1,
                "sample_factorization_2": f2,
                "interpretation": interpretation,
            }
        )

        json_cases.append(
            {
                "q": fraction_to_str(q),
                "target": fraction_to_str(target) if target is not None else None,
                "theoretical_case": case_label,
                "atoms_within_degree_bound": [fraction_to_str(a) for a in atoms_list],
                "num_factorizations_found": len(factorizations),
                "length_set": lengths,
                "sample_factorizations": [
                    factorization_to_str(f) for f in factorizations[:5]
                ],
                "interpretation": interpretation,
            }
        )

    write_csv_rows(OUTPUT_DIR / "additive_factorization_search.csv", csv_rows)
    return csv_rows, json_cases


def run_multiplicative_cases() -> tuple[list[dict], list[dict]]:
    csv_rows: list[dict[str, str]] = []
    json_cases: list[dict] = []

    for label, q in MULTIPLICATIVE_CASES:
        identity = multiplicative_universal_identity(q)
        lv = identity["left_value"]
        rv = identity["right_value"]
        holds = identity["identity_holds"]

        interpretation = (
            f"q={fraction_to_str(q)}: the identity (1+q+q^2)(1+q^3) = (1+q^2+q^4)(1+q) "
            f"holds: {holds}. Both sides equal {lv}. "
            "This is the exact symbolic obstruction from Exercise 1.7 showing "
            "that (N0[q]\\{0}, *) is not a UFM when q=a/b with a,b>1. "
            "This computation is exact, not bounded."
        )

        csv_rows.append(
            {
                "q": fraction_to_str(q),
                "left_factor_1": identity["left_factor_1"],
                "left_factor_2": identity["left_factor_2"],
                "right_factor_1": identity["right_factor_1"],
                "right_factor_2": identity["right_factor_2"],
                "left_value": str(lv),
                "right_value": str(rv),
                "identity_holds": "yes" if holds else "no",
                "interpretation": interpretation,
            }
        )

        json_cases.append(
            {
                "q": fraction_to_str(q),
                "left_factor_1": identity["left_factor_1"],
                "left_factor_2": identity["left_factor_2"],
                "right_factor_1": identity["right_factor_1"],
                "right_factor_2": identity["right_factor_2"],
                "left_value": str(lv),
                "right_value": str(rv),
                "identity_holds": holds,
                "interpretation": interpretation,
            }
        )

    write_csv_rows(
        OUTPUT_DIR / "multiplicative_universal_identity.csv", csv_rows
    )
    return csv_rows, json_cases


def build_summary_markdown(
    additive_rows: list[dict],
    mult_rows: list[dict],
) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        r"This experiment searches for bounded additive factorizations in $\mathbb{N}_0[q]$ "
        "and records the universal multiplicative identity from Exercise 1.7. "
        "It provides bounded computational witnesses for two key claims:\n"
        r"1. When $q = a/b$ with $a,b > 1$, the additive monoid $(\mathbb{N}_0[q],+)$ "
        "admits multiple factorization lengths for the same element.\n"
        r"2. The multiplicative identity $(1+q+q^2)(1+q^3) = (1+q^2+q^4)(1+q)$ "
        r"is the exact obstruction showing $(\mathbb{N}_0[q]\setminus\{0\},\cdot)$ is not a UFM."
    )

    sections.append(
        "## Bounded Warning\n\n"
        "> **" + BOUNDED_WARNING + "**\n\n"
        "Additive factorization results are bounded by `max_atom_degree` and "
        "`max_factorization_length`. The multiplicative identity computation is exact "
        "for any given $q$, not bounded."
    )

    sections.append(
        "## Parameters\n\n"
        f"- `max_atom_degree = {MAX_ATOM_DEGREE}`\n"
        f"- `max_factorization_length = {MAX_FACTORIZATION_LENGTH}`\n"
        f"- `max_solutions = {MAX_SOLUTIONS}`\n"
        "- Atoms from `theoretical_atoms_n0q(q, max_atom_degree)` (Exercise 1.8)"
    )

    add_table = [
        "| q | target | theoretical case | factorizations found | length set | interpretation |",
        "|---|---|---|---|---|---|",
    ]
    for row in additive_rows:
        interp_short = row["interpretation"].split(".")[0] + "."
        add_table.append(
            f"| {row['q']} | {row['target']} | {row['theoretical_case']} "
            f"| {row['num_factorizations_found']} | {row['length_set']} "
            f"| {interp_short} |"
        )
    sections.append(
        "## Additive Factorization Search\n\n" + "\n".join(add_table)
    )

    mult_table = [
        "| q | left factorization | right factorization | common value | identity holds |",
        "|---|---|---|---|---|",
    ]
    for row in mult_rows:
        lf = f"({row['left_factor_1']}) · ({row['left_factor_2']})"
        rf = f"({row['right_factor_1']}) · ({row['right_factor_2']})"
        mult_table.append(
            f"| {row['q']} | {lf} | {rf} | {row['left_value']} | {row['identity_holds']} |"
        )
    sections.append(
        "## Multiplicative Universal Identity\n\n" + "\n".join(mult_table)
    )

    sections.append(
        "## Interpretation\n\n"
        r"**q = 2:** $\mathbb{N}_0[2] = \mathbb{N}_0$. Additive factorization behaves like "
        r"$\mathbb{N}_0$, where the only atom is $1$. UFM baseline case per Exercise 1.7.\n\n"
        r"**q = 1/2:** The monoid $(\mathbb{N}_0[1/2],+)$ has no atoms by Exercise 1.8. "
        "Atom-factorization search is not meaningful and is skipped.\n\n"
        r"**q = a/b with a, b > 1 (3/2, 2/3, 4/9, 5/3):** The additive identity $a = bq$ "
        "gives bounded witnesses of non-unique additive factorization: "
        r"$\underbrace{1+\cdots+1}_{a} = \underbrace{q+\cdots+q}_{b}$. "
        "Multiple factorization lengths appear in the bounded search.\n\n"
        "**Multiplicative identity:** $(1+q+q^2)(1+q^3) = (1+q^2+q^4)(1+q)$ is the exact "
        "symbolic obstruction used in Exercise 1.7. Both products factor the element "
        r"$1+q+q^2+q^3+q^4+q^5$ in two distinct ways in $(\mathbb{N}_0[q]\setminus\{0\},\cdot)$.\n\n"
        "**These computations are sanity checks and evidence organization, not proofs.**"
    )

    sections.append(
        "## Next Experiments\n\n"
        "- `exp_002_detect_units_in_bounded_samples.py` — identify units in bounded samples.\n"
        "- `exp_003_group_associate_classes.py` — group elements by associate classes.\n"
        "- `exp_008_valuation_patterns.py` — analyze valuation patterns.\n"
        "- `exp_007_idf_sanity_checks.py` — IDF sanity checks."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 004 — Bounded Factorization Search",
        sections,
    )


def main() -> None:
    ensure_dir(OUTPUT_DIR)

    _, additive_json = run_additive_cases()
    _, mult_json = run_multiplicative_cases()

    additive_csv_rows = list(
        (OUTPUT_DIR / "additive_factorization_search.csv").open(encoding="utf-8")
    )
    additive_md_rows: list[dict] = []
    for case in additive_json:
        additive_md_rows.append(
            {
                "q": case["q"],
                "target": str(case["target"]) if case["target"] else "N/A",
                "theoretical_case": case["theoretical_case"],
                "num_factorizations_found": str(case["num_factorizations_found"]),
                "length_set": str(case["length_set"]),
                "interpretation": case["interpretation"],
            }
        )

    build_summary_markdown(additive_md_rows, mult_json)

    json_payload = {
        "experiment": "exp_004_bounded_factorization_search",
        "bounded_warning": BOUNDED_WARNING,
        "parameters": {
            "max_atom_degree": MAX_ATOM_DEGREE,
            "max_factorization_length": MAX_FACTORIZATION_LENGTH,
            "max_solutions": MAX_SOLUTIONS,
        },
        "additive_cases": additive_json,
        "multiplicative_cases": mult_json,
    }
    write_json(OUTPUT_DIR / "factorization_search_results.json", json_payload)

    csv_files = list(OUTPUT_DIR.glob("*.csv"))
    json_files = list(OUTPUT_DIR.glob("*.json"))
    summary_exists = (OUTPUT_DIR / "summary.md").exists()

    print("")
    print("Experiment 004 complete.")
    print(f"  Output directory    : {OUTPUT_DIR}")
    print(f"  Additive cases      : {len(N0Q_CASES)}")
    print(f"  Multiplicative cases: {len(MULTIPLICATIVE_CASES)}")
    print(f"  CSV files           : {len(csv_files)}")
    print(f"  JSON files          : {len(json_files)}")
    print(f"  summary.md          : {'yes' if summary_exists else 'MISSING'}")
    print(f"  Proof files mod     : not checked by script")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  Factorization witnesses are sample-based and do not prove UFM/non-UFM.")
    print("")


if __name__ == "__main__":
    main()
