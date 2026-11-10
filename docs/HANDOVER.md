# Forest Carbon Pipeline - Handover Guide

**Audience:** any analyst picking this repository up cold.
**Promise:** same-day time-to-productivity.

## Hour 1: The Quickstart
1. Click the **Master Orchestrator** Colab badge on the README.
2. `Runtime -> Run all`.
3. Confirm the 6-phase summary block prints with the metrics listed in the README. Zero external setup required.

## Day 1: Code as Documentation
1. Clone the repo, `pip install -r requirements.txt`.
2. Run `pytest tests/ -v` - 10 guardrails must pass, including a live pipeline run.
3. Work through notebooks 00-06 in order; each one is standalone and re-runs its upstream phases.

## Week 1: Prove the System
1. Ship one real configuration change via Pull Request.
2. Prove the architecture accepts modification safely without breaking the quarantine gate.
3. Swap the synthetic scene for a real Sentinel-2 tile in notebook 01 and watch the quarantine gate do its job on any bad input.

## Phase Map
| Notebook | Phase | Key artefact |
|---|---|---|
| 00 | Upload & preview | `data/field_plot_template.csv` |
| 01 | Masking & demarcation | `forest_mask`, `input_hash` |
| 02 | Classification & clustering | `type_map`, `density_map` |
| 03 | Clubbing & stratification | `stratum_map`, plot allocation |
| 04 | Field plots & ground truth | `plots` (30 cm CBH FSI rule) |
| 05 | RF modelling | `agb_map`, CV R-squared |
| 06 | Carbon output | CO2e totals + provenance metadata |
| 99 | Master orchestrator | one-click end-to-end run |
