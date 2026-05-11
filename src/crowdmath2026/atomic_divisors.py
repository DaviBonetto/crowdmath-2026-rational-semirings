from fractions import Fraction

from crowdmath2026.associates import (
    group_associate_classes,
    canonical_representative,
)


def find_multiplicative_factorization_in_sample(
    x: Fraction,
    sample: set[Fraction],
    units: set[Fraction],
) -> tuple[Fraction, Fraction] | None:
    """Find a nontrivial multiplicative factorization of x within the sample.

    Returns (a, b) with a, b in sample, neither a unit, and a*b == x.
    Returns None if no such pair exists within the sample.

    This is a bounded search: absence of a witness does not prove x is an atom.
    """
    zero = Fraction(0)
    if x == zero:
        return None
    for a in sample:
        if a == zero or a in units:
            continue
        if a == x:
            continue  # would force b = 1 (a unit)
        # Exact division: check whether x/a is in the sample and nonunit
        if x % a == Fraction(0):
            b = x / a
        else:
            b = x / a  # Fraction division is always exact
        if b in sample and b not in units and b != zero and a * b == x:
            return (a, b)
    return None


def classify_candidate_multiplicative_atoms(
    sample: set[Fraction],
    units: set[Fraction],
) -> dict[str, object]:
    """Classify nonzero sample elements as candidate multiplicative atoms or decomposable.

    An element is a candidate atom if:
    - it is not zero,
    - it is not a unit,
    - no nontrivial multiplicative factorization exists within the sample.

    Returns a dict with:
      candidate_atoms       : set[Fraction]
      decomposable          : dict[Fraction, tuple[Fraction, Fraction]]
      unit_count            : int
      candidate_atom_count  : int
      decomposable_count    : int
      nonzero_sample_count  : int

    NOTE: 'Candidate atom' does not imply proven atom. Bounded search may miss
    factorizations whose factors lie outside the sample.
    """
    zero = Fraction(0)
    nonzero = {x for x in sample if x != zero}

    candidate_atoms: set[Fraction] = set()
    decomposable: dict[Fraction, tuple[Fraction, Fraction]] = {}

    for x in nonzero:
        if x in units:
            continue
        witness = find_multiplicative_factorization_in_sample(x, nonzero, units)
        if witness is None:
            candidate_atoms.add(x)
        else:
            decomposable[x] = witness

    return {
        "candidate_atoms": candidate_atoms,
        "decomposable": decomposable,
        "unit_count": len(units & nonzero),
        "candidate_atom_count": len(candidate_atoms),
        "decomposable_count": len(decomposable),
        "nonzero_sample_count": len(nonzero),
    }


def divides_in_sample(
    divisor: Fraction,
    target: Fraction,
    sample: set[Fraction],
) -> Fraction | None:
    """Return the quotient target/divisor if it lies in the sample, else None.

    Uses exact Fraction arithmetic. Returns None for zero divisor.
    """
    zero = Fraction(0)
    if divisor == zero:
        return None
    quotient = target / divisor
    if quotient in sample:
        return quotient
    return None


def candidate_atomic_divisors(
    target: Fraction,
    candidate_atoms: set[Fraction],
    sample: set[Fraction],
) -> dict[Fraction, Fraction]:
    """Find all candidate atoms that divide target inside the sample.

    Returns:
      dict mapping candidate_atom -> quotient_witness

    A candidate atom a is included if target/a lies in the sample.
    This is a bounded search: atoms whose quotient lies outside the sample are missed.
    """
    result: dict[Fraction, Fraction] = {}
    for a in candidate_atoms:
        q = divides_in_sample(a, target, sample)
        if q is not None:
            result[a] = q
    return result


def group_divisors_by_associate_class(
    divisors: set[Fraction],
    units: set[Fraction],
    sample: set[Fraction],
) -> list[set[Fraction]]:
    """Group a set of candidate atomic divisors into sample associate classes.

    Uses BFS associate grouping restricted to the divisor set.
    Two divisors a, b are in the same class if there exists a sample unit u
    such that u*a = b (and b is also a divisor).

    Returns a list of sets; each set is one sample associate class.
    """
    return group_associate_classes(divisors, units)
