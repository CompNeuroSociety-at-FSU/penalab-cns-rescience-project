#Created by Gillian Durta
from brian2 import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from gfs_version_2 import gfs_object

matplotlib.rcParams['svg.fonttype'] = 'none'
prefs.codegen.target = 'numpy'

# Initialize FULL Brian2 network

net = gfs_object()

GF = net.GF
TTMn = net.TTMn
PSI = net.PSI
DLMn = net.DLMn

ranges = {
    'g_gap': np.arange(20, 160, 10) * nS,
    'gnatbar': np.arange(230e-3, 530e-3, 20e-3) * mS/cm**2,
    'gkbar': np.arange(1e-3, 25e-3, 1e-3) * mS/cm**2,
    'gleak': np.arange(0, 100e-6, 5e-6) * mS/cm**2
}

param1 = 'g_gap'
param2s = ['gnatbar', 'gkbar', 'gleak']

# SIMPLE delay proxy (replace with real spike detection later)

def fake_delay():
    return 1 + 0.2*np.random.rand()


def run_scan(param1, vals1, param2, vals2):

    TTMn_delays = np.zeros((len(vals1), len(vals2)))
    DLMn_delays = np.zeros((len(vals1), len(vals2)))

    for i, v1 in enumerate(vals1):
        for j, v2 in enumerate(vals2):

            # -------------------------
            # RESET SIMULATION STATE
            # -------------------------
            GF.v = -70*mV
            TTMn.v = -70*mV
            PSI.v = -70*mV
            DLMn.v = -70*mV

            # -------------------------
            # SET PARAMETERS
            # -------------------------
            if param1 == 'g_gap':
                net.set_param('g_gap', v1)

            net.set_param(param2, v2)

            # Brief GF injection to evoke a spike, close to original stimulation style.
            GF.I_inj[0] = 5*nA
            net.net.run(0.03*ms)
            GF.I_inj[0] = 0*amp

            # -------------------------
            # RUN SIMULATION
            # -------------------------
            net.net.run(5*ms)

            # -------------------------
            # STORE RESULTS (placeholder)
            # -------------------------
            TTMn_delays[i, j] = fake_delay()
            DLMn_delays[i, j] = fake_delay() + 0.4

    return {
        'TTMn_delays': TTMn_delays,
        'DLMn_delays': DLMn_delays
    }



# RUN SCANS
fig1 = plt.figure(figsize=(15, 10))
ii = 1

for param2 in param2s:

    plt.subplot(2, 3, ii)

    delay_dict = run_scan(
        param1,
        ranges[param1],
        param2,
        ranges[param2]
    )

    # -------------------------
    # CLEAN DATA
    # -------------------------
    delay_dict['TTMn_delays'][delay_dict['TTMn_delays'] < 0] = np.nan
    delay_dict['DLMn_delays'][delay_dict['DLMn_delays'] < 0] = np.nan

    # -------------------------
    # PLOT TTMn
    # -------------------------
    plt.contour(np.log(delay_dict['TTMn_delays']), 25)
    plt.title(f"TTMn vs {param2}")

    plt.subplot(2, 3, ii + 3)

    # -------------------------
    # PLOT DLMn
    # -------------------------
    plt.contour(np.log(delay_dict['DLMn_delays']), 25)
    plt.title(f"DLMn vs {param2}")

    ii += 1

plt.tight_layout()
plt.savefig('gfs_param_scan_conductances_brian2.png')
plt.close(fig1)
