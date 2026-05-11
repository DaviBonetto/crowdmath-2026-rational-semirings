# Experiment 001 — Bounded Element Generation for N0[q] and N0[q,r]

## Purpose

Experiment 001 generates bounded finite samples of elements of $\mathbb{N}_0[q]$ and $\mathbb{N}_0[q,r]$ using exact rational arithmetic (`fractions.Fraction`). It records distinct values, representation counts, and collisions. A collision means that the same rational number is reached by more than one bounded polynomial coefficient tuple. Collisions indicate multiple bounded polynomial representations of the same rational element. They are useful computational signals, but they do not by themselves prove failure of unique factorization. This is infrastructure for future experiments on atoms, factorizations, units, and IDF.

## Parameters

**N0[q]:** `max_degree = 4`, `max_coeff = 3`

**N0[q,r]:** `max_degree_q = 3`, `max_degree_r = 3`, `max_coeff = 2`

## N0[q] Results

| q | Distinct elements | Total reps | Collisions | Max reps per element |
|---|---|---|---|---|
| 2 | 94 | 1024 | 90 | 16 |
| 1/2 | 94 | 1024 | 90 | 16 |
| 3/2 | 454 | 1024 | 262 | 8 |
| 2/3 | 454 | 1024 | 262 | 8 |

## N0[q,r] Results

| q | r | Distinct elements | Total reps | Collisions | Max reps per element |
|---|---|---|---|---|---|
| 2/3 | 3/5 | 30117 | 43046721 | 29415 | 4485 |
| 3/2 | 5/3 | 30117 | 43046721 | 29415 | 4485 |
| 1/2 | 1/3 | 1201 | 43046721 | 1197 | 67271 |

## Warning

> **This is a bounded computational sample. It does not prove atomicity, unique factorization, IDF behavior, or any infinite mathematical property.**

All outputs are finite samples bounded by degree and coefficient constraints. No infinite properties (atomicity, UFM, IDF) are inferred from these results.

## Next Experiments

- `exp_002_detect_units_in_bounded_samples.py` — identify units within bounded samples.
- `exp_004_bounded_factorization_search.py` — search for additive factorizations within bounded sets.
- `exp_005_candidate_atom_detection.py` — identify candidate atoms: elements with no nontrivial decomposition in the sample.
