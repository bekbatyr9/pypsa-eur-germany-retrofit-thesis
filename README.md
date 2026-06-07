# Techno-Economic Analysis of Building Retrofit on German Power Systems

MSc Thesis — Erasmus Mundus Smart Cities and Communities (2026)  
Université de Mons (UMons), Belgium  
**Author:** Bek Batyrbek  
**Supervisors:** Dr. Pietro Favaro · Dr. Zacharie De Grève

---

## Overview

This repository contains all materials for the MSc thesis quantifying 
how building-envelope retrofit and heat-pump electrification interact 
at the German national power-system level under the 2050 net-zero 
constraint, using the open-source PyPSA-Eur sector-coupled 
capacity-expansion model.

---

## Repository Contents

| Folder / File | Description |
|---|---|
| `analysis/` | Jupyter notebook with complete analysis and figures |
| `config/` | PyPSA-Eur configuration files for all six primary scenarios |
| `networks/` | Solved PyPSA-Eur networks for all eight scenarios (~25 MB each) |
| `docs/` | Methodology notes |

---

## Scenario Design

| Scenario | Retrofit | Gas Boilers | Description |
|---|---|---|---|
| S0 | 0% | Allowed | Baseline — no policy |
| S1 | 29% | Allowed | Insulation only |
| S2 | 0% | Banned | Electrification only |
| S3-Low | 15% | Banned | Combined — low (1%/yr) |
| S3 | 29% | Banned | Combined — moderate (2%/yr) |
| S3-High | 45% | Banned | Combined — high (3%/yr) |
| S3-Smooth-12h | 29% | Banned | + building thermal mass smoothing |
| S3-Smooth-24h | 29% | Banned | + thermal mass and buffer storage |

---

## Key Results

**System costs:**

| Scenario | System Cost (€ bn/yr) |
|---|---|
| S0 Baseline | 84.5 |
| S1 Insulation | 68.0 |
| S2 Heat Pumps | 86.0 |
| S3-Low (15%) | 77.2 |
| S3 (29%) | 69.2 |
| S3-High (45%) | 60.5 |
| S3-Smooth-12h | 52.2 |
| S3-Smooth-24h | 51.4 |

**Cost-benefit analysis** (conservative accounting, bill savings excluded):

| Renovation Rate | Net Benefit (€ bn/yr) | BCR |
|---|---|---|
| 1%/yr — 15% retrofit | +3.1 | 1.37 |
| 2%/yr — 29% retrofit | −13.4 | 0.64 |
| 3%/yr — 45% retrofit | −63.5 | 0.36 |

**Four key findings:**
1. Marginal system value of retrofit: ~€0.5 bn/yr per percentage 
   point — linear across 0–45%, no diminishing returns
2. Heat pumps cost-optimal at 69–81% share across all scenarios 
   regardless of explicit policy mandates
3. Flexibility-retrofit substitution: heat-pump grid smoothing 
   drops from 20.7% (S0) to 1.4% (S3-High) as retrofit deepens
4. Smart control with building thermal mass alone reduces system 
   cost 25% (€17 bn/yr); buffer storage adds only marginal savings

---

## Reproducing the Results

### Requirements
- PyPSA-Eur v1.1.2 · linopy v0.6.4 · HiGHS solver · Python 3.10+
- ~12–15 hours compute per scenario (4 cores, 11 GB RAM + 8 GB swap)

### Using the Solved Networks (Quickest)

Clone the repo and open the notebook directly:

```bash
git clone https://github.com/bekbatyr9/germany-retrofit-thesis.git
cd germany-retrofit-thesis
jupyter notebook analysis/
```

All eight solved networks are in `networks/`. Load any network:

```python
import pypsa
n = pypsa.Network("networks/S3_combined_moderate_s_5___2050.nc")
```

### Re-Solving From Scratch

1. Install PyPSA-Eur: https://pypsa-eur.readthedocs.io
2. Copy configs from `config/` to your PyPSA-Eur config directory
3. Run:
```bash
pixi run snakemake -j4 solve_sector_networks \
  --configfile config/config.DE.S3.yaml
```

---

## Policy Recommendations

1. **BMWK**: Target 2%/yr renovation rate with industrial 
   cost-reduction policies (prefabricated insulation, serial 
   deep-retrofit programs)
2. **GEG/EPBD**: Sequence envelope retrofit before the 2028 
   boiler ban; tie heat-pump subsidies to EPC-D minimum threshold
3. **BNetzA**: Require renovation-rate and smart-control 
   scenarios in the Network Development Plan

---
