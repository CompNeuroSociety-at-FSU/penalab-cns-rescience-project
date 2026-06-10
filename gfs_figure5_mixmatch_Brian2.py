from brian2 import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from gfs_plot_helpers import run_trial, sweep_2d, sweep_1d

matplotlib.rcParams['svg.fonttype'] = 'none'
prefs.codegen.target = 'numpy'
defaultclock.dt = 0.01*ms


def contour_levels(matrix, n=20):
    lo = float(np.nanmin(matrix))
    hi = float(np.nanmax(matrix))
    if np.isclose(lo, hi):
        return None
    return np.linspace(lo, hi, n)


def main():
    # Panel C style: compare medial vs lateral dendrite length impact.
    med_vals = np.arange(20, 110, 5) * um
    lat_vals = np.arange(10, 70, 5) * um

    print('Running Figure 5 dendrite sweeps...', flush=True)
    ttm_med, dlm_med = sweep_1d('TTMn_med_L', med_vals)
    ttm_lat, dlm_lat = sweep_1d('TTMn_lat_L', lat_vals)

    # Panel E style: GF length/diameter map at old-age gap conductance.
    gf_len_vals = np.arange(200, 620, 20) * um
    gf_diam_vals = np.arange(3.0, 14.0, 0.5) * um

    print('Running Figure 5 GF length/diameter sweep...', flush=True)
    _, dlm_gf_map = sweep_2d(
        'GF_L',
        gf_len_vals,
        'GF_diam',
        gf_diam_vals,
        base_params={'g_gap': 34.5 * uS},
        penalty_ms=5.0,
    )

    # Random mix-and-match sample for sensitivity overview.
    rng = np.random.default_rng(2026)
    n_samples = 80
    rand_lat = np.full(n_samples, np.nan)
    rand_gap = np.full(n_samples, np.nan)
    rand_med = np.full(n_samples, np.nan)

    print('Running Figure 5 random mix-and-match samples...', flush=True)
    for i in range(n_samples):
        p = {
            'g_gap': rng.uniform(20.0, 150.0) * uS,
            'gnatbar': rng.uniform(0.23, 0.53) * siemens / cm**2,
            'gkbar': rng.uniform(0.001, 0.025) * siemens / cm**2,
            'gleak': rng.uniform(0.0, 100e-6) * siemens / cm**2,
            'TTMn_med_L': rng.uniform(20.0, 100.0) * um,
            'TTMn_lat_L': rng.uniform(10.0, 60.0) * um,
            'GF_diam': rng.uniform(3.0, 13.0) * um,
            'GF_L': rng.uniform(200.0, 600.0) * um,
        }
        out = run_trial(params=p)
        rand_lat[i] = 5.0 if not np.isfinite(out['DLMn_latency_ms']) else out['DLMn_latency_ms']
        rand_gap[i] = float(p['g_gap'] / uS)
        rand_med[i] = float(p['TTMn_med_L'] / um)

    fig = plt.figure(figsize=(13, 9))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(np.asarray(med_vals / um), dlm_med, 'o-', label='vary TTMn_med_L')
    ax1.plot(np.asarray(lat_vals / um), dlm_lat, 's--', label='vary TTMn_lat_L')
    ax1.set_title('Figure 5C style: dendrite length effect on DLMn latency')
    ax1.set_xlabel('Length (um)')
    ax1.set_ylabel('DLMn latency (ms)')
    ax1.grid(alpha=0.25)
    ax1.legend(fontsize=8)

    ax2 = fig.add_subplot(2, 2, 2)
    levels = contour_levels(dlm_gf_map)
    if levels is not None:
        c = ax2.contour(dlm_gf_map, levels=levels, colors='k', linewidths=0.8)
        ax2.clabel(c, inline=1, fontsize=7)
    else:
        ax2.text(0.5, 0.5, 'No contour variation', transform=ax2.transAxes, ha='center', va='center')
    ax2.set_title('Figure 5E style: GF length vs GF diameter (old g_gap)')
    ax2.set_xlabel('GF_diam (um)')
    ax2.set_ylabel('GF_L (um)')
    x_step = max(1, len(gf_diam_vals) // 6)
    y_step = max(1, len(gf_len_vals) // 6)
    ax2.set_xticks(range(0, len(gf_diam_vals), x_step))
    ax2.set_yticks(range(0, len(gf_len_vals), y_step))
    ax2.set_xticklabels([f"{v:.1f}" for v in np.asarray(gf_diam_vals[::x_step] / um)])
    ax2.set_yticklabels([f"{v:.0f}" for v in np.asarray(gf_len_vals[::y_step] / um)])

    ax3 = fig.add_subplot(2, 1, 2)
    sc = ax3.scatter(rand_gap, rand_lat, c=rand_med, cmap='viridis', s=24, alpha=0.8)
    ax3.set_title('Figure 5 random mix-and-match: DLMn latency vs g_gap (color = TTMn_med_L)')
    ax3.set_xlabel('g_gap (uS)')
    ax3.set_ylabel('DLMn latency (ms)')
    ax3.grid(alpha=0.25)
    cbar = fig.colorbar(sc, ax=ax3)
    cbar.set_label('TTMn_med_L (um)')

    fig.tight_layout()
    fig.savefig('figure5_mixmatch_brian2.png', dpi=200)
    plt.close(fig)

    print('Saved figure5_mixmatch_brian2.png', flush=True)
    print(f'Dendrite med latency range: {np.nanmin(dlm_med):.4f} to {np.nanmax(dlm_med):.4f} ms', flush=True)
    print(f'GF map latency range: {np.nanmin(dlm_gf_map):.4f} to {np.nanmax(dlm_gf_map):.4f} ms', flush=True)


if __name__ == '__main__':
    main()
