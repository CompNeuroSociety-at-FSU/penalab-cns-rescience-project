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
    # Paper decided to experiment with using 4 neurons
    # I wanted there to be an option to change the number of neurons within
    # the GFS, so I decided to have the default number of neurons match the paper
    # but I could experiment with more neurons if I wanted to

    # num_gf = 1, num_ttm = 1, num_psi = 1, num_dlmn = 1, Save these just in case for the number of neurons if want to change
    #         self.num_gf = num_gf # Number of GF neurons in this GFS, default is 1
    #   self.num_ttm = num_ttm # Number of TTMn neurons in this GFS, default is 1
    #   self.num_psi = num_psi # Number of PSI neurons in this GFS, default is 1
    #   self.num_dlmn = num_dlmn # Number of DLMn neurons in this GFS, default is 1
    # We'll have to use the Spatial Neuron class that only covers one Neurons

    def __init__(self):
        # Now we are getting to describe the shapes for each of th eneurons, this is according to page 3 of the ENEURO Paper

    

        ## Another AI Generated, Beware, AI generate
        # 1. Calculate the length of a single compartment (50 um total / 51 chunks)
        segment_length = 50 / 51

        # 2. Create an array of exactly 51 lengths, and attach the unit
        axon_lengths = ones(51) * segment_length * um

        # The paper uses 51 iso-segments for the axons and dendrites (all of the cylindrical segments of the paper)
        # First we are putting the default morphology (or shape) for the gf neuron
        # The GF neuron does not contains any axons or dendrites, so nothing else needed other than using Soma class
        # But it does have electrical synpases between the axon of the PSI and the dendrite of the TTmn
        self.gf_neuron_morph = Soma(diameter = 8*um)

        # Figure out that length BS later for the gf_neuron: length=400*um

        # Here is the morphology for the TTMn neuron, it contains two dendrites and one active axon
        self.ttmn_neuron_morph = Soma(diameter=6*um) 
        # self.ttmn_neuron_morph.medial_dendrite = Cylinder(diameter=6*um, length=axon_lengths, n=51)
        self.ttmn_neuron_morph.medial_dendrite = Cylinder(diameter=6*um, length=60*um, n=51)
        #self.ttmn_neuron_morph.lateral_dendrite = Cylinder(diameter=6*um, length=axon_lengths, n=51)
        self.ttmn_neuron_morph.lateral_dendrite = Cylinder(diameter=6*um, length=30*um, n=51)
        # self.ttmn_neuron_morph.axon = Cylinder(diameter=6*um, length=axon_lengths, n=51)
        self.ttmn_neuron_morph.axon = Cylinder(diameter=6*um, length=50*um, n=51)

        # Here is the morphology for the PSI neuron, one axon and one dentrite
        self.psi_neuron_morph = Soma(diameter=4.5*um)
        # self.psi_neuron_morph.axon = Cylinder(diameter=4.5*um, length=axon_lengths, n=51)
        self.psi_neuron_morph.axon = Cylinder(diameter=4.5*um, length=90*um, n=51)
        # self.psi_neuron_morph.dentrite = Cylinder(diameter=4.5*um, length=axon_lengths, n=51)
        self.psi_neuron_morph.dendrite = Cylinder(diameter=4.5*um, length=170*um, n=51)

        # Here is the morphology for the DLMn neuron, 2 diameters (one proximal one distal) and both one axon and dentrite
        # Nah, dude. The axon is tapered but the diameter for the neuron is not


        # I will use cable theory to calculate the diameter of the dlmn neuron
        # But for the purposes of getting the structure of the code, we'll use 
        # 8 micrometers for the neuron's diameter
        self.dlmn_neuron_morph = Soma(diameter=8*um)
        prox_diam = 2*um
        dist_diam = 4*um

        # AI Generated code beware
        axon_diameters = linspace(prox_diam, dist_diam, 52)
        # AI generated up there

        self.dlmn_neuron_morph.axon = Section(diameter=axon_diameters, length=axon_lengths, n=51)
        # self.dlmn_neuron_morph.axon = Section(diameter=axon_diameters, length=50*um, n=51)
        # self.dlmn_neuron_morph.dentrite = Cylinder(diameter=2*um, length=axon_lengths)
        self.dlmn_neuron_morph.dendrite = Cylinder(diameter=2*um, length=100*um)


        # Here are the standard membrane properties, this shows how electricity will flow
        # through the neurons
        # Make sure to put the rest of the membrane properties from the paper


        # These are the most basic membrane properties from the paper
        self.leak_conductance = 0.03*mS / cm**2
        self.leak_reversal_potential = -85*mV
        self.specific_membrane_capitance = 1*uF /cm**2
        self.specific_axial_resistance = 35 * ohm * cm


        # Sample differential equation for the flow of eletricity through this ion
        # The differential equation for a passive spatial compartment, AI generated, 
        # This will be changed later
        eqs = '''
        Im = gl * (El - v) : amp/meter**2
        I_inj : amp (point current) # Placeholder for where we will inject electricity
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
    
    