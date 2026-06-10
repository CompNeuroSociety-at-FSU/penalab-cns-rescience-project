from brian2 import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from gfs_plot_helpers import run_trial, sweep_1d

matplotlib.rcParams['svg.fonttype'] = 'none'
prefs.codegen.target = 'numpy'
defaultclock.dt = 0.01*ms


def main():
    g_gap_values = np.arange(20, 170, 10) * uS
    young_gap = 135 * uS
    old_gap = 34.5 * uS

    print('Running Figure 2 gap-conductance sweep...', flush=True)
    ttm_lat, dlm_lat = sweep_1d('g_gap', g_gap_values)

    print('Running Figure 2 trace simulations...', flush=True)
    young_trace = run_trial(params={'g_gap': young_gap})
    old_trace = run_trial(params={'g_gap': old_gap})

    x_vals_uS = np.asarray(g_gap_values / uS, dtype=float)

    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(young_trace['t_ms'], young_trace['TTMn_mV'], label='TTMn young (135 uS)', color='tab:blue')
    ax1.plot(old_trace['t_ms'], old_trace['TTMn_mV'], '--', label='TTMn old (34.5 uS)', color='tab:blue', alpha=0.8)
    ax1.plot(young_trace['t_ms'], young_trace['DLMn_mV'], label='DLMn young (135 uS)', color='tab:orange')
    ax1.plot(old_trace['t_ms'], old_trace['DLMn_mV'], '--', label='DLMn old (34.5 uS)', color='tab:orange', alpha=0.8)
    ax1.axhline(-30.0, color='0.4', linestyle=':', linewidth=1.0, label='threshold')
    ax1.set_title('Figure 2B style: spikes over time (young vs old g_gap)')
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Voltage (mV)')
    ax1.grid(alpha=0.25)
    ax1.legend(fontsize=8, ncol=2)

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(x_vals_uS, ttm_lat, 'o-', color='tab:blue', label='TTMn latency')
    ax2.plot(x_vals_uS, dlm_lat, 's-', color='tab:orange', label='DLMn latency')
    ax2.axvline(float(young_gap / uS), color='tab:green', linestyle='--', linewidth=1.2, label='young 135 uS')
    ax2.axvline(float(old_gap / uS), color='tab:red', linestyle='--', linewidth=1.2, label='old 34.5 uS')
    ax2.set_title('Figure 2C style: latency vs gap-junction conductance')
    ax2.set_xlabel('g_gap (uS)')
    ax2.set_ylabel('Latency (ms)')
    ax2.grid(alpha=0.25)
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig('figure2_core_problem_brian2.png', dpi=200)
    plt.close(fig)

    print('Saved figure2_core_problem_brian2.png', flush=True)
    print(f'TTMn latency range: {np.nanmin(ttm_lat):.4f} to {np.nanmax(ttm_lat):.4f} ms', flush=True)
    print(f'DLMn latency range: {np.nanmin(dlm_lat):.4f} to {np.nanmax(dlm_lat):.4f} ms', flush=True)


if __name__ == '__main__':
    main()
