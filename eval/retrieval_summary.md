# Retrieval evaluation

Hit = a top-k chunk from the expected document whose pages include the expected page. `multi` is strict (both passages in the top k); partial = share of passages found.

## Hit rate (all answerable questions)

| Design | n | hit@1 | hit@3 | hit@5 | words@1 | words@3 | words@5 |
|---|---|---|---|---|---|---|---|
| fixed | 26 | 58% | 69% | 81% | 150 | 450 | 750 |
| structured | 26 | 77% | 88% | 100% | 196 | 584 | 984 |

## By question kind

| Design | kind | n | hit@1 | hit@3 | hit@5 | partial@1 | partial@3 | partial@5 |
|---|---|---|---|---|---|---|---|---|
| fixed | single | 20 | 75% | 90% | 95% | 75% | 90% | 95% |
| fixed | multi | 6 | 0% | 0% | 33% | 42% | 50% | 67% |
| structured | single | 20 | 100% | 100% | 100% | 100% | 100% | 100% |
| structured | multi | 6 | 0% | 50% | 100% | 33% | 75% | 100% |

## Misses at k = 5

- **fixed**: q03 (expected GEVO2026 p.27, ranks -, top-1 GEVO2026 p.16-17), q21 (expected GEVO2025 p.16; GEVO2026 p.16, ranks -; 1, top-1 GEVO2026 p.16-17), q22 (expected GEVO2025 p.16; GEVO2026 p.19, ranks -; 1, top-1 GEVO2026 p.18-19), q23 (expected GEVO2025 p.17; GEVO2026 p.21, ranks -; 2, top-1 GEVO2025 p.25), q24 (expected GEVO2025 p.47; GEVO2026 p.93, ranks -; 1, top-1 GEVO2026 p.93-94)
- **structured**: none
