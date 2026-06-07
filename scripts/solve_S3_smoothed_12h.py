"""
solve_S3_smoothed.py — Solve the S3 with smoothed heat demand profile
This represents smart heat pump control with building thermal mass + buffer storage
"""
import pypsa
from pathlib import Path
import time
import sys

SCENARIO_NAME = 'S3_smoothed_12h'

INPUT_PATH = Path("/mnt/c/Users/bekba/Desktop/electrification_scenarios/prenetwork_S3_smoothed_12h.nc")
OUTPUT_PATH = Path("/mnt/c/Users/bekba/Desktop/electrification_solved/solved_S3_smoothed_12h.nc")

OUTPUT_PATH.parent.mkdir(exist_ok=True, parents=True)

# Same solver options as before, with loose tolerance for faster convergence
SOLVER_OPTIONS = {
    'solver': 'ipm',
    'run_crossover': 'off',
    'parallel': 'on',
    'threads': 4,
    'presolve': 'on',
    'output_flag': True,
    'log_to_console': True,
    'ipm_optimality_tolerance': 1e-4,
}

print("="*80, flush=True)
print(f"SOLVING: {SCENARIO_NAME}", flush=True)
print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
print("="*80, flush=True)
print(f"Input:  {INPUT_PATH}", flush=True)
print(f"Output: {OUTPUT_PATH}", flush=True)
print()

if OUTPUT_PATH.exists():
    print(f"Output file already exists. Delete to re-solve:", flush=True)
    print(f"  {OUTPUT_PATH}", flush=True)
    sys.exit(0)

if not INPUT_PATH.exists():
    print(f"ERROR: Input file not found: {INPUT_PATH}", flush=True)
    sys.exit(1)

print("Loading network...", flush=True)
n = pypsa.Network(str(INPUT_PATH))

# Verify the smoothed demand is in place
heat_loads = n.loads[n.loads.carrier.str.contains('heat', case=False)]
peak = n.loads_t.p_set[heat_loads.index].sum(axis=1).max() / 1e3
print(f"  Verified peak heat demand: {peak:.0f} GW (expected ~163 GW for smoothed)", flush=True)
print(f"  Snapshots: {len(n.snapshots)}", flush=True)
print(f"  Links: {len(n.links)}", flush=True)
print()

print("Starting optimization...", flush=True)
print(f"Expected time: 8-12 hours with tolerance 1e-4", flush=True)
print("─"*80, flush=True)

start = time.time()

try:
    status, condition = n.optimize(
        solver_name='highs',
        solver_options=SOLVER_OPTIONS,
    )
    
    elapsed_hours = (time.time() - start) / 3600
    
    print()
    print("="*80, flush=True)
    print(f"SOLVED in {elapsed_hours:.2f} hours", flush=True)
    print(f"Finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("="*80, flush=True)
    print(f"  Status:    {status}", flush=True)
    print(f"  Condition: {condition}", flush=True)
    print(f"  Objective: €{n.objective/1e9:.2f} bn/yr", flush=True)
    print()
    
    hp_cap = n.links[n.links.carrier.str.contains('heat pump', case=False)].p_nom_opt.sum() / 1e3
    res_cap = n.links[n.links.carrier.str.contains('resistive', case=False)].p_nom_opt.sum() / 1e3
    gas_chp_cap = n.links[n.links.carrier.str.contains('gas CHP', case=True, regex=False)].p_nom_opt.sum() / 1e3
    wind = n.generators[n.generators.carrier.str.contains('wind|onwind|offwind', case=False)].p_nom_opt.sum() / 1e3
    solar = n.generators[n.generators.carrier.str.contains('solar', case=False)].p_nom_opt.sum() / 1e3
    thermal_storage = n.stores[n.stores.carrier.str.contains('water', case=False)].e_nom_opt.sum() / 1e3
    
    print(f"  Heat pumps:          {hp_cap:.1f} GW (S3 original: 92.5 GW)", flush=True)
    print(f"  Resistive heaters:   {res_cap:.1f} GW (S3 original: 58.3 GW)", flush=True)
    print(f"  Gas CHP:             {gas_chp_cap:.1f} GW (S3 original: 191.1 GW)", flush=True)
    print(f"  Wind:                {wind:.1f} GW (S3 original: 119.3 GW)", flush=True)
    print(f"  Solar:               {solar:.1f} GW (S3 original: 234.9 GW)", flush=True)
    print(f"  Thermal storage:     {thermal_storage:.0f} GWh (S3 original: 3,171 GWh)", flush=True)
    print()
    
    n.export_to_netcdf(str(OUTPUT_PATH))
    print(f"Saved to: {OUTPUT_PATH}", flush=True)
    
except Exception as e:
    print(f"FAILED: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
