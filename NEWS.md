# NEWS

## [1.0.2] - 2026-11-10
- Bootstrap: locate repo up-tree -> `git clone --depth 1` in Colab -> explicit RuntimeError. Verified against a simulated fresh Colab clone (8/8 notebooks).
- All 8 notebooks are standalone: each re-runs its upstream phases deterministically (seed 42).
- Random Forest now drives the map: per-pixel AGB = rf.predict([ndvi, savi, stratum]); FSI 30 cm CBH rule filters qualifying plots (>= 3 mature stems).
- IPCC math exact: tC = AGB x 0.47, CO2e = tC x 44/12 computed in code (replaces rounded 1.725 / 1.7253 constants).
- Pixel area restored to 20 x 20 m = 0.04 ha; Phase 3 emits type x 10 + density strata with a proportional plot budget.
- Removed the unconditional "Environment: Google Colab" print.

## [1.0.1] - 2026-11-10
- Bootstrap walks up the directory tree; sys.path.insert(0, repo_root) prevents shadowing.

## [1.0.0] - 2026-11-10
- Initial release. Multi-notebook suite (00-06, 99).
- Username SyedRafiAhmedGIS hardcoded.
