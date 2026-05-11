from fractions import Fraction


def integer_prime_factorization(n: int) -> dict[int, int]:
    """Return the prime factorization of a positive integer n.

    Examples:
      12 -> {2: 2, 3: 1}
       1 -> {}

    Raises ValueError for n < 1.
    """
    if n < 1:
        raise ValueError(f"Expected a positive integer, got {n!r}.")
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def _is_prime(p: int) -> bool:
    """Return True iff p is prime (trial division)."""
    if p < 2:
        return False
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    d = 3
    while d * d <= p:
        if p % d == 0:
            return False
        d += 2
    return True


def valuation(x: Fraction, p: int) -> int:
    """Return the p-adic valuation v_p(x) for a nonzero rational x.

    For x = a/b in lowest terms:
      v_p(x) = v_p(a) - v_p(b)
    where v_p(n) is the exponent of p in the prime factorization of n.

    Raises:
      ValueError if x == 0.
      ValueError if p is not prime.
    """
    if x == Fraction(0):
        raise ValueError("valuation is not defined for zero.")
    if not _is_prime(p):
        raise ValueError(f"{p} is not prime.")

    a = abs(x.numerator)
    b = x.denominator  # always positive for Fraction in lowest terms

    def count_p(n: int) -> int:
        count = 0
        while n > 0 and n % p == 0:
            count += 1
            n //= p
        return count

    return count_p(a) - count_p(b)


def support_primes(x: Fraction) -> set[int]:
    """Return the set of primes appearing in the numerator or denominator of x.

    For x = 1, returns the empty set.
    Raises ValueError for x == 0.
    """
    if x == Fraction(0):
        raise ValueError("support_primes is not defined for zero.")
    a = abs(x.numerator)
    b = x.denominator
    primes: set[int] = set()
    primes.update(integer_prime_factorization(a).keys())
    primes.update(integer_prime_factorization(b).keys())
    return primes


def valuation_vector(x: Fraction, primes: list[int]) -> tuple[int, ...]:
    """Return the tuple (v_p1(x), ..., v_pk(x)) for the given list of primes.

    Uses exact Fraction arithmetic; each component is an integer.
    """
    return tuple(valuation(x, p) for p in primes)


def valuation_summary(
    elements: set[Fraction],
    primes: list[int],
) -> dict[str, object]:
    """Compute aggregate valuation statistics over a set of nonzero elements.

    Returns a dict with:
      num_elements      : int
      primes            : list[int]
      valuation_ranges  : {p: {min, max, distinct_count}} for each prime
      vector_count      : int  (number of distinct valuation vectors)
      zero_excluded     : bool (True: zero was excluded before calling)
    """
    zero = Fraction(0)
    nonzero = [x for x in elements if x != zero]
    zero_excluded = any(x == zero for x in elements)

    per_prime: dict[int, list[int]] = {p: [] for p in primes}
    vectors: set[tuple[int, ...]] = set()

    for x in nonzero:
        vec = valuation_vector(x, primes)
        vectors.add(vec)
        for p, v in zip(primes, vec):
            per_prime[p].append(v)

    ranges: dict[str, dict[str, int]] = {}
    for p in primes:
        vals = per_prime[p]
        if vals:
            ranges[str(p)] = {
                "min": min(vals),
                "max": max(vals),
                "distinct_count": len(set(vals)),
            }
        else:
            ranges[str(p)] = {"min": 0, "max": 0, "distinct_count": 0}

    return {
        "num_elements": len(nonzero),
        "primes": primes,
        "valuation_ranges": ranges,
        "vector_count": len(vectors),
        "zero_excluded": zero_excluded,
    }
