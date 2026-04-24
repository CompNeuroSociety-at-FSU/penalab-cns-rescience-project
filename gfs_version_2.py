# Jonathan Alcineus & Gillian Durta - 2026
# Here is the structure that I will create for the giant fiber system (GFS) of 
# Drosophila melanogaster, or adult fruit fly, In the original paper, the authors
# Used 4 neurons (The GF neuron, the TTM motoneuron (TTMn), 
# a peripherally synapsing interneuron (PSI), and a DLM motoneuron (DLMn)) to simulate
# this system, this is crucial to create the structure of the giant fiber system of for class
# and potentially create subclasses under this class for each of the type of neurons

# Gillian added the shapes of neurons PSI and DLMn

from brian2 import *
import matplotlib
import numpy

class gfs_object:
    # Paper designed experiment with using 4 neurons
    # Through further analysis of the paper, the authors' design for the neurons to have morphology to be composed of 
    # cylinders, usually relying on the axons and dendrites
    # No soma is necessary at all for function, like it is not necessary
    # The axon is the main core of the geometery, according the original paper's code

    # We'll have to use the Spatial Neuron class to account for the neurons' geometry

    def __init__(self):
        # Now we are getting to describe the shapes for each of the neurons, this is according to page 3 of the ENEURO Paper


        # The paper uses 51 iso-segments for the axons and dendrites (all of the cylindrical segments of the paper)
        # First we are putting the default morphology (or shape) for the gf neuron
        # The GF neuron does not contains any axons or dendrites, so one cylinder will represent this neuron
        # But it does have electrical synpases between the axon of the PSI and the dendrite of the TTmn
        self.gf_neuron_morph = Cylinder(diameter=8*um, length=400*um, n=51)


        # Here is the morphology for the TTMn neuron, it contains two dendrites and one active axon
        self.ttmn_neuron_morph = Cylinder(diameter=6*um, length=50*um, n=51)

        self.ttmn_neuron_morph.medial_dendrite = Cylinder(diameter=6*um, length=60*um, n=51)

        self.ttmn_neuron_morph.lateral_dendrite = Cylinder(diameter=6*um, length=30*um, n=51)


        # Here is the morphology for the PSI neuron, one axon and one dentrite
        self.psi_neuron_morph = Cylinder(diameter=4.5*um, length=90*um, n=51)

        self.psi_neuron_morph.dendrite = Cylinder(diameter=4.5*um, length=170*um, n=51)

        # Here is the morphology for the DLMn neuron, 2 diameters (one proximal one distal) and both one axon and dentrite
        # Nah, dude. The axon is tapered but the diameter for the neuron is not

        prox_diam = 2*um
        dist_diam = 4*um

        # Section with n compartments expects n+1 diameter values for tapering.
        axon_diameters = numpy.linspace(prox_diam/um, dist_diam/um, 52) * um

        axon_lengths = numpy.ones(51) * (50.0/51.0) * um
        self.dlmn_neuron_morph = Section(diameter=axon_diameters, length=axon_lengths, n=51)
       
        self.dlmn_neuron_morph.dendrite = Cylinder(diameter=2*um, length=100*um)


        # Here are the standard membrane properties, this shows how electricity will flow
        # through the neurons
        # Make sure to put the rest of the membrane properties from the paper



        # These are the most basic membrane properties from the paper
        self.leak_conductance = 0.03*mS / cm**2
        self.leak_reversal_potential = -85*mV
        self.specific_membrane_capitance = 1*uF /cm**2
        self.specific_axial_resistance = 35 * ohm * cm
        self.maximal_t_conductance = 300 * mS / cm**2
        self.maximal_p_conductance = 0.11*mS / cm**2
        self.maximal_v_conductance = 10*mS / cm**2
        self.young_gap_conductance = 135*uS
        self.old_gap_conductance = 34.5*uS
        self.chemical_synapse_rise = 0.1*ms
        self.chemical_synapse_decay = 1*ms
        self.chemical_synapse_reversal = 0*mV
        self.chemical_synapse_delay = 0.15*ms
        self.chemical_synapse_peak_conductance = 80*uS
        self.neuromuscular_junction_delay = 0.35*ms
        self.leak_reversal_potential = -85*mV
        self.sodium_reversal_potential = 65*mV
        self.potassium_reversal_potential = -74*mV


        # HH-like active membrane equations adapted from the original NEURON mechanisms.
        eqs_for_active = '''
        Im = gl*(El - v) + gnatbar*(m**3)*h*(E_Na - v) + gnapbar*p*(E_Na - v) + gkbar*n*(E_k - v) + I_gap/area + g_chem*(E_syn - v)/area + I_inj/area : amp/meter**2
        I_inj : amp (point current)
        I_gap : amp (point current)
        dg_chem/dt = -g_chem/tau_syn : siemens

        dm/dt = (m_inf - m)/m_tau : 1
        dh/dt = (h_inf - h)/h_tau : 1
        dn/dt = (n_inf - n)/n_tau : 1
        dp/dt = (p_inf - p)/p_tau : 1

        m_inf = 1/(1 + exp(clip((v - (-29.13*mV))/(-8.92*mV), -50, 50))) : 1
        h_inf = 1/(1 + exp(clip((v - (-47.0*mV))/(5.0*mV), -50, 50))) : 1
        n_inf = 1/(1 + exp(clip((v - (-12.85*mV))/(-19.91*mV), -50, 50))) : 1
        p_inf = 1/(1 + exp(clip((v - (-48.77*mV))/(-3.68*mV), -50, 50))) : 1

        m_tau = (0.13 + 3.43/(1 + exp(clip((v + 45.35*mV)/(5.98*mV), -50, 50))))*ms : second
        h_tau = (0.36 + exp(clip((v + 20.65*mV)/(-10.47*mV), -50, 50)))*ms : second
        n_tau = 1.0*ms : second
        p_tau = 1.0*ms : second

        gl : siemens/meter**2
        gnatbar : siemens/meter**2
        gnapbar : siemens/meter**2
        gkbar : siemens/meter**2
        E_Na : volt
        E_k : volt
        El : volt
        E_syn : volt
        tau_syn : second
        '''
        

        # Here are the neurons that will created from the number of neurons listed
        self.gf_neuron = SpatialNeuron(morphology=self.gf_neuron_morph, model=eqs_for_active,
                                       Cm=self.specific_membrane_capitance, Ri=self.specific_axial_resistance,
                                       method='exponential_euler', threshold='v > -20*mV', refractory=1*ms)
        self.ttm_neuron = SpatialNeuron(morphology=self.ttmn_neuron_morph, model=eqs_for_active,
                                        Cm=self.specific_membrane_capitance, Ri=self.specific_axial_resistance,
                                        method='exponential_euler', threshold='v > -20*mV', refractory=1*ms)
        self.psi_neuron = SpatialNeuron(morphology=self.psi_neuron_morph, model=eqs_for_active,
                                        Cm=self.specific_membrane_capitance, Ri=self.specific_axial_resistance,
                                        method='exponential_euler', threshold='v > -20*mV', refractory=1*ms)
        self.dlmn_neuron = SpatialNeuron(morphology=self.dlmn_neuron_morph, model=eqs_for_active,
                                         Cm=self.specific_membrane_capitance, Ri=self.specific_axial_resistance,
                                         method='exponential_euler', threshold='v > -20*mV', refractory=1*ms)

        self.params = {
            'g_gap': self.young_gap_conductance,
            'gnatbar': self.maximal_t_conductance,
            'gkbar': self.maximal_v_conductance,
            'gleak': self.leak_conductance,
        }

        for neuron in [self.gf_neuron, self.ttm_neuron, self.psi_neuron, self.dlmn_neuron]:
            neuron.gl = self.leak_conductance
            neuron.gnatbar = self.maximal_t_conductance
            neuron.gnapbar = self.maximal_p_conductance
            neuron.gkbar = self.maximal_v_conductance
            neuron.E_Na = self.sodium_reversal_potential
            neuron.E_k = self.potassium_reversal_potential
            neuron.El = self.leak_reversal_potential
            neuron.E_syn = self.chemical_synapse_reversal
            neuron.tau_syn = self.chemical_synapse_decay
            neuron.g_chem = 0*siemens
            neuron.I_gap = 0*amp
            neuron.I_inj = 0*amp
            neuron.m = 'm_inf'
            neuron.h = 'h_inf'
            neuron.n = 'n_inf'
            neuron.p = 'p_inf'

        self.GF = self.gf_neuron
        self.TTMn = self.ttm_neuron
        self.PSI = self.psi_neuron
        self.DLMn = self.dlmn_neuron

        self.setting_leak_reversal_potential()
        self.wiring_neurons()
        

    def setting_leak_reversal_potential(self):
        # Sets all of the starting voltage
        self.gf_neuron.v = self.leak_reversal_potential
        self.ttm_neuron.v = self.leak_reversal_potential
        self.psi_neuron.v = self.leak_reversal_potential
        self.dlmn_neuron.v = self.leak_reversal_potential

    # This is where I include the synapses that connected each of the
    # neurons, either through electrical of chemical connections
    # This is how the GFS will be wired
    def wiring_neurons(self):
        # Keep these values close to the original NEURON defaults.
        ttmn_syn_pre_loc = 1.0
        ttmn_syn_post_loc = 0.2
        psi_syn_pre_loc = 0.9
        psi_syn_post_loc = 0.5
        dlmn_syn_pre_loc = 0.85
        dlmn_syn_post_loc = 0.25

        gf_ttmn_delay = 1.0*ms
        gf_psi_delay = 1.0*ms
        psi_dlmn_delay = self.chemical_synapse_delay

        gf_ttmn_wt = 0.00
        gf_psi_wt = 0.00
        psi_dlmn_wt = 0.08

        gf_n = len(self.gf_neuron)
        ttmn_med_n = len(self.ttm_neuron.medial_dendrite)
        psi_n = len(self.psi_neuron)
        psi_den_n = len(self.psi_neuron.dendrite)
        dlmn_den_n = len(self.dlmn_neuron.dendrite)

        gf_ttmn_i = int(round(ttmn_syn_pre_loc * (gf_n - 1)))
        gf_psi_i = int(round(psi_syn_pre_loc * (gf_n - 1)))
        psi_dlmn_i = int(round(dlmn_syn_pre_loc * (psi_n - 1)))
        ttmn_j = int(round(ttmn_syn_post_loc * (ttmn_med_n - 1)))
        psi_j = int(round(psi_syn_post_loc * (psi_den_n - 1)))
        dlmn_j = int(round(dlmn_syn_post_loc * (dlmn_den_n - 1)))

        # NetCon-like event connections from the original model.
        self.GF_TTMn_con = Synapses(
            self.gf_neuron,
            self.ttm_neuron.medial_dendrite,
            model='w : siemens',
            on_pre='g_chem_post += w',
            delay=gf_ttmn_delay,
        )
        self.GF_TTMn_con.connect(i=[gf_ttmn_i], j=[ttmn_j])
        self.GF_TTMn_con.w = gf_ttmn_wt*uS

        self.GF_PSI_con = Synapses(
            self.gf_neuron,
            self.psi_neuron.dendrite,
            model='w : siemens',
            on_pre='g_chem_post += w',
            delay=gf_psi_delay,
        )
        self.GF_PSI_con.connect(i=[gf_psi_i], j=[psi_j])
        self.GF_PSI_con.w = gf_psi_wt*uS

        self.PSI_DLMn_con = Synapses(
            self.psi_neuron,
            self.dlmn_neuron.dendrite,
            model='w : siemens',
            on_pre='g_chem_post += w',
            delay=psi_dlmn_delay,
        )
        self.PSI_DLMn_con.connect(i=[psi_dlmn_i], j=[dlmn_j])
        self.PSI_DLMn_con.w = psi_dlmn_wt*uS

        # Gap currents mirror the original gap2 behavior: i = g*(v_pre - v_post).
        self.GF_TTMn_gap = Synapses(
            self.gf_neuron,
            self.ttm_neuron.medial_dendrite,
            model='g_gap : siemens\nI_gap_post = g_gap*(v_pre - v_post) : amp (summed)',
        )
        self.GF_TTMn_gap.connect(i=[gf_ttmn_i], j=[ttmn_j])
        self.GF_TTMn_gap.g_gap = self.young_gap_conductance

        self.GF_PSI_gap = Synapses(
            self.gf_neuron,
            self.psi_neuron.dendrite,
            model='g_gap : siemens\nI_gap_post = g_gap*(v_pre - v_post) : amp (summed)',
        )
        self.GF_PSI_gap.connect(i=[gf_psi_i], j=[psi_j])
        self.GF_PSI_gap.g_gap = self.young_gap_conductance

        self.net = Network(
            self.gf_neuron,
            self.ttm_neuron,
            self.psi_neuron,
            self.dlmn_neuron,
            self.GF_TTMn_con,
            self.GF_PSI_con,
            self.PSI_DLMn_con,
            self.GF_TTMn_gap,
            self.GF_PSI_gap,
        )
        self.gaps = self.GF_TTMn_gap



    def setup_monitors(self):
        """
        Initializes StateMonitors for all neurons in the circuit.
        Call this right after initializing your neurons and before running.
        """
        # Point neurons (Assuming GF, TTM, and PSI are NeuronGroups)
        self.mon_gf = StateMonitor(self.gf_neuron, 'v', record=True)
        self.mon_ttm = StateMonitor(self.ttm_neuron, 'v', record=True)
        self.mon_psi = StateMonitor(self.psi_neuron, 'v', record=True)

        # Spatial neuron (DLMn)
        # Recording at the dendrite tip (input) and axon terminal (output)
        self.mon_dlmn = StateMonitor(self.dlmn_neuron, 'v', record=[0, len(self.dlmn_neuron)-1])


        ## AI Generated code 
        # Tell the network to include these monitors in the simulation
        self.net.add(self.mon_gf, self.mon_ttm, self.mon_psi, self.mon_dlmn)

        ## AI generated code

    def inject_and_run(self, current_amp=5*nA, start_time=10*ms, pulse_duration=0.03*ms, cooldown=20*ms):
        """
        Runs the simulation, injects a square pulse of current into the DLMn dendrite, 
        and then continues running to observe the voltage decay.
        """
    
        self.net.run(start_time)

        self.gf_neuron.I_inj[0] = current_amp
        self.net.run(pulse_duration)

        self.gf_neuron.I_inj[0] = 0*amp
        self.net.run(cooldown)

    def set_param(self, param, val):
        if param == 'g_gap':
            self.GF_TTMn_gap.g_gap = val
            self.GF_PSI_gap.g_gap = val
            self.params['g_gap'] = val
            return

        if param == 'gnatbar':
            for neuron in [self.GF, self.TTMn, self.PSI, self.DLMn]:
                neuron.gnatbar = val
            self.params['gnatbar'] = val
            return

        if param == 'gkbar':
            for neuron in [self.GF, self.TTMn, self.PSI, self.DLMn]:
                neuron.gkbar = val
            self.params['gkbar'] = val
            return

        if param == 'gleak':
            for neuron in [self.GF, self.TTMn, self.PSI, self.DLMn]:
                neuron.gl = val
            self.params['gleak'] = val
    
