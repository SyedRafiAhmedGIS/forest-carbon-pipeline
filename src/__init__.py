"""Forest Carbon Pipeline - src package.

Phase modules use phaseN_ prefix names (valid Python identifiers), so plain
imports work. This __init__ re-exports the public API so that both
`from src import model_forest_stock` and
`from src.phase4_model import model_forest_stock` resolve.
"""
from .phase1_demarcate import demarcate_forest_pixels
from .phase2_preprocess import classify_spectral_types
from .phase3_clubbing import clubbing_stratification
from .phase4_model import generate_field_campaign, model_forest_stock
from .phase5_carbon import calculate_carbon_output

__all__ = [
    "demarcate_forest_pixels",
    "classify_spectral_types",
    "clubbing_stratification",
    "generate_field_campaign",
    "model_forest_stock",
    "calculate_carbon_output",
]
