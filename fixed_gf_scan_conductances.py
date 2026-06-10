from gfs_version_2 import gfs_object as fixed_gap_gfs_object
import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from pathlib import Path
import math

OUT_DIR = Path('/home/joncineus/Spring2026-CompNeuro/jalcineus-penalab-cns-rescience-project/')

LANDSCAPE_CACHE = OUT_DIR / 'brian2_fixed_gap_latency_landscapes.npz'
LANDSCAPE_PNG = OUT_DIR / 'brian2_fixed_gap_latency_landscapes.png'
FORCE_RECOMPUTE_LANDSCAPES = False
landscape_errors = []

SIM_DT = 0.005 * ms
PAPER_STIM = 120 * nA
PAPER_DUR = 0.03 * ms
PAPER_MUSCLE_DELAY_MS = 0.35
RUN_AFTER = 5 * ms

def _peak(mon):
    arr = np.asarray(mon.v / mV)
    return float(np.nanmax(arr)) if arr.size else math.nan

def _minv(mon):
    arr = np.asarray(mon.v / mV)
    return float(np.nanmin(arr)) if arr.size else math.nan

def _finite(mon):
    arr = np.asarray(mon.v / mV)
    return bool(np.isfinite(arr).all())

# The standalone comparison script defines this, but this notebook runs in its
# own kernel. Keep it local here so landscape recomputation does not silently
# collapse to NaN.
PAPER_MUSCLE_DELAY_MS = globals().get('PAPER_MUSCLE_DELAY_MS', 0.35)

landscape_gap_ns = np.array([20.0, 34.5, 70.0, 105.0, 135.0, 160.0])
landscape_specs = [
    {
        'key': 'gnatbar',
        'label': 'gNa,t (mS/cm^2)',
        'values': np.array([230.0, 300.0, 380.0, 460.0, 520.0]),
        'unit': mS / cm**2,
        'baseline': 300.0,
    },
    {
        'key': 'gkbar',
        'label': 'gK (mS/cm^2)',
        'values': np.array([1.0, 5.0, 10.0, 16.0, 24.0]),
        'unit': mS / cm**2,
        'baseline': 10.0,
    },
    {
        'key': 'gleak',
        'label': 'gleak (mS/cm^2)',
        'values': np.array([0.0, 0.01, 0.03, 0.06, 0.095]),
        'unit': mS / cm**2,
        'baseline': 0.03,
    },
]

LANDSCAPE_TARGETS_MS = {'TTMn': 0.93, 'DLMn': 1.44}

def _peak_latency_for_landscape(mon, threshold=-30.0):
    t = np.asarray(mon.t / ms)
    v = np.asarray(mon.v / mV)
    if v.size == 0 or not np.isfinite(v).any():
        return math.nan
    if np.nanmax(v) <= threshold:
        return math.nan
    _, time_idx = np.unravel_index(np.nanargmax(v), v.shape)
    return float(t[time_idx] + PAPER_MUSCLE_DELAY_MS)

def _run_fixed_landscape_point(param_key, param_value, gap_ns):
    start_scope()
    defaultclock.dt = SIM_DT
    try:
        obj = fixed_gap_gfs_object()
        obj.set_param('g_gap', gap_ns * nS)
        obj.set_param(param_key, param_value)
        obj.setup_monitors()
        obj.GF.I_inj[0] = PAPER_STIM
        obj.net.run(PAPER_DUR)
        obj.GF.I_inj[0] = 0 * amp
        obj.net.run(5 * ms)
        return _peak_latency_for_landscape(obj.mon_ttm), _peak_latency_for_landscape(obj.mon_dlmn)
    except Exception as exc:
        landscape_errors.append(f'{param_key}={param_value}, g_gap={gap_ns} nS: {type(exc).__name__}: {exc}')
        return math.nan, math.nan

def compute_landscape_results():
    results = {'gap_ns': landscape_gap_ns}
    for spec in landscape_specs:
        ttm = np.full((len(landscape_gap_ns), len(spec['values'])), np.nan)
        dlm = np.full_like(ttm, np.nan)
        for yi, gap_ns in enumerate(landscape_gap_ns):
            for xi, value in enumerate(spec['values']):
                ttm[yi, xi], dlm[yi, xi] = _run_fixed_landscape_point(
                    spec['key'], value * spec['unit'], gap_ns
                )
        results[f"{spec['key']}_values"] = spec['values']
        results[f"{spec['key']}_TTMn"] = ttm
        results[f"{spec['key']}_DLMn"] = dlm
    return results

def _cache_has_finite_latencies(results):
    latency_keys = [key for key in results if key.endswith('_TTMn') or key.endswith('_DLMn')]
    return any(np.isfinite(results[key]).any() for key in latency_keys)

if LANDSCAPE_CACHE.exists() and not FORCE_RECOMPUTE_LANDSCAPES:
    loaded = np.load(LANDSCAPE_CACHE)
    landscape_results = {key: loaded[key] for key in loaded.files}
    if not _cache_has_finite_latencies(landscape_results):
        print('Landscape cache had no finite latencies; recomputing it now.')
        landscape_results = compute_landscape_results()
        np.savez(LANDSCAPE_CACHE, **landscape_results)
else:
    landscape_results = compute_landscape_results()
    np.savez(LANDSCAPE_CACHE, **landscape_results)

if landscape_errors:
    print('Landscape calculation warnings/errors:')
    for message in landscape_errors[:10]:
        print('  ', message)
    if len(landscape_errors) > 10:
        print(f'  ... {len(landscape_errors) - 10} more')

fig, axes = plt.subplots(2, 3, figsize=(15.5, 8.8), sharey=True, constrained_layout=True)
for col, spec in enumerate(landscape_specs):
    xs = landscape_results[f"{spec['key']}_values"]
    ys = landscape_results['gap_ns']
    X, Y = np.meshgrid(xs, ys)
    for row, output in enumerate(['TTMn', 'DLMn']):
        ax = axes[row, col]
        Z = np.ma.masked_invalid(landscape_results[f"{spec['key']}_{output}"])
        if Z.count() == 0:
            ax.text(0.5, 0.5, 'No finite latencies', ha='center', va='center', transform=ax.transAxes)
            continue
        finite = np.asarray(Z.compressed(), dtype=float)
        levels = np.linspace(np.nanmin(finite), np.nanmax(finite), 13)
        if np.allclose(levels[0], levels[-1]):
            levels = np.linspace(levels[0] - 0.05, levels[0] + 0.05, 13)
        cf = ax.contourf(X, Y, Z, levels=levels, cmap='viridis')
        ax.contour(X, Y, Z, levels=levels[::3], colors='white', linewidths=0.5, alpha=0.7)
        target = LANDSCAPE_TARGETS_MS[output]
        if np.nanmin(finite) <= target <= np.nanmax(finite):
            ax.contour(X, Y, Z, levels=[target], colors='red', linewidths=1.6, linestyles='--')
        ax.axhline(135, color='tab:blue', lw=1.4, ls=':', label='young gap')
        ax.axhline(34.5, color='tab:orange', lw=1.4, ls=':', label='old gap')
        ax.scatter([spec['baseline']], [135], color='tab:blue', edgecolor='white', s=38, zorder=5)
        ax.scatter([spec['baseline']], [34.5], color='tab:orange', edgecolor='white', s=38, zorder=5)
        ax.set_title(f'{output} latency vs {spec["key"]}')
        ax.set_xlabel(spec['label'])
        if col == 0:
            ax.set_ylabel('g_gap (nS)')
        cbar = fig.colorbar(cf, ax=ax, shrink=0.86)
        cbar.set_label('Latency (ms)')

handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles[:2], labels[:2], loc='upper center', ncol=2, frameon=False)
fig.suptitle('Brian2 fixed-copy latency landscapes, paper gap units', fontsize=15)
fig.savefig(LANDSCAPE_PNG, dpi=180, bbox_inches='tight')
plt.show()

print(f'Saved landscape figure: {LANDSCAPE_PNG}')
print(f'Saved landscape cache:  {LANDSCAPE_CACHE}')

# Create a plot showing latency differences between old and young flies
fig_diff, axes_diff = plt.subplots(1, 3, figsize=(15.5, 4.4), sharey=True, constrained_layout=True)
young_gap_idx = np.where(landscape_gap_ns == 135.0)[0][0]
old_gap_idx = np.where(landscape_gap_ns == 34.5)[0][0]

for col, spec in enumerate(landscape_specs):
    ax = axes_diff[col]
    xs = landscape_results[f"{spec['key']}_values"]
    
    for row, output in enumerate(['TTMn', 'DLMn']):
        young_latencies = landscape_results[f"{spec['key']}_{output}"][young_gap_idx, :]
        old_latencies = landscape_results[f"{spec['key']}_{output}"][old_gap_idx, :]
        latency_diff = young_latencies - old_latencies
        
        linestyle = '-' if output == 'TTMn' else '--'
        label = f'{output} (young - old)'
        ax.plot(xs, latency_diff, linestyle=linestyle, linewidth=2, label=label, marker='o')
    
    ax.axhline(0, color='black', linestyle='-', linewidth=0.8, alpha=0.3)
    ax.set_xlabel(spec['label'])
    ax.set_title(f'Latency difference vs {spec["key"]}')
    ax.legend()
    if col == 0:
        ax.set_ylabel('Latency difference (ms)')
    ax.grid(True, alpha=0.3)

fig_diff.suptitle('Latency differences: Young (gap=135 nS) vs Old (gap=34.5 nS)', fontsize=15)
latency_diff_png = OUT_DIR / 'brian2_fixed_gap_latency_differences.png'
fig_diff.savefig(latency_diff_png, dpi=180, bbox_inches='tight')
plt.show()

print(f'Saved latency difference figure: {latency_diff_png}')