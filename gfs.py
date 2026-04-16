# Jonathan Alcineus - 2026
# Here is the structure that I will create for the giant fiber system (GFS) of 
# Drosophila melanogaster, or adult fruit fly, In the original paper, the authors
# Used 4 neurons (The GF neuron, the TTM motoneuron (TTMn), 
# a peripherally synapsing interneuron (PSI), and a DLM motoneuron (DLMn)) to simulate
# this system, this is crucial to create the structure of the giant fiber system of for class
# and potentially create subclasses under this class for each of the type of neurons

from brian2 import *
import matplotlib
import numpy

class gfs:
    # Paper decided to experiment with using 4 neurons
    # I wanted there to be an option to change the number of neurons within
    # the GFS, so I decided to have the default number of neurons match the paper
    # but I could experiment with more neurons if I wanted to

    def __init__(self, num_gf = 1, num_ttm = 1, num_psi = 1, num_dlmn = 1):
        self.num_gf = num_gf # Number of GF neurons in this GFS, default is 1
        self.num_ttm = num_ttm # Number of TTMn neurons in this GFS, default is 1
        self.num_psi = num_psi # Number of PSI neurons in this GFS, default is 1
        self.num_dlmn = num_dlmn # Number of DLMn neurons in this GFS, default is 1

    # Sample equation for the neuron's groups, will change later
        self.eqs =  '''
            dv/dt = 1-v : 1
        '''
    
    # Here are the neurons that will created from the number of neurons listed
    def create_neurons(self):
        gf_neurons = NeuronGroup(self.num_gf, self.eqs)
        ttm_neurons = NeuronGroup(self.num_ttm, self.eqs)
        psi_neurons = NeuronGroup(self.num_psi, self.eqs)
        dlmn_neurons = NeuronGroup(self.num_dlmn, self.eqs)
