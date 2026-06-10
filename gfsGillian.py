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

        # First we are putting the default morphology (or shape) for the gf neuron
        # The GF neuron does not contains any axons or dendrites, so nothing else needed other than using Soma class
        # But it does have electrical synpases between the axon of the PSI and the dendrite of the TTmn
        self.gf_neuron_morph = Soma(diameter = 8*μm, length=400*μm)

        # Here is the morphology for the TTMn neuron, it contains two dendrites and one active axon
        self.ttmn_neuron_morph = Soma(diameter=6*μm)
        self.ttmn_neuron_morph.medial_dendrite = Cylinder(length=60*μm)
        self.ttmn_neuron_morph.lateral_dendrite = Cylinder(length=30*μm)
        self.ttmn_neuron_morph.axon = Cylinder(length=50*μm)

        # Here is the morphology for the PSI neuron, one axon and one dentrite
        self.psi_neuron_morph = Soma(diameter=4.5*μm)
        self.psi_neuron_morph.axon = Cylinder(length=90*μm)
        self.psi_neuron_morph.dentrite = Cylinder(length=170*μm)

        # Here is the morphology for the DLMn neuron, 2 diameters (one proximal one distal) and both one axon and dentrite
        self.dlmn_neuron_morph.proximal = Soma(diameter=2*μm)
        self.dlmn_neuron_morph.distal = Soma(diameter=4*μm)
        self.dlmn_neuron_morph.axon = Cylinder(length=50*μm)
        self.dlmn_neuron_morph.dentrite = Cylinder(length=100*μm)



        # Sample equation for the neuron's groups, will change later
        self.eqs =  '''
            dv/dt = 1-v : 1
        '''
    
        # Here are the neurons that will created from the number of neurons listed
        self.gf_neuron = SpatialNeuron(morphology=self.gf_neuron_morph)
        self.ttm_neuron = SpatialNeuron(morphology=self.ttmn_neuron_morph)
        self.psi_neuron = SpatialNeuron(morphology=self.psi_neuron_morph)
        self.dlmn_neuron = SpatialNeuron(morphology=self.dlmn_neuron_morph)
