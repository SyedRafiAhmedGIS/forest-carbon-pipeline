"""Phase 6 - Carbon Output: IPCC conversion + provenance metadata."""
import hashlib

import numpy as np

IPCC_CARBON_FRACTION = 0.47   # IPCC 2006 Guidelines default (tropical forests)
C_TO_CO2 = 44.0 / 12.0        # molecular weight ratio, CO2 / C (= 3.666667)
PIXEL_AREA_HA = 0.04          # 20 x 20 m pixel grid


def calculate_carbon_output(agb_map, commit_sha="main"):
    """Convert the AGB map (t/ha) into carbon stock and CO2e totals.

    tC/ha = AGB x 0.47 (IPCC 2006 default) and tCO2e = tC x 44/12. Totals
    multiply by the real pixel area (0.04 ha), so stock figures are honest.
    The ratio is computed, not rounded into a constant.
    """
    forest = agb_map > 0
    carbon_tC_ha = agb_map * IPCC_CARBON_FRACTION
    co2e_t_ha = carbon_tC_ha * C_TO_CO2
    input_hash = hashlib.md5(agb_map.tobytes()).hexdigest()

    metadata = {
        "commit_sha": commit_sha,
        "input_hash": input_hash,
        "pixel_area_ha": PIXEL_AREA_HA,
        "forest_pixels": int(forest.sum()),
        "mean_agb_t_ha": round(float(agb_map[forest].mean()), 1) if forest.any() else 0.0,
        "total_agb_t": round(float(agb_map.sum() * PIXEL_AREA_HA), 1),
        "total_carbon_tC": round(float(carbon_tC_ha.sum() * PIXEL_AREA_HA), 1),
        "total_co2e_tCO2e": round(float(co2e_t_ha.sum() * PIXEL_AREA_HA), 1),
        "ipcc_carbon_fraction": IPCC_CARBON_FRACTION,
        "c_to_co2_ratio": round(C_TO_CO2, 4),
    }
    print(f"Phase 6 complete. Mean AGB {metadata['mean_agb_t_ha']} t/ha | "
          f"Stock {metadata['total_carbon_tC']} tC | "
          f"{metadata['total_co2e_tCO2e']} t CO2e (x{C_TO_CO2:.3f}, {PIXEL_AREA_HA} ha/pixel).")
    print(f"Provenance: commit={commit_sha} input_hash={input_hash[:8]}")
    return carbon_tC_ha, metadata
