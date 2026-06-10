from brian2 import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from gfs_plot_helpers import sweep_2d

matplotlib.rcParams['svg.fonttype'] = 'none'
prefs.codegen.target = 'numpy'
defaultclock.dt = 0.01*ms


PARAM_SCANS = {
    'PSI_diam': np.arange(1.0, 8.5, 0.5) * um,
    'TTMn_med_L': np.arange(20, 110, 5) * um,
    'GF_diam': np.arange(3.0, 13.5, 0.5) * um,
}


def format_values(values, unit):
    arr = np.asarray(values / unit, dtype=float)
    return [f"{v:.2f}".rstrip('0').rstrip('.') for v in arr]


def contour_levels(matrix, n=20):
    lo = float(np.nanmin(matrix))
    hi = float(np.nanmax(matrix))
    if np.isclose(lo, hi):
        return None
    return np.linspace(lo, hi, n)


def main():
    g_gap_vals = np.arange(20, 160, 10) * uS

    fig = plt.figure(figsize=(14, 8))
    panel = 1

    for param_x, x_vals in PARAM_SCANS.items():
        print(f'Running Figure 4 scan: g_gap vs {param_x}', flush=True)
        ttm, dlm = sweep_2d(
            'g_gap',
            g_gap_vals,
            param_x,
            x_vals,
            penalty_ms=5.0,
            run_kwargs={
                'dt_schedule': (0.0025 * ms, 0.001 * ms, 0.0005 * ms),
                'verbose_retries': False,
            },
        )

        ax1 = fig.add_subplot(2, 3, panel)
        lev1 = contour_levels(ttm)
        if lev1 is not None:
            c1 = ax1.contour(ttm, levels=lev1, colors='k', linewidths=0.8)
            ax1.clabel(c1, inline=1, fontsize=7)
        else:
            ax1.text(0.5, 0.5, 'No contour variation', transform=ax1.transAxes, ha='center', va='center')

        ax1.set_title(f'TTMn: g_gap vs {param_x}')
        ax1.set_xlabel(param_x)
        ax1.set_ylabel('g_gap (uS)')
        ax1.set_xticks(range(0, len(x_vals), max(1, len(x_vals) // 6)))
        ax1.set_yticks(range(0, len(g_gap_vals), 2))

        if param_x.endswith('diam'):
            x_unit = um
        else:
            x_unit = um

        ax1.set_xticklabels(format_values(x_vals[::max(1, len(x_vals) // 6)], x_unit))
        ax1.set_yticklabels(format_values(g_gap_vals[::2], uS))

        ax2 = fig.add_subplot(2, 3, panel + 3)
        lev2 = contour_levels(dlm)
        if lev2 is not None:
            c2 = ax2.contour(dlm, levels=lev2, colors='k', linewidths=0.8)
            ax2.clabel(c2, inline=1, fontsize=7)
        else:
            ax2.text(0.5, 0.5, 'No contour variation', transform=ax2.transAxes, ha='center', va='center')

        ax2.set_title(f'DLMn: g_gap vs {param_x}')
        ax2.set_xlabel(param_x)
        ax2.set_ylabel('g_gap (uS)')
        ax2.set_xticks(range(0, len(x_vals), max(1, len(x_vals) // 6)))
        ax2.set_yticks(range(0, len(g_gap_vals), 2))
        ax2.set_xticklabels(format_values(x_vals[::max(1, len(x_vals) // 6)], x_unit))
        ax2.set_yticklabels(format_values(g_gap_vals[::2], uS))

        print(
            f'{param_x} diagnostics -> '
            f'TTMn min/max: {np.nanmin(ttm):.4f}/{np.nanmax(ttm):.4f} ms, '
            f'DLMn min/max: {np.nanmin(dlm):.4f}/{np.nanmax(dlm):.4f} ms',
            flush=True,
        )

        panel += 1

    fig.suptitle('Figure 4 style: anatomy vs g_gap (contour lines only)', fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig('figure4_anatomy_brian2.png', dpi=200)
    plt.close(fig)

    print('Saved figure4_anatomy_brian2.png', flush=True)


if __name__ == '__main__':
    main()
