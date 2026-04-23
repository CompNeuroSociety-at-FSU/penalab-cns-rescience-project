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
        self.gf_neuron_morph = Cylinder(diameter = 8*um, length=400*um)


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

        axon_diameters = [prox_diam, dist_diam]

        self.dlmn_neuron_morph = Section(diameter=axon_diameters, length=50*um, n=51)
       
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
        self.chemical_synapse_reversal = 0
        self.chemical_synapse_delay = 0.15*ms
        self.chemical_synapse_peak_conductance = 80*uS
        self.neuromuscular_junction_delay = 0.35*ms
        self.leak_reversal_potential = -85*mV
        self.sodium_reversal_potential = 65*mV
        self.potassium_reversal_potential = -74*mV


        # This will be the set of equations that are used for the active sections of the neurons (axons)
        eqs_for_active= '''
        Im = : -g_bar_Na * (m**3) * h *(v-E_Na) - g_bar_K * (n**4) * (v-E_k) - gl * (v - El):amp/meter**2
        I_inj : amp (point current) # The current the included externally from the membrane

        

        '''

        # These will be the set of equations that will be used for the passive section of the neurons
        eqs_for_passive = '''
        Im = -gl * (v - El) : amp/meter**2
        I_inj : amp (point current) # The current the included externally from the membrane
        '''
    
        # Here are the neurons that will created from the number of neurons listed
        self.gf_neuron = SpatialNeuron(morphology=self.gf_neuron_morph, model=eqs,
                                       Cm=self.specific_membrane_capitance,Ri= self.specific_axial_resistance,
                                       namespace={'gl': self.leak_conductance, 'El' : self.leak_reversal_potential})
        self.ttm_neuron = SpatialNeuron(morphology=self.ttmn_neuron_morph, model=eqs,
                                         Cm=self.specific_membrane_capitance,Ri= self.specific_axial_resistance,
                                         namespace={'gl': self.leak_conductance, 'El' : self.leak_reversal_potential})
        self.psi_neuron = SpatialNeuron(morphology=self.psi_neuron_morph, model=eqs,
                                         Cm=self.specific_membrane_capitance,Ri= self.specific_axial_resistance,
                                         namespace={'gl': self.leak_conductance, 'El' : self.leak_reversal_potential})
        self.dlmn_neuron = SpatialNeuron(morphology=self.dlmn_neuron_morph, model=eqs,
                                          Cm=self.specific_membrane_capitance,Ri= self.specific_axial_resistance,
                                          namespace={'gl': self.leak_conductance, 'El' : self.leak_reversal_potential})
        

        # AI GENERATED CODE, AI GENERATED CODE, WARNING AI GENERATED CODE
        # ... your existing morphology and neuron setup ...
        
        # Add this at the bottom of __init__
        self.net = Network()
        self.net.add(self.dlmn_neuron)
        
        # If your gf, ttm, and psi neurons are already defined, add them too!
        self.net.add(self.gf_neuron, self.ttm_neuron, self.psi_neuron)

        # AI GENERATED CODE IS ABOVE





    def setting_leak_reversal_potential(self):
        # Sets all of the starting voltage
        self.gf_neuron.v = self.leak_reversal_potential
        self.ttm_neuron.v = self.leak_reversal_potential
        self.psi_neuron.v = self.leak_reversal_potential
        self.dlmn_neuron.v = self.leak_reversal_potential

    # AI Generated code, Will be replaced
    # WARNING AI GENERATED CODE, FOR TESTING PURPOSES ONLY
    # AI GENERATED CODE BEWARE, AI GENERATED AHEAD
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
        self.mon_dlmn_dend = StateMonitor(self.dlmn_neuron.dendrite[0], 'v', record=True)
        self.mon_dlmn_axon = StateMonitor(self.dlmn_neuron.axon[50], 'v', record=True)


        ## AI Generated code 
        # Tell the network to include these monitors in the simulation
        self.net.add(self.mon_dlmn_dend, self.mon_dlmn_axon)

        ## AI generated code

    def inject_and_run(self, current_amp=1*nA, start_time=10*ms, pulse_duration=2*ms, cooldown=20*ms):
        """
        Runs the simulation, injects a square pulse of current into the DLMn dendrite, 
        and then continues running to observe the voltage decay.
        """
    
        self.net.run(start_time)

        self.dlmn_neuron.I_inj[self.dlmn_neuron.dendrite[0]] = current_amp
        self.net.run(pulse_duration)

        self.dlmn_neuron.I_inj[self.dlmn_neuron.dendrite[0]] = 0*amp
        self.net.run(cooldown)

    # Phew, away from AI  generated code
    
    
