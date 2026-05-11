from fractions import Fraction

from crowdmath2026.rationals import fraction_to_str, fraction_sort_key


def associate_closure_in_sample(
    x: Fraction,
    units: set[Fraction],
    sample: set[Fraction],
) -> set[Fraction]:
    """Return all elements u*x that lie in the sample, for u in units.

    Zero is excluded. Uses exact Fraction arithmetic.

    This is a bounded operation: elements u*x that fall outside the bounded
    sample are not included, even if they would be theoretical associates.
    """
    zero = Fraction(0)
    closure: set[Fraction] = set()
    for u in units:
        candidate = u * x
        if candidate != zero and candidate in sample:
            closure.add(candidate)
    return closure


def group_associate_classes(
    sample: set[Fraction],
    units: set[Fraction],
) -> list[set[Fraction]]:
    """Partition the nonzero sample into associate classes under the given unit set.

    Two nonzero elements a, b are in the same sample associate class if
    there exists a unit u in units such that u*a = b (and u*a is in the sample).

    Uses union-find via a greedy connected-components approach:
    - For each element, compute its associate closure within the sample.
    - Merge sets that share any element.

    Returns a list of sets; each set is one sample associate class.
    Sort the list by the canonical (smallest) representative of each class.

    If units = {1}, every class is a singleton.

    This is a bounded grouping: an infinite associate class may appear split
    into multiple smaller classes if some unit multiples lie outside the sample.
    """
    zero = Fraction(0)
    nonzero = {x for x in sample if x != zero}

    # Build adjacency: x ~ y if y = u*x for some unit u in sample
    assigned: dict[Fraction, int] = {}  # element -> class index
    classes: list[set[Fraction]] = []

    for x in sorted(nonzero, key=fraction_sort_key):
        if x in assigned:
            continue
        # BFS from x
        component: set[Fraction] = set()
        queue: list[Fraction] = [x]
        visited: set[Fraction] = {x}
        while queue:
            current = queue.pop()
            component.add(current)
            neighbors = associate_closure_in_sample(current, units, nonzero)
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        class_idx = len(classes)
        classes.append(component)
        for el in component:
            assigned[el] = class_idx

    # Sort by canonical representative
    classes.sort(key=lambda cls: fraction_sort_key(canonical_representative(cls)))
    return classes


def canonical_representative(cls: set[Fraction]) -> Fraction:
    """Return the smallest element of the associate class by exact numeric value."""
    return min(cls, key=fraction_sort_key)


def class_summary(classes: list[set[Fraction]]) -> dict[str, int]:
    """Return aggregate statistics for a list of associate classes.

    Returns:
      num_classes            : total number of classes
      singleton_classes      : classes with exactly one element
      non_singleton_classes  : classes with two or more elements
      largest_class_size     : size of the largest class
    """
    sizes = [len(cls) for cls in classes]
    return {
        "num_classes": len(classes),
        "singleton_classes": sum(1 for s in sizes if s == 1),
        "non_singleton_classes": sum(1 for s in sizes if s > 1),
        "largest_class_size": max(sizes) if sizes else 0,
    }
