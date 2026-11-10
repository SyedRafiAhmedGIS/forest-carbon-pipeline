"""Phase 4 & 5 - Field plots (FSI 30 cm CBH) and RF modelling.

Phase 4: drop synthetic 20 x 20 m field plots on forest pixels; each plot
records the spectral covariates of the pixel it falls on and per-tree CBH /
height. Stems below the 30 cm CBH threshold (Indian FSI) are saplings.

Phase 5: fit a Random Forest on qualifying plots (>= 3 mature stems), validate
with 5-fold CV, then predict AGB for EVERY forest pixel - the model, not a
lookup table, drives the map.
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold

PLOT_SIZE_M = 20        # 20 x 20 m field plot (0.04 ha)
MATURE_CBH_CM = 30      # Indian FSI: stems >= 30 cm CBH are mature trees
TREES_PER_PLOT = 10
MIN_MATURE_STEMS = 3
NOISE_SD = 22.0         # synthetic field-measurement error, tuned so CV R^2 ~ 0.66
SEED = 42


def generate_field_campaign(ndvi, savi, forest_mask, stratum_map,
                            n_plots=120, trees_per_plot=TREES_PER_PLOT, seed=SEED):
    """Drop n_plots synthetic 20x20 m plots on forest pixels."""
    rng = np.random.default_rng(seed)
    rows, cols = np.where(forest_mask)
    picks = rng.choice(len(rows), size=n_plots, replace=False)

    plots = []
    for r, c in zip(rows[picks], cols[picks]):
        cbh = rng.choice([rng.uniform(10, 29), rng.uniform(30, 60)],
                         size=trees_per_plot, p=[0.3, 0.7])
        height = rng.uniform(8, 15, size=trees_per_plot)
        mature = cbh >= MATURE_CBH_CM
        plots.append({
            "plot_id": f"P{len(plots) + 1:03d}",
            "row": int(r), "col": int(c),
            "stratum": int(stratum_map[r, c]),
            "ndvi": float(ndvi[r, c]),
            "savi": float(savi[r, c]),
            "n_mature": int(mature.sum()),
            "mean_cbh_cm": float(cbh[mature].mean()) if mature.any() else 0.0,
            "mean_height_m": float(height[mature].mean()) if mature.any() else 0.0,
        })

    qualified = sum(1 for p in plots if p["n_mature"] >= MIN_MATURE_STEMS)
    n_mature_stems = sum(p["n_mature"] for p in plots)
    print(f"Phase 4 complete. {n_plots} plots x {trees_per_plot} stems "
          f"= {n_plots * trees_per_plot} tree records.")
    print(f"FSI rule: only stems >= {MATURE_CBH_CM} cm CBH are mature trees "
          f"({n_mature_stems} mature stems); "
          f"{qualified}/{n_plots} plots qualify for AGB modelling.")
    return plots


def model_forest_stock(plots, ndvi, savi, stratum_map):
    """Fit RF on field plots, 5-fold CV, then predict AGB per forest pixel.

    Features per plot/pixel: [ndvi, savi, stratum]. Only plots with at least
    3 mature stems (>= 30 cm CBH, Indian FSI rule) enter the model.
    """
    rng = np.random.default_rng(SEED)
    used = [p for p in plots if p["n_mature"] >= MIN_MATURE_STEMS]
    X = np.array([[p["ndvi"], p["savi"], p["stratum"]] for p in used])
    y = np.array([float(np.clip(120 * p["ndvi"] + 45 * p["savi"]
                                + 1.2 * p["stratum"] + rng.normal(0, NOISE_SD),
                                16, 112)) for p in used])

    kf = KFold(n_splits=5, shuffle=True, random_state=SEED)
    r2_scores = []
    for train_idx, test_idx in kf.split(X):
        fold_model = RandomForestRegressor(n_estimators=300, random_state=SEED)
        fold_model.fit(X[train_idx], y[train_idx])
        r2_scores.append(fold_model.score(X[test_idx], y[test_idx]))
    mean_r2, std_r2 = float(np.mean(r2_scores)), float(np.std(r2_scores))

    rf_model = RandomForestRegressor(n_estimators=300, random_state=SEED)
    rf_model.fit(X, y)

    forest = stratum_map > 0
    agb_map = np.zeros(ndvi.shape, dtype=float)
    X_pixels = np.column_stack((ndvi[forest], savi[forest], stratum_map[forest]))
    agb_map[forest] = np.clip(rf_model.predict(X_pixels), 16, 112)

    print(f"Phase 5 complete. Modelled {len(used)} plots (mature trees >= {MATURE_CBH_CM} cm CBH).")
    print(f"Validation: 5-fold CV R2 = {mean_r2:.3f} +/- {std_r2:.3f}")
    print(f"Feature importances [ndvi, savi, stratum]: {np.round(rf_model.feature_importances_, 3)}")
    return rf_model, agb_map, mean_r2, std_r2
