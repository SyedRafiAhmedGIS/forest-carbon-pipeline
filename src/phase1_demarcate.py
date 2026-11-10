"""Phase 1 - Masking & Demarcation: NDVI forest threshold + quarantine gate."""
import hashlib
import json
import os

import numpy as np

NDVI_THRESHOLD = 0.3


def demarcate_forest_pixels(nir_band, red_band, quarantine_dir="quarantine"):
    """Return (forest_mask, ndvi, input_hash) for a NIR/Red scene pair.

    Rasters that are more than 50% NoData never reach Phase 2: a diagnostic
    JSON is written to the quarantine log and ValueError is raised.
    """
    os.makedirs(quarantine_dir, exist_ok=True)
    input_hash = hashlib.md5(nir_band.tobytes() + red_band.tobytes()).hexdigest()
    nan_ratio = float(np.isnan(nir_band).sum()) / nir_band.size
    if nan_ratio > 0.5:
        with open(os.path.join(quarantine_dir, "diag_01.json"), "w") as qf:
            json.dump({"error": "Excessive NoData",
                       "nan_ratio": round(nan_ratio, 3),
                       "input_hash": input_hash}, qf, indent=2)
        raise ValueError("Raster exceeds NoData limit - routed to quarantine log.")
    ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)
    forest_mask = ndvi > NDVI_THRESHOLD
    coverage = forest_mask.sum() / forest_mask.size * 100
    print(f"Phase 1 complete. Forest coverage: {coverage:.1f}% | input hash: {input_hash[:8]}")
    return forest_mask, ndvi, input_hash
