"""Phase 3 - Clubbing & Stratification: TYPE x DENSITY matrix overlay."""
import numpy as np

DENSITY_LEGEND = {3: "VDF (>=70%)", 2: "MDF (40-70%)", 1: "OF (10-40%)"}


def clubbing_stratification(type_map, density_map, n_target_plots=100):
    """Overlay the forest TYPE map (1-3) with the DENSITY map (1-3).

    Stratum id = type * 10 + density (e.g. 23 = type 2, VDF). Field-plot
    effort is allocated proportionally to stratum area with a floor of 2
    plots per active stratum; Phase 4 drops the plots this budget defines.
    """
    forest = (type_map > 0) & (density_map > 0)
    stratum_map = np.zeros(type_map.shape, dtype=int)
    stratum_map[forest] = type_map[forest] * 10 + density_map[forest]

    ids, counts = np.unique(stratum_map[forest], return_counts=True)
    total = int(counts.sum())
    allocation = {int(sid): max(2, int(round(n_target_plots * n / total)))
                  for sid, n in zip(ids, counts)}

    print(f"Phase 3 complete. Matrix overlay: {len(ids)} active strata, "
          f"{n_target_plots}-plot budget allocated.")
    print(f"{'stratum':>7} | {'type':>4} | {'density':>11} | {'pixels':>7} | {'share':>6} | plots")
    for sid, n in zip(ids, counts):
        print(f"{int(sid):>7} | {int(sid) // 10:>4} | {DENSITY_LEGEND[int(sid) % 10]:>11} | "
              f"{int(n):>7} | {n / total * 100:>5.1f}% | {allocation[int(sid)]}")
    return stratum_map, allocation
