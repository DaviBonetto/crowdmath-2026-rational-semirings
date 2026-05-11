from fractions import Fraction


def parse_fraction(value: str | int) -> Fraction:
    """Parse a string or integer into a Fraction.

    Accepts formats: "2", "3/2", "1/3", 2.
    Raises ValueError if the input cannot be parsed.
    """
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        value = value.strip()
        if "/" in value:
            parts = value.split("/")
            if len(parts) != 2:
                raise ValueError(f"Cannot parse fraction: {value!r}")
            try:
                return Fraction(int(parts[0]), int(parts[1]))
            except (ValueError, ZeroDivisionError) as exc:
                raise ValueError(f"Cannot parse fraction: {value!r}") from exc
        try:
            return Fraction(int(value))
        except ValueError as exc:
            raise ValueError(f"Cannot parse fraction: {value!r}") from exc
    raise ValueError(f"Expected str or int, got {type(value).__name__}: {value!r}")


def fraction_to_str(x: Fraction) -> str:
    """Return a human-readable string for a Fraction.

    Returns "n" if denominator is 1, else "n/d".
    """
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def fraction_sort_key(x: Fraction) -> tuple[int, int]:
    """Return a sorting key for a Fraction based on its numeric value.

    Uses (numerator * sign, denominator) so that exact comparison is preserved.
    """
    return (x.numerator, x.denominator)
