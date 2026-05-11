import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key
from crowdmath2026.semirings import generate_n0_q
from crowdmath2026.valuations import (
    support_primes,
    valuation_vector,
    valuation_summary,
    integer_prime_factorization,
)
from crowdmath2026.experiments import (
    ensure_dir,
    write_json,
    write_csv_rows,
    write_markdown_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "results" / "exp_008_outputs"

BOUNDED_WARNING = (
    "This is a bounded computational sample. It does not prove the complete "
    "valuation structure of the infinite monoid."
)

MAX_DEGREE = 5
MAX_COEFF = 3
PRIME_CAP = 8

# First 20 primes for reference
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

N0Q_CASES: list[tuple[str, Fraction]] = [
    ("2", Fraction(2)),
    ("1_2", Fraction(1, 2)),
    ("1_6", Fraction(1, 6)),
    ("3_2", Fraction(3, 2)),
    ("2_3", Fraction(2, 3)),
    ("4_9", Fraction(4, 9)),
    ("5_3", Fraction(5, 3)),
]


def _select_primes(
    q: Fraction,
    nonzero_sample: set[Fraction],
) -> tuple[list[int], bool]:
    """Select relevant primes for valuation analysis.

    Strategy:
    1. Always include primes from q (numerator and denominator).
    2. Add primes found in sample elements, sorted numerically.
    3. Cap total at PRIME_CAP.
    4. Return (selected_primes, truncation_occurred).
    """
    q_primes = support_primes(q) if q != Fraction(1) else set()
    # Ensure 2 is included if q is integer > 1 and 2 divides q
    q_primes.update(integer_prime_factorization(abs(q.numerator)).keys())
    q_primes.update(integer_prime_factorization(q.denominator).keys())

    # Collect all sample primes
    sample_prime_set: set[int] = set()
    for x in nonzero_sample:
        try:
            sample_prime_set.update(support_primes(x))
        except ValueError:
            pass

    all_candidates = sorted(q_primes | sample_prime_set)
    # Filter to known small primes list to avoid any odd integers sneaking in
    all_candidates = [p for p in all_candidates if p in SMALL_PRIMES]

    truncated = len(all_candidates) > PRIME_CAP
    selected = all_candidates[:PRIME_CAP]
    return selected, truncated


def _range_summary_str(ranges: dict[str, dict[str, int]], primes: list[int]) -> str:
    """Format valuation ranges as a compact string for the summary table."""
    parts = []
    for p in primes:
        rng = ranges.get(str(p), {})
        lo = rng.get("min", 0)
        hi = rng.get("max", 0)
        parts.append(f"v_{p}:[{lo},{hi}]")
    return ", ".join(parts)


def run_case(q: Fraction) -> dict[str, object]:
    generation = generate_n0_q(q, MAX_DEGREE, MAX_COEFF)
    zero = Fraction(0)
    nonzero_sample: set[Fraction] = {x for x in generation.keys() if x != zero}

    selected_primes, truncated = _select_primes(q, nonzero_sample)
    summary = valuation_summary(nonzero_sample, selected_primes)

    label = fraction_to_str(q).replace("/", "_")
    sorted_elements = sorted(nonzero_sample, key=fraction_sort_key)

    # CSV: one row per element
    primes_str = str(selected_primes)
    csv_rows: list[dict[str, str]] = []
    for x in sorted_elements:
        try:
            sp = sorted(support_primes(x))
        except ValueError:
            sp = []
        try:
            vvec = valuation_vector(x, selected_primes)
        except ValueError:
            vvec = tuple(0 for _ in selected_primes)

        csv_rows.append(
            {
                "element": fraction_to_str(x),
                "decimal_approx": f"{float(x):.8f}",
                "numerator": str(x.numerator),
                "denominator": str(x.denominator),
                "support_primes": str(sp),
                "valuation_vector": str(list(vvec)),
                "selected_primes": primes_str,
            }
        )

    csv_path = OUTPUT_DIR / f"n0q_q_{label}_valuations.csv"
    write_csv_rows(csv_path, csv_rows)

    # Sample rows for JSON (limit to first 20 for readability)
    sample_json_rows = []
    for row in csv_rows[:20]:
        sample_json_rows.append(
            {
                "element": row["element"],
                "numerator": row["numerator"],
                "denominator": row["denominator"],
                "support_primes": row["support_primes"],
                "valuation_vector": row["valuation_vector"],
            }
        )

    ranges = summary.get("valuation_ranges", {})
    json_data = {
        "object": "N0[q]",
        "q": fraction_to_str(q),
        "parameters": {
            "max_degree": MAX_DEGREE,
            "max_coeff": MAX_COEFF,
            "prime_cap": PRIME_CAP,
        },
        "bounded_warning": BOUNDED_WARNING,
        "selected_primes": selected_primes,
        "prime_truncation_occurred": truncated,
        "summary": {
            "num_nonzero_elements": summary["num_elements"],
            "vector_count": summary["vector_count"],
            "valuation_ranges": {
                str(p): ranges.get(str(p), {}) for p in selected_primes
            },
        },
        "sample_rows": sample_json_rows,
    }

    json_path = OUTPUT_DIR / f"n0q_q_{label}_valuations.json"
    write_json(json_path, json_data)

    range_str = _range_summary_str(ranges, selected_primes)

    return {
        "q": fraction_to_str(q),
        "nonzero_elements": summary["num_elements"],
        "selected_primes": str(selected_primes),
        "vector_count": summary["vector_count"],
        "range_summary": range_str,
        "truncation": "yes" if truncated else "no",
    }


def build_summary_markdown(results: list[dict[str, object]]) -> None:
    sections: list[str] = []

    sections.append(
        "## Purpose\n\n"
        r"This experiment computes bounded $p$-adic valuation vectors for nonzero elements "
        r"of $\mathbb{N}_0[q]$. For a nonzero rational $x = a/b$ in lowest terms, the "
        r"$p$-adic valuation is $v_p(x) = v_p(a) - v_p(b)$, where $v_p(n)$ is the "
        "exponent of $p$ in the prime factorization of $n$. "
        "Valuation patterns help organize denominator behavior, divisibility structure, "
        "and arithmetic properties relevant to Exercises 0.8, 1.7, and 1.8."
    )

    sections.append(
        "## Bounded Warning\n\n"
        "> **" + BOUNDED_WARNING + "**\n\n"
        "Selected primes are chosen from primes appearing in $q$ and in the bounded sample. "
        f"The prime list is capped at {PRIME_CAP} primes. Valuation ranges reflect only "
        "elements reachable within the degree and coefficient bounds."
    )

    sections.append(
        "## Parameters\n\n"
        f"- `max_degree = {MAX_DEGREE}`\n"
        f"- `max_coeff = {MAX_COEFF}`\n"
        f"- `prime_cap = {PRIME_CAP}` (first {PRIME_CAP} primes appearing in $q$ and sample)\n"
        "- Sample generated by `generate_n0_q(q, max_degree, max_coeff)` from `semirings.py`\n"
        "- Valuation functions from `src/crowdmath2026/valuations.py`\n"
        "- q values tested: " + ", ".join(str(r["q"]) for r in results)
    )

    table_rows = [
        "| q | Nonzero elements | Selected primes | Valuation vectors | Valuation range summary | Truncation? |",
        "|---|---|---|---|---|---|",
    ]
    for res in results:
        table_rows.append(
            f"| {res['q']} | {res['nonzero_elements']} | {res['selected_primes']} "
            f"| {res['vector_count']} | {res['range_summary']} | {res['truncation']} |"
        )
    sections.append("## Results Table\n\n" + "\n".join(table_rows))

    sections.append(
        "## Interpretation\n\n"
        r"**q = 2:** Elements lie in $\mathbb{N}_0[2] = \mathbb{N}_0$. "
        "All denominators are 1, so $p$-adic valuations are nonnegative. "
        "The valuation vector tracks divisibility by small primes within the integer sample.\n\n"
        r"**q = 1/2:** Negative 2-adic valuations appear. "
        r"Elements include $1/2, 1/4, 1/8, \ldots$ whose denominators are powers of 2. "
        r"This reflects the structure $\mathbb{N}_0[1/2] \subset \mathbb{Z}[1/2]_{>0}$.\n\n"
        r"**q = 1/6:** Both negative 2-adic and 3-adic valuations appear. "
        r"Elements include denominators that are products of powers of 2 and 3. "
        r"This reflects $\mathbb{N}_0[1/6] \subset \mathbb{Z}[1/6]_{>0}$.\n\n"
        r"**q = a/b with a, b > 1:** Numerator and denominator primes of $q$ "
        "create mixed valuation behavior. "
        "For example, $q = 3/2$ introduces both 3-adic and 2-adic valuations in sample elements. "
        "The valuation vector changes with each power of $q$.\n\n"
        "**Valuation data organizes future experiments.** "
        "Divisibility patterns, denominator bounds, and prime support are useful inputs "
        "for IDF analysis and atomic divisor detection.\n\n"
        "**This is not a proof of infinite valuation behavior.** "
        "The sample covers only elements reachable within the degree and coefficient bounds."
    )

    sections.append(
        "## Next Experiments\n\n"
        "- `exp_007_idf_sanity_checks.py` — IDF sanity checks.\n"
        "- `exp_006_candidate_atomic_divisors.py` — candidate atomic divisors."
    )

    write_markdown_summary(
        OUTPUT_DIR / "summary.md",
        "Experiment 008 — Bounded Valuation Patterns",
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
    print("Experiment 008 complete.")
    print(f"  Output directory : {OUTPUT_DIR}")
    print(f"  N0[q] cases      : {len(results)}")
    print(f"  CSV files        : {len(csv_files)}")
    print(f"  JSON files       : {len(json_files)}")
    print(f"  summary.md       : {'yes' if summary_exists else 'MISSING'}")
    print(f"  Pessoal/ modified: not checked by script")
    print(f"  Proof files mod  : not checked by script")
    print("")
    print("  WARNING: This is bounded computational evidence only.")
    print("  Valuation patterns are sample-based and do not prove the complete infinite structure.")
    print("")


if __name__ == "__main__":
    main()
