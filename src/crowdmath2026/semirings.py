from fractions import Fraction


def powers(base: Fraction, max_degree: int) -> list[Fraction]:
    """Return [base**0, base**1, ..., base**max_degree] using exact arithmetic."""
    result: list[Fraction] = []
    current = Fraction(1)
    for _ in range(max_degree + 1):
        result.append(current)
        current = current * base
    return result


def _extend_by_monomial(
    current: dict[Fraction, tuple[tuple, int]],
    mono_value: Fraction,
    coeff_tag: object,
    max_coeff: int,
    zero_tag: object,
) -> dict[Fraction, tuple[tuple, int]]:
    """Extend a generation dict by one monomial.

    current maps value -> (sample_rep, count).
    coeff_tag is a callable c -> tag to append to the representation for
    nonzero c; zero_tag is what to append for c == 0 (typically None, skipped).

    Returns a new dict of the same shape.
    """
    next_state: dict[Fraction, tuple[tuple, int]] = {}
    for value, (sample_rep, count) in current.items():
        for c in range(max_coeff + 1):
            new_value = value + Fraction(c) * mono_value
            tag = coeff_tag(c)
            new_rep = sample_rep if tag is None else sample_rep + (tag,)
            new_count = count
            if new_value not in next_state:
                next_state[new_value] = (new_rep, new_count)
            else:
                existing_rep, existing_count = next_state[new_value]
                next_state[new_value] = (existing_rep, existing_count + new_count)
    return next_state


def generate_n0_q(
    q: Fraction,
    max_degree: int,
    max_coeff: int,
) -> dict[Fraction, tuple[tuple[int, ...], int]]:
    """Generate bounded elements of N0[q] with exact rational arithmetic.

    Elements have the form  c_0 + c_1*q + ... + c_d*q^d
    where 0 <= d <= max_degree and 0 <= c_i <= max_coeff.

    Returns a dict mapping each distinct Fraction value to a pair:
      (sample_representation, total_count)
    where sample_representation is one coefficient tuple (c_0, ..., c_max_degree)
    and total_count is the number of distinct tuples producing that value.

    Zero is included.
    """
    q_powers = powers(q, max_degree)
    state: dict[Fraction, tuple[tuple, int]] = {Fraction(0): ((), 1)}

    for mono_value in q_powers:
        def _tag(c: int) -> tuple[int, ...]:
            return (c,)
        next_state: dict[Fraction, tuple[tuple, int]] = {}
        for value, (sample_rep, count) in state.items():
            for c in range(max_coeff + 1):
                new_value = value + Fraction(c) * mono_value
                new_rep = sample_rep + (c,)
                if new_value not in next_state:
                    next_state[new_value] = (new_rep, count)
                else:
                    existing_rep, existing_count = next_state[new_value]
                    next_state[new_value] = (existing_rep, existing_count + count)
        state = next_state

    return state


def generate_n0_qr(
    q: Fraction,
    r: Fraction,
    max_degree_q: int,
    max_degree_r: int,
    max_coeff: int,
) -> dict[Fraction, tuple[tuple[tuple[int, int, int], ...], int]]:
    """Generate bounded elements of N0[q, r] with exact rational arithmetic.

    Elements have the form  sum_{i,j} a_{i,j} * q^i * r^j
    where 0 <= i <= max_degree_q, 0 <= j <= max_degree_r,
    and 0 <= a_{i,j} <= max_coeff.

    Returns a dict mapping each distinct Fraction value to a pair:
      (sample_representation, total_count)
    where sample_representation is a tuple of (i, j, coeff) triples for
    nonzero coefficients only, and total_count is the number of distinct
    coefficient assignments producing that value.

    Zero is stored with empty representation.
    """
    q_powers = powers(q, max_degree_q)
    r_powers = powers(r, max_degree_r)

    state: dict[Fraction, tuple[tuple, int]] = {Fraction(0): ((), 1)}

    for i in range(max_degree_q + 1):
        for j in range(max_degree_r + 1):
            mono_value = q_powers[i] * r_powers[j]
            next_state: dict[Fraction, tuple[tuple, int]] = {}
            for value, (sample_rep, count) in state.items():
                for c in range(max_coeff + 1):
                    new_value = value + Fraction(c) * mono_value
                    new_rep = sample_rep if c == 0 else sample_rep + ((i, j, c),)
                    if new_value not in next_state:
                        next_state[new_value] = (new_rep, count)
                    else:
                        existing_rep, existing_count = next_state[new_value]
                        next_state[new_value] = (existing_rep, existing_count + count)
            state = next_state

    return state


def summarize_generation(elements: dict[Fraction, tuple[tuple, int]]) -> dict[str, int]:
    """Return summary statistics for a generation result.

    Keys returned:
      total_distinct_elements
      total_representations
      collisions
      max_representations_for_one_element
    """
    total_distinct = len(elements)
    total_reps = sum(count for _, count in elements.values())
    collisions = sum(1 for _, count in elements.values() if count > 1)
    max_reps = max((count for _, count in elements.values()), default=0)

    return {
        "total_distinct_elements": total_distinct,
        "total_representations": total_reps,
        "collisions": collisions,
        "max_representations_for_one_element": max_reps,
    }
