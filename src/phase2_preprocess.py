"""Phase 2 - Classification & Clustering: K-Means types + canopy density classes."""
import numpy as np
from sklearn.cluster import KMeans


def classify_spectral_types(ndvi, savi, forest_mask):
    """Cluster forest pixels into 3 spectral TYPEs (K-Means) and classify each
    pixel into the FSI canopy-density legend from an NDVI cover proxy:

        VDF (>=70% cover) | MDF (40-70%) | OF (10-40%)

    Returns (type_map, density_map). Future redesign: supervised U-Net CNN
    with skip connections.
    """
    feats = np.column_stack((ndvi[forest_mask], savi[forest_mask]))
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(feats)

    type_map = np.zeros(ndvi.shape, dtype=int)
    type_map[forest_mask] = labels + 1

    cover_pct = np.clip((ndvi - 0.2) / 0.5, 0, 1) * 100  # NDVI -> canopy cover proxy
    density_map = np.zeros(ndvi.shape, dtype=int)
    f = forest_mask
    density_map[f] = ((cover_pct[f] >= 70) * 3
                      + ((cover_pct[f] >= 40) & (cover_pct[f] < 70)) * 2
                      + ((cover_pct[f] >= 10) & (cover_pct[f] < 40)) * 1)

    for d, name in ((3, "VDF (>=70%)"), (2, "MDF (40-70%)"), (1, "OF (10-40%)")):
        share = (density_map == d).sum() / max(int(f.sum()), 1) * 100
        print(f"Phase 2 complete. {name}: {share:.1f}% of forest pixels")
    return type_map, density_map
