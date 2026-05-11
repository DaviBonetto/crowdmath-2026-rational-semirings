# Experiment 004 — Bounded Factorization Search

## Purpose

This experiment searches for bounded additive factorizations in $\mathbb{N}_0[q]$ and records the universal multiplicative identity from Exercise 1.7. It provides bounded computational witnesses for two key claims:
1. When $q = a/b$ with $a,b > 1$, the additive monoid $(\mathbb{N}_0[q],+)$ admits multiple factorization lengths for the same element.
2. The multiplicative identity $(1+q+q^2)(1+q^3) = (1+q^2+q^4)(1+q)$ is the exact obstruction showing $(\mathbb{N}_0[q]\setminus\{0\},\cdot)$ is not a UFM.

## Bounded Warning

> **This is a bounded computational sample. It does not prove atomicity, unique factorization, IDF behavior, or any infinite mathematical property.**

Additive factorization results are bounded by `max_atom_degree` and `max_factorization_length`. The multiplicative identity computation is exact for any given $q$, not bounded.

## Parameters

- `max_atom_degree = 5`
- `max_factorization_length = 12`
- `max_solutions = 50`
- Atoms from `theoretical_atoms_n0q(q, max_atom_degree)` (Exercise 1.8)

## Additive Factorization Search

| q | target | theoretical case | factorizations found | length set | interpretation |
|---|---|---|---|---|---|
| 2 | 6 | integer | 1 | [6] | q=2: N0[q]=N0. |
| 1/2 | N/A | reciprocal_integer | 0 | [] | q=1/2: N0[q] has no atoms by Exercise 1. |
| 3/2 | 3 | mixed_fraction | 2 | [2, 3] | q=3/2: additive identity a=bq gives 3=2*(3/2). |
| 2/3 | 2 | mixed_fraction | 6 | [2, 3, 4, 5, 6, 7] | q=2/3: additive identity a=bq gives 2=3*(2/3). |
| 4/9 | 4 | mixed_fraction | 2 | [4, 9] | q=4/9: additive identity a=bq gives 4=9*(4/9). |
| 5/3 | 5 | mixed_fraction | 2 | [3, 5] | q=5/3: additive identity a=bq gives 5=3*(5/3). |

## Multiplicative Universal Identity

| q | left factorization | right factorization | common value | identity holds |
|---|---|---|---|---|
| 3/2 | (19/4) · (35/8) | (133/16) · (5/2) | 665/32 | True |
| 2/3 | (19/9) · (35/27) | (133/81) · (5/3) | 665/243 | True |
| 4/9 | (133/81) · (793/729) | (8113/6561) · (13/9) | 105469/59049 | True |
| 5/3 | (49/9) · (152/27) | (931/81) · (8/3) | 7448/243 | True |

## Interpretation

**q = 2:** $\mathbb{N}_0[2] = \mathbb{N}_0$. Additive factorization behaves like $\mathbb{N}_0$, where the only atom is $1$. UFM baseline case per Exercise 1.7.\n\n**q = 1/2:** The monoid $(\mathbb{N}_0[1/2],+)$ has no atoms by Exercise 1.8. Atom-factorization search is not meaningful and is skipped.

**q = a/b with a, b > 1 (3/2, 2/3, 4/9, 5/3):** The additive identity $a = bq$ gives bounded witnesses of non-unique additive factorization: $\underbrace{1+\cdots+1}_{a} = \underbrace{q+\cdots+q}_{b}$. Multiple factorization lengths appear in the bounded search.

**Multiplicative identity:** $(1+q+q^2)(1+q^3) = (1+q^2+q^4)(1+q)$ is the exact symbolic obstruction used in Exercise 1.7. Both products factor the element $1+q+q^2+q^3+q^4+q^5$ in two distinct ways in $(\mathbb{N}_0[q]\setminus\{0\},\cdot)$.\n\n**These computations are sanity checks and evidence organization, not proofs.**

## Next Experiments

- `exp_002_detect_units_in_bounded_samples.py` — identify units in bounded samples.
- `exp_003_group_associate_classes.py` — group elements by associate classes.
- `exp_008_valuation_patterns.py` — analyze valuation patterns.
- `exp_007_idf_sanity_checks.py` — IDF sanity checks.
