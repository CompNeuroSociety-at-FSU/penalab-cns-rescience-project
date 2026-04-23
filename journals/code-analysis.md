# Examining the original paper's code:

## Analysis of the Code and Information from the paper to recreate the GFS as intended by the authors

### Date: 2026-04-23

- "Neuron is a basic unit of the brain, Neuron's send electrical signals throughout the body (Made for rapid commmunication)" (Pages 21-22, Hedges)
- "Axons are the output extension of a neuron" (Page 25, Hedges)
- "When the axons transmits an electrical signal, its called an action potential" (Page 26, Hedges)
- "Axon length depends on the neuron and the function" (Page 27, Hedges)
- "Axon Diameter: effects the speed which the action potential will propogate. Larger the diameter = faster a signal can travel" (Page 28, Hedges)
- "Synapse - physical distance separatin to neurons" (Page 30, Hedges)
- Unlike electrical synpases which share cytoplasm and are less that 5 nm apart, chemical synapses uses neurotransmitters to commmunicate (Page 30-31, Hedges)
- Presynaptic - before synapse is formed with another neuron (Page 32, Hedges)
- Postsynaptic - forms synapse with another neuron (Pagge 32, Hedges)
- Dendrites pull electricity towards the neuron, while axons pull elecriccty away from the neuron

### Paper's Description of the Giant Fiber System:

- "Gap junctions are physical substrate of eletrical synpases or fast channels and fast tranmission in neruons" (Page 2, Augustin et. al)
- "Less gap junctions in nervous system = aging" (Page 2, Augustin et. al)
- Membrane conductance is the y value and the x value is latency
- GFS contains four (4) neurons
  1. Giant Fiber (GF) Neuron
  2. TTM motor neuron
  3. peripherally synpasing interneuron (PSI)
  4. DLM motor neuron
     (Page 3, Augustin et. al)
- Each neuron contains **1 to 3 unbranched cylindrical sections** (Page 3, Augustin et. al)
- Each cylinder's section contains 51 iso-segmments, the basic computational unit ... connected to specific axial resistance (Pages 3, Augustin et. al)
- GF Neuron has a unidirectional electrical synpase connected the axon (or active section) of the PSI and synpase connected to the passive session or dendrites (TTM)
- The TTM neuron has two dendrites and an axon
- The PSI neuron contains a dendrite and an axon, that forms a chemical synapse onto to the active section (axon) of the DLMn
- DLMn contains a tapering axon and a dendrite
- All above is (Page 3, Augustin et. al)

### Paper's Claim

According to our model, anatomical properties of the GFS neurons have a stronger impact on the transmission than neuronal membrane conductance densities. The model provides testable predictions for the effect of experimental interventions on the circuit’s performance in young and ageing flies. (Page 1, Augustin et. al)

### My Claim

Through my reading and research of the functions of dendrites and axons within neurons, the **neuronal anatomy** plays a larger role **response latency** then the **membrane conductance**.

#### Independent vs Dependent

**Independent:** the diameter and length of the dendrites, axons and neurons (meters), and the membrane conductance (siemens)
**Dependent:** the response latency (seconds)

### Code Implementation of the GFS

- Let's look at the class file, `gfn.py`
- Questions raised
- Planned experiments
- Items to investigate

```python

 def __init__(self, params = 'def'):
        if params == 'def':
            self.params={'GF_diam': 8,
                 'GF_L': 400,
                 'TTMn_diam': 6,
                 'TTMn_L': 50,
                 'TTMn_med_L': 60,
                 'TTMn_lat_L': 30,
                 'PSI_diam': 4.5,
                 'PSI_L': 90,
                 'PSI_pas_L': 170,
                 'DLMn_diam_start': 2,
                 'DLMn_diam_end': 4,
                 'DLMn_L': 50,
                 'DLMn_pas_L': 100,
                 'temp': 25.0,
                 'g_gap': 135.0,
                 'TTMn_syn_tau1': 0.5,
                 'TTMn_syn_tau2': 5.0,
                 'TTMn_syn_e': 0,
                 'TTMn_syn_pre_loc': 1.0,
                 'TTMn_syn_post_loc': 0.2,
                 'PSI_syn_tau1': 0.1,
                 'PSI_syn_tau2': 5.0,
                 'PSI_syn_e': 0,
                 'PSI_syn_pre_loc': 0.9,
                 'PSI_syn_post_loc': 0.5,
                 'DLMn_syn_tau1': 0.1,
                 'DLMn_syn_tau2': 1.0,
                 'DLMn_syn_e': 0,
                 'DLMn_syn_pre_loc': 0.85,
                 'DLMn_syn_post_loc': 0.25,
                 'GF_TTMn_delay': 1,
                 'GF_TTMn_wt': 0.00,
                 'GF_PSI_delay': 1,
                 'GF_PSI_wt': 0.00,
                 'PSI_DLMn_delay': 0.15,
                 'PSI_DLMn_wt': 0.08,
                 'gnatbar': 300e-3,
                 'gnapbar': 110e-6,
                 'gkbar': 10e-3,
                 'gleak': 30e-6,
                 'Eleak': -85.0,
                 'ena': 65,
                 'ek': -74,
                 'stim_loc': 0.0,
                 'stim_dur': 0.03,
                 'stim_delay': 100,
                 'stim_amp':120.0,
                 'muscle_delay':0.35}
        else:
            self.params = params;

        params = self.params

```

These are all of the default parameters for the giant fiber system for this model

```python
        self.GF = neuron.h.Section(name = 'GF');
        self.GF.nseg = 51
        self.GF.diam = params['GF_diam'];
        self.GF.L = params['GF_L'];
```

Setting the parameters and creating the gf neuron

```python

        self.TTMn = neuron.h.Section(name = 'TTMn');
        self.TTMn.nseg = 51
        self.TTMn.diam = params['TTMn_diam'];
        self.TTMn.L = params['TTMn_L'];

        self.TTMn_med = neuron.h.Section(name = 'TTMn_med');
        self.TTMn_med.nseg = 51
        self.TTMn_med.diam = params['TTMn_diam'];
        self.TTMn_med.L = params['TTMn_med_L'];
        self.TTMn_syn = neuron.h.Exp2Syn(self.TTMn_med(params['TTMn_syn_post_loc']))
        self.TTMn_syn.tau1 = params['TTMn_syn_tau1'];
        self.TTMn_syn.tau2 = params['TTMn_syn_tau2'];
        self.TTMn_syn.e = params['TTMn_syn_e'];
        self.TTMn_med.connect(self.TTMn,0,0)

        self.TTMn_lat = neuron.h.Section(name = 'TTMn_lat');
        self.TTMn_lat.nseg = 51
        self.TTMn_lat.diam = params['TTMn_diam'];
        self.TTMn_lat.L = params['TTMn_lat_L'];
        self.TTMn_lat.connect(self.TTMn,0,0)
```

Setting the parameters and creating the neuron for the TTMn neuron

```python
self.PSI = neuron.h.Section(name = 'PSI');
        self.PSI.nseg = 51
        self.PSI.diam = params['PSI_diam'];
        self.PSI.L = params['PSI_L'];
        self.PSI_syn = neuron.h.Exp2Syn(self.PSI(params['PSI_syn_post_loc']))
        self.PSI_syn.tau1 = params['PSI_syn_tau1'];
        self.PSI_syn.tau2 = params['PSI_syn_tau2'];
        self.PSI_syn.e = params['PSI_syn_e'];

        self.PSI_pas = neuron.h.Section(name = 'PSI_pas');
        self.PSI_pas.nseg = 51
        self.PSI_pas.diam = params['PSI_diam'];
        self.PSI_pas.L = params['PSI_pas_L'];
        self.PSI_pas.connect(self.PSI,0,0)
```

Setting the parameters and creating the neuron for the PSI neuron

```python
 self.DLMn = neuron.h.Section(name = 'DLMn');
        self.DLMn.nseg = 51
        for seg in self.DLMn:
            seg.diam = params['DLMn_diam_start'] + seg.x * (params['DLMn_diam_end'] - params['DLMn_diam_start'])

        self.DLMn.L = params['DLMn_L'];
        self.DLMn_syn = neuron.h.Exp2Syn(self.DLMn(params['DLMn_syn_post_loc']))
        self.DLMn_syn.tau1 = params['DLMn_syn_tau1'];
        self.DLMn_syn.tau2 = params['DLMn_syn_tau2'];
        self.DLMn_syn.e = params['DLMn_syn_e'];

        self.DLMn_pas = neuron.h.Section(name = 'DLMn_pas');
        self.DLMn_pas.nseg = 51
        self.DLMn_pas.diam = params['DLMn_diam_start'];
        self.DLMn_pas.L = params['DLMn_pas_L'];
        self.DLMn_pas.connect(self.DLMn,0,0)
```

Setting the parameters and creating the neuron for the DLM neuron

```python
        for cell in [self.PSI_pas, self.TTMn_med, self.TTMn_lat, self.DLMn_pas]:
            cell.insert('pas')
            cell.e_pas = params['Eleak']
            cell.g_pas = params['gleak']
```

Creates baseline resting state for each of the neurons, E represent equilibrium gradient matches the chemical gradient or not net flow for a particular ion. g represent the conductunce or how easily ions flow through the channels. For leak channels, this is a constant value. For sodium and potassium channels, this changes a lot depending on the voltage.

### Math Behind the Neuron in the Paper

**Paper Helpful for understanding the membrane capitance**
[Here is the link](https://www.cns.nyu.edu/~david/handouts/membrane.pdf)

"The battery represents the sodium-potassium pump that acts to hold the electrical potential of the inside of the cell below that of the outside. This voltage difference is called the resting potential of the neuron" (Page 1, Hegger)

Before we get into complexity of including ion channels and fully utilizing the Hodgkin-Huxley (HH) Model, we have to understand the core of the model: Core membrane equation.

$$C_m \frac{dV}{dt} = -I_{ion} + I_{ext}$$.

This equation is extremely crucial, because it represent the sum of the currents (in the neruon (ionic) and applied to the neuron externally) which equal to the membrane capacitance and the rate of change of the membrane potential over time. t is a independent variable (specifically the response latency)

Because electrical signals in through neurons work similarily as electrical circuits, we can begin my starting with Ohm's Law:
$$V = IR$$
where $V$ is equal to voltage, $I$ current and $R$ resistance

\***\*IMPORTANT! Conductance is how easily a charge, flows through membrane. Capacitance is the membrane's ability to store a charge\*\***

However, within many electric fields and even biological models, you'll have to deal with components that store energy or charge. And the Ohm's does not cut it.

First, we have this equation. This is because a capacitator stores energy in an electric field. The electrical charge is held in proportion to the Voltage across a specific capacitance.

$$Q=CV$$ or specificially, $$Q(t)=CV(t)$$ where $Q$ is electrical charge (this changes), $V$ Voltage (the voltage) and $C$ capacitance (constant), depends of the size of the capacitor

A current is defined as this:
$$I = \frac{dQ}{dt}$$, where $I$ is the current and $\frac{dQ}{dt}$ is the change in electrical charge over time

Find the derivative on both sides, with respect to t:
$$\frac{d}{dt}(Q(t))=\frac{d}{dt}[C.V(t)]$$

Then bam! We have the equation for current:
$$I=C\frac{dV(t)}{dt}$$

If there is not a change in voltage, that means there is current flows with the lipid bilayer of the membrane

\***\*IMPORTANT: Conductance is the inverse of resistance. Conductance= how easily ions flow through field/membrane, Resistance= how hard ions flow.\*\***

**Hodgkin-Huxley Model**
So the current that is going into the membrane has to equal the current out. Specifically,
$$I_c+I_g = 0 $$ or $$C\frac{dV_m}{dt} + g(V_m-E) = 0$$, where $g$ is equal to conductance, $V_m$ is equal to membrane potential, and $E$ is equal to resting potential of a neuron. (Page 2-3, Heeger)

But finally last but not least the one the only, full Hodgkin-Huxley Model
It breaks down the ionic current membrane into sodium, potassium, and leak channels for action potential occur
$$C\frac{dV}{dt} = -\=g_{Na}m^3h(V-E_{Na}) -\=g_{K}n^4(V-E_{K})-\=g_{L}(V-E_{L}) + I_{ext}$$

Where $E_x$, is the resting potential or reversal equilibrium and $\=g_x$ is the maximum conductance for an Ion. If $V > E_{Na}$, sodium is flowing out. If $V < E_{Na}$, sodium is flowing in. The variables $m, n, h$ are received by representing the probabilit between 0 and 1 of the sodium gates $m^3h$ (This shows 3 channels need to be open) and the potassium gates $n^4$ are open (This shows 4 channels needs to be open). This functions like the lipid bilayer of a the neuron (which is a cell duh)

**Throwing analogies:**

- When neuron is at rest, the leak current is balanced by the sodium-potassium pump, so net current is zero
- Current is injected to neuron by potassium pump

# Super useful Links:

https://brian2.readthedocs.io/en/2.9.0/examples/compartmental.bipolar_cell.html

https://brian2.readthedocs.io/en/2.7.1/reference/brian2.spatialneuron.morphology.Soma.html
