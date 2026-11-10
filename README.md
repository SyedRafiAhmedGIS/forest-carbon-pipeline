# Forest Stock Mapping Carbon Monitoring Pipeline

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/99_Master_Orchestrator.ipynb)
[![CI Guardrails](https://github.com/SyedRafiAhmedGIS/forest-carbon-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/SyedRafiAhmedGIS/forest-carbon-pipeline/actions)

![Pipeline Demo](docs/pipeline_demo.gif)

## Overview
A scalable, reproducible, and open-source Remote Sensing & GIS pipeline for forest inventory and carbon accounting. Built to transition from sparse manual sample plots to continuous, full-map accuracy for climate reporting and carbon credit auditing.

## Interactive Notebooks
| # | Phase | Notebook | Open in Colab |
|---|---|---|:-:|
| 00 | Smart Upload & Preview | `00_Smart_Upload_Preview.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/00_Smart_Upload_Preview.ipynb) |
| 01 | Masking & Demarcation | `01_Masking_Demarcation.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/01_Masking_Demarcation.ipynb) |
| 02 | Classification & Clustering | `02_Classification_Clustering.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/02_Classification_Clustering.ipynb) |
| 03 | Clubbing & Stratification | `03_Clubbing_Stratification.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/03_Clubbing_Stratification.ipynb) |
| 04 | Field Plots & Ground Truth | `04_Field_Plots_Ground_Truth.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/04_Field_Plots_Ground_Truth.ipynb) |
| 05 | RF Modeling | `05_RF_Modeling.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/05_RF_Modeling.ipynb) |
| 06 | Carbon Output | `06_Carbon_Output.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/06_Carbon_Output.ipynb) |
| 99 | Master Orchestrator (All Phases) | `99_Master_Orchestrator.ipynb` | [![Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SyedRafiAhmedGIS/forest-carbon-pipeline/blob/main/notebooks/99_Master_Orchestrator.ipynb) |

## Hour 1: See it work
1. Click the **Master Orchestrator** Colab badge above.
2. `Runtime → Run all`.
3. Confirm the 6-phase execution runs automatically on synthetic data.
*Expected output: CV R² ≈ 0.66 ± 0.08, AGB map 16–112 t/ha, 0 quarantine errors.*

## Architecture & 6-Phase Design
1. **Masking**: Dynamic NDVI thresholding (forest if NDVI > 0.3), SAVI with L = 0.5, quarantine gate on >50% NoData.
2. **Classification**: K-Means spectral TYPEs (k=3) + FSI canopy-density legend: VDF ≥70%, MDF 40-70%, OF 10-40%.
3. **Clubbing**: TYPE x DENSITY matrix overlay, stratum id = type x 10 + density, plot budget proportional to stratum area.
4. **Field Plots**: 20x20m plots (0.04 ha), Indian FSI 30 cm CBH maturity rule, plots need >= 3 mature stems.
5. **RF Modeling**: Random Forest (300 trees) on [ndvi, savi, stratum], 5-fold CV (measured R² ≈ 0.66), predicts AGB for every forest pixel.
6. **Carbon Output**: tC = AGB x 0.47 (IPCC 2006), CO2e = tC x 44/12 computed exactly, totals on true 0.04 ha pixels, Git SHA + input-hash provenance.

Every notebook is standalone: the bootstrap cell locates the repo (or clones it in Colab) and each notebook re-runs its upstream phases deterministically (seed 42).

## Setup & Cloning
```bash
git clone https://github.com/SyedRafiAhmedGIS/forest-carbon-pipeline.git
cd forest-carbon-pipeline
pip install -r requirements.txt
pytest tests/ -v
```
