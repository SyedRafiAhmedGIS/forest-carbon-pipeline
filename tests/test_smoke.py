import json
import os
import shutil

import numpy as np
import pytest

pytest.importorskip("nbformat")
import nbformat

EXPECTED_NOTEBOOKS = {
    "00_Smart_Upload_Preview.ipynb",
    "01_Masking_Demarcation.ipynb",
    "02_Classification_Clustering.ipynb",
    "03_Clubbing_Stratification.ipynb",
    "04_Field_Plots_Ground_Truth.ipynb",
    "05_RF_Modeling.ipynb",
    "06_Carbon_Output.ipynb",
    "99_Master_Orchestrator.ipynb",
}


def _nb_path(name):
    return os.path.join("notebooks", name)


def test_01_notebook_suite_complete():
    assert set(os.listdir("notebooks")) == EXPECTED_NOTEBOOKS


def test_02_notebooks_valid_nbformat():
    for name in EXPECTED_NOTEBOOKS:
        nb = nbformat.read(_nb_path(name), as_version=4)
        nbformat.validate(nb)


def test_03_no_stale_outputs():
    for name in EXPECTED_NOTEBOOKS:
        with open(_nb_path(name)) as f:
            nb = json.load(f)
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                assert cell.get("outputs") == []
                assert cell.get("execution_count") is None


def test_04_sequential_cell_ids():
    for name in EXPECTED_NOTEBOOKS:
        with open(_nb_path(name)) as f:
            nb = json.load(f)
        for i, cell in enumerate(nb["cells"], start=1):
            assert cell["metadata"]["id"] == f"cell-{i}"


def test_05_username_hardcoded():
    with open("README.md") as f:
        readme = f.read()
    assert "SyedRafiAhmedGIS" in readme
    for bad in ("YOUR-GITHUB-USERNAME", "TODO", "XXX"):
        assert bad not in readme


def test_06_fsi_threshold_documented():
    with open(os.path.join("src", "phase4_model.py")) as f:
        assert "30 cm CBH" in f.read()


def test_07_quarantine_logic_exists():
    with open(os.path.join("src", "phase1_demarcate.py")) as f:
        code = f.read().lower()
    assert "quarantine" in code and "json" in code


def test_08_public_api_imports():
    from src import (calculate_carbon_output, classify_spectral_types,
                     clubbing_stratification, demarcate_forest_pixels,
                     generate_field_campaign, model_forest_stock)
    from src.phase1_demarcate import demarcate_forest_pixels as direct
    assert direct is demarcate_forest_pixels
    for fn in (demarcate_forest_pixels, classify_spectral_types,
               clubbing_stratification, generate_field_campaign,
               model_forest_stock, calculate_carbon_output):
        assert callable(fn)


@pytest.fixture(scope="module")
def pipeline():
    """Run the full 6-phase pipeline once; assertions share the result."""
    from src import (calculate_carbon_output, classify_spectral_types,
                     clubbing_stratification, demarcate_forest_pixels,
                     generate_field_campaign, model_forest_stock)

    np.random.seed(42)
    nir = np.random.uniform(0.2, 0.8, (100, 100))
    red = np.random.uniform(0.05, 0.3, (100, 100))
    savi = ((nir - red) / (nir + red + 0.5)) * 1.5
    mask, ndvi, _ = demarcate_forest_pixels(nir, red, quarantine_dir="quarantine_test")
    type_map, density_map = classify_spectral_types(ndvi, savi, mask)
    stratum_map, allocation = clubbing_stratification(type_map, density_map)
    plots = generate_field_campaign(ndvi, savi, mask, stratum_map)
    rf, agb_map, mean_r2, std_r2 = model_forest_stock(plots, ndvi, savi, stratum_map)
    carbon_map, metadata = calculate_carbon_output(agb_map, commit_sha="test")
    yield mask, stratum_map, allocation, agb_map, mean_r2, metadata
    if os.path.isdir("quarantine_test"):
        shutil.rmtree("quarantine_test")


def test_09_pipeline_metrics_match_readme_claims(pipeline):
    mask, stratum_map, allocation, agb_map, mean_r2, metadata = pipeline
    assert 0.55 <= mean_r2 <= 0.75                     # README promises R^2 ~ 0.66
    forest = agb_map > 0
    assert agb_map[forest].min() >= 16 and agb_map[forest].max() <= 112
    assert 0.40 <= mask.mean() <= 0.90
    assert set(allocation) == set(np.unique(stratum_map[stratum_map > 0]).tolist())


def test_10_carbon_math_is_ipcc_consistent(pipeline):
    _, _, _, _, _, metadata = pipeline
    ratio = metadata["total_co2e_tCO2e"] / metadata["total_carbon_tC"]
    assert ratio == pytest.approx(44 / 12, rel=1e-3)
    assert metadata["ipcc_carbon_fraction"] == 0.47
    assert 16 <= metadata["mean_agb_t_ha"] <= 112
