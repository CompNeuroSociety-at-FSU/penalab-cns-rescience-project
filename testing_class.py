# This is where the class based ong the giant fiber system will be tested and worked on, so in the separate file
# So yeah

from brian2 import *
import matplotlib
import numpy
import gfs_version_2

if __name__ == "__main__":
    example_1 = gfs_version_2.gfs_object()
    print(example_1.gf_neuron)
    print(example_1.psi_neuron)
    print(example_1.dlmn_neuron)
    print(example_1.ttm_neuron)


    example_1.setup_monitors()


    ## AI GENERATED CODE, BEWARE
    ## WARNING THIS CODE WAS AI Generated for testinf purpose's only
    # Run the simulation with a 1.5 nA zap for 3 milliseconds
    example_1.inject_and_run(current_amp=1.5*nA, pulse_duration=3*ms)

    # --- Plotting the DLMn results directly from the class attributes ---
    import matplotlib.pyplot as plt

    print(f"Number of data points recorded: {len(example_1.mon_dlmn_dend.t)}")

    plt.plot(example_1.mon_dlmn_dend.t/ms, example_1.mon_dlmn_dend.v[0]/mV, label='DLMn Dendrite Tip')
    plt.plot(example_1.mon_dlmn_axon.t/ms, example_1.mon_dlmn_axon.v[0]/mV, label='DLMn Axon Terminal')
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.legend()
    plt.show()