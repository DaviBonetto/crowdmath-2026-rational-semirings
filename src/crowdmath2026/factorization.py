from fractions import Fraction

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key


def find_additive_decomposition(
    x: Fraction,
    elements: set[Fraction],
) -> tuple[Fraction, Fraction] | None:
    """Search for a pair (a, b) of nonzero elements in the sample with a + b = x.

    Returns one witness (a, b) if found, or None if no decomposition exists
    within the given sample. Zero is excluded as a summand.

    This is a bounded search: the sample is finite, so a None result does
    not prove that x is an atom in the infinite monoid.
    """
    zero = Fraction(0)
    for a in elements:
        if a <= zero:
            continue
        b = x - a
        if b <= zero:
            continue
        if b == a and b in elements:
            return (a, b)
        if b != a and b in elements:
            return (a, b)
    return None


def classify_candidate_atoms(
    elements: set[Fraction],
) -> dict[str, object]:
    """Classify all elements in a bounded sample as candidate atoms or decomposable.

    An element is a candidate atom in the sample if no decomposition
    x = a + b with a, b nonzero and in the sample is found.

    This is strictly a bounded result. Candidate atoms may be false positives
    if the required decomposition falls outside the sample range.

    Returns a dict with keys:
      candidate_atoms        : sorted list of Fraction
      decomposable           : dict mapping str(element) -> "a + b" witness string
      zero_present           : bool
      total_elements         : int
      nonzero_elements       : int
      candidate_atom_count   : int
      decomposable_count     : int
    """
    zero = Fraction(0)
    positive_elements = {x for x in elements if x > zero}

    candidate_atoms: list[Fraction] = []
    decomposable: dict[str, str] = {}

    for x in sorted(positive_elements, key=fraction_sort_key):
        witness = find_additive_decomposition(x, positive_elements)
        if witness is None:
            candidate_atoms.append(x)
        else:
            a, b = witness
            decomposable[fraction_to_str(x)] = (
                f"{fraction_to_str(a)} + {fraction_to_str(b)}"
            )

    return {
        "candidate_atoms": candidate_atoms,
        "decomposable": decomposable,
        "zero_present": zero in elements,
        "total_elements": len(elements),
        "nonzero_elements": len(positive_elements),
        "candidate_atom_count": len(candidate_atoms),
        "decomposable_count": len(decomposable),
    }


def theoretical_atoms_n0q(
    q: Fraction,
    max_degree: int,
) -> set[Fraction]:
    """Return the theoretical set of atoms of (N0[q], +) within the degree bound.

    Based on Exercise 1.8 (Resource 1):
    - q in N (b=1):            atoms = {1}
    - q = 1/n for n >= 2:      atoms = {} (non-atomic monoid)
    - q = a/b with a,b >= 2:   atoms = {q^n : 0 <= n <= max_degree}

    This returns only atoms up to q^max_degree, matching the sample range.
    It does not return atoms outside the degree bound even if they exist.
    """
    a = q.numerator
    b = q.denominator

    if b == 1:
        return {Fraction(1)}

    if a == 1:
        return set()

    power = Fraction(1)
    atoms: set[Fraction] = set()
    for _ in range(max_degree + 1):
        atoms.add(power)
        power = power * q
    return atoms


def compare_candidates_to_theory(
    candidates: set[Fraction],
    theoretical: set[Fraction],
) -> dict[str, set[Fraction]]:
    """Compare bounded candidate atoms to the theoretical atom set.

    Returns:
      true_positives             : in both candidates and theoretical
      false_positives            : in candidates but not in theoretical
      missed_theoretical_atoms   : in theoretical but not in candidates

    False positives arise when the sample boundary makes a theoretically
    non-atomic element appear indecomposable (its decomposition lies outside
    the bounded sample). Missed theoretical atoms occur when the sample
    does not contain the atom at all, or when the atom's required
    decomposition check fails for another reason.
    """
    true_positives = candidates & theoretical
    false_positives = candidates - theoretical
    missed = theoretical - candidates

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "missed_theoretical_atoms": missed,
    }


def additive_factorizations(
    target: Fraction,
    atoms: list[Fraction],
    max_length: int,
    max_solutions: int = 50,
) -> list[tuple[Fraction, ...]]:
    """Search for factorizations of target as a sum of atoms.

    Each factorization is a tuple of atoms in nondecreasing order, so
    permutations of the same multiset are counted once.

    Only atoms <= target are considered. Stops after max_solutions results.
    Returns exact Fraction tuples.

    This is a bounded search. An empty result does not prove that the target
    is an atom in the infinite monoid; it only means no factorization was
    found within the given atom set and length bound.
    """
    usable = sorted(a for a in atoms if Fraction(0) < a <= target)
    solutions: list[tuple[Fraction, ...]] = []

    def dfs(remaining: Fraction, current: list[Fraction], min_index: int) -> None:
        if remaining == Fraction(0):
            solutions.append(tuple(current))
            return
        if len(current) >= max_length:
            return
        if len(solutions) >= max_solutions:
            return
        for i in range(min_index, len(usable)):
            a = usable[i]
            if a > remaining:
                break
            current.append(a)
            dfs(remaining - a, current, i)
            current.pop()
            if len(solutions) >= max_solutions:
                return

    dfs(target, [], 0)
    return solutions


def factorization_lengths(
    factorizations: list[tuple[Fraction, ...]],
) -> list[int]:
    """Return sorted list of distinct factorization lengths."""
    return sorted({len(f) for f in factorizations})


def factorization_to_str(factorization: tuple[Fraction, ...]) -> str:
    """Convert a factorization tuple to a human-readable sum string.

    Example: (1, 1, Fraction(3,2)) -> "1 + 1 + 3/2"
    """
    return " + ".join(fraction_to_str(a) for a in factorization)


def multiplicative_universal_identity(
    q: Fraction,
) -> dict[str, object]:
    """Compute the multiplicative universal non-UFM identity from Exercise 1.7.

    The identity is:
        (1 + q + q^2)(1 + q^3) = (1 + q^2 + q^4)(1 + q)

    Both sides expand to 1 + q + q^2 + q^3 + q^4 + q^5, so the identity holds
    for all q. This is the exact symbolic obstruction used to show that
    (N0[q] \\ {0}, *) is not a UFM when q = a/b with a, b > 1.

    All arithmetic is exact via fractions.Fraction.
    """
    q2 = q * q
    q3 = q2 * q
    q4 = q3 * q

    left_f1 = Fraction(1) + q + q2
    left_f2 = Fraction(1) + q3
    left_value = left_f1 * left_f2

    right_f1 = Fraction(1) + q2 + q4
    right_f2 = Fraction(1) + q
    right_value = right_f1 * right_f2

    return {
        "q": fraction_to_str(q),
        "left_factor_1": fraction_to_str(left_f1),
        "left_factor_2": fraction_to_str(left_f2),
        "right_factor_1": fraction_to_str(right_f1),
        "right_factor_2": fraction_to_str(right_f2),
        "left_value": fraction_to_str(left_value),
        "right_value": fraction_to_str(right_value),
        "identity_holds": left_value == right_value,
    }
