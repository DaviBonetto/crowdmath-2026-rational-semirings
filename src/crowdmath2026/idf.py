from fractions import Fraction

from crowdmath2026.rationals import fraction_to_str

IDF_BOUNDED_WARNING = (
    "This is a bounded IDF sanity check. It does not prove IDF, non-IDF, or the complete "
    "atomic divisor structure of the infinite monoid."
)


def idf_target_summary(
    target: Fraction,
    candidate_divisors: dict[Fraction, Fraction],
    associate_classes: list[set[Fraction]],
) -> dict[str, object]:
    """Summarize IDF-related information for a single target element.

    Args:
      target             : the element being inspected
      candidate_divisors : dict mapping candidate_atom -> quotient_witness
      associate_classes  : list of associate-class sets of the candidate atomic divisors

    Returns a dict with:
      target                              : str
      raw_candidate_atomic_divisor_count  : int
      associate_class_count               : int
      largest_associate_class_size        : int
      visible_idf_check_passed            : bool (always True in bounded sample)
      warning                             : str

    NOTE: visible_idf_check_passed is always True because a bounded sample contains
    finitely many elements. This should NOT be read as a proof of IDF for the
    infinite monoid.
    """
    raw_count = len(candidate_divisors)
    class_count = len(associate_classes)
    largest = max((len(cls) for cls in associate_classes), default=0)

    return {
        "target": fraction_to_str(target),
        "raw_candidate_atomic_divisor_count": raw_count,
        "associate_class_count": class_count,
        "largest_associate_class_size": largest,
        "visible_idf_check_passed": True,
        "warning": IDF_BOUNDED_WARNING,
    }


def summarize_idf_case(
    target_summaries: list[dict[str, object]],
) -> dict[str, object]:
    """Aggregate IDF summary statistics across all targets for a given q.

    Returns a dict with:
      targets_tested                    : int
      max_raw_divisor_count             : int
      max_associate_class_count         : int
      max_largest_associate_class_size  : int
      targets_with_nonzero_divisors     : int
      targets_with_multiple_associate_classes : int
      visible_idf_checks_all_finite     : bool
    """
    if not target_summaries:
        return {
            "targets_tested": 0,
            "max_raw_divisor_count": 0,
            "max_associate_class_count": 0,
            "max_largest_associate_class_size": 0,
            "targets_with_nonzero_divisors": 0,
            "targets_with_multiple_associate_classes": 0,
            "visible_idf_checks_all_finite": True,
        }

    return {
        "targets_tested": len(target_summaries),
        "max_raw_divisor_count": max(
            s["raw_candidate_atomic_divisor_count"] for s in target_summaries
        ),
        "max_associate_class_count": max(
            s["associate_class_count"] for s in target_summaries
        ),
        "max_largest_associate_class_size": max(
            s["largest_associate_class_size"] for s in target_summaries
        ),
        "targets_with_nonzero_divisors": sum(
            1 for s in target_summaries if s["raw_candidate_atomic_divisor_count"] > 0
        ),
        "targets_with_multiple_associate_classes": sum(
            1 for s in target_summaries if s["associate_class_count"] > 1
        ),
        "visible_idf_checks_all_finite": all(
            s["visible_idf_check_passed"] for s in target_summaries
        ),
    }


def idf_interpretation_label(
    q_case: str,
    raw_divisor_count: int,
    associate_class_count: int,
) -> str:
    """Return a concise, conservative IDF interpretation label for one target.

    Args:
      q_case              : 'integer' | 'reciprocal_integer' | 'mixed_fraction'
      raw_divisor_count   : number of raw candidate atomic divisors
      associate_class_count : number of associate classes of those divisors
    """
    if q_case == "integer":
        return "integer baseline"
    if q_case == "reciprocal_integer":
        return "nontrivial units may collapse raw divisors into fewer associate classes"
    if q_case == "mixed_fraction":
        return "only unit 1 expected; raw divisors and associate classes usually coincide"
    return "bounded sample"


def raw_vs_associate_gap(
    raw_divisor_count: int,
    associate_class_count: int,
) -> int:
    """Return raw_divisor_count - associate_class_count.

    A positive gap indicates that units are collapsing multiple raw candidate
    atomic divisors into the same associate class. This is expected for
    q = 1/n cases where nontrivial units exist.
    """
    return raw_divisor_count - associate_class_count
