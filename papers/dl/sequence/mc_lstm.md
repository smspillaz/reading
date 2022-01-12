---
title: MC-LSTM - Mass-Conserving LSTM.
venue: ICML
pages: 4275-4286
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/icml/HoedtKKHHNHK21
ee: http://proceedings.mlr.press/v139/hoedt21a.html
url: https://dblp.org/rec/conf/icml/HoedtKKHHNHK21
authors: ["Pieter-Jan Hoedt", "Frederik Kratzert", "Daniel Klotz", "Christina Halmich", "Markus Holzleitner", "Grey Nearing", "Sepp Hochreiter", "G\u00fcnter Klambauer"]
sync_version: 0
---

# MC-LSTM

Contributions:
* Extend the inductive bias of LSTM to model the redistribution of stored quantities
* Results: New SOTA for NAUs at learning arithmetic operations, traffic forecasting, modelling a damped pendulum, hydrology peak flows.
* Interpretability: "in the hydrology example, we show that MC-LSTM states correlated with real world processes and are therefore interpretable"


Problem: A mechanism beyond storing is required for real-world applications.

 - Real world systems goverend by conservation laws (mass, energy, momentum, charge, particle counts)
 - Standard deep learning struggles at conserving quantities across layers or timesteps. Usually exploit spurious correlations.

# How it works

* MC-LSTM has astrong inductive bias to guarantee the conservation of mass, implemented by *left stochastic matricies*, ensuring that the sum of memory cells in the network represents the *current mass of the system*.
* Inputs divided into *mass inputs* and *auxiliary inputs*.

The original LSTM gate is:

$$c^t = c^{t - 1} + f(x^t, h^{t - 1})$$

To modify this according to the MC-LSTM formulation, we do three changes:

1. $f$ must distribute the mass from inputs into accumulators
2. Mass that leaves the MC-LSTM must disappear from the accumulators
3. Mass must be redistributed between accumulators

We also distinguish between *mass inputs* ($x$) and *auxliary inputs* ($\alpha$) . The auxiliary inputs can be used to contriol the gates.

So now we represent the forward pass as:

$$\mathbf{m}^t_{\text{total}} = \mathbf{R}^t \cdot \mathbf{c}^{t - 1} + \mathbf{i}^t \cdot x^t$$
$$\mathbf{c}^t = (1 - \mathbf{o}^t) \odot \mathbf{m}^t_{\text{total}}$$
$$h^t = \mathbf{o}^t \odot \mathbf{m}^t_{\text{total}}$$

($i$ and $o$ are the input and output gates and $R$ is a "positive left stochastic" matrix, where $1^T \cdot R = 1^T$)

**Positive Left Stochastic Matrix**: Used to describe the transitions of a Markov chain. Each entry mus be a nonnegative real number representing a probability.

 - Each column must sum to 1, which is the reason for the identity $1^T \cdot R = 1^T$ 

So interpreting each of these equations:
 - First equation is the dot product of the prior cell state (masses), redistributed according to $R^t$ plus the input gate times the auxiliary input $x^t$. Note that $x^t$ is a *scalar* and $i^t$ is a *vector* and the output, $\mathbf{m}_{\text{total}}$ is a *vector*, so the first equation *redistributes the existing mass* and *adds new mass* according to the input gate times some scale factor.
 - Second equation controls the *current mass*. Basically, the current mass is one-minus the output, elementwise product with the redistributed total mass.
 - Final equation controls the mass leaving the system. Note that $\mathbf{c}^t + \mathbf{h}^t = \mathbf{m}_{\text{total}}$
 - We also require that $0 \le o^t \le 1$ and $\sum i^t = 1$

Note as well that the *amount of mass on each timestep* may change, eg, $\mathbf{m}_{\text{total}}^t \ne \mathbf{m}_{\text{total}}^{t - 1}$ . We only require that:

1. Current mass in the system cannot increase or decrease "on its own", all new mass must come through the input gate (first equation). Current mass may only be "redistributed" across the cell states.
2. Mass leaving the system and mass remaining in the system must add up to the total mass in equation 1.

### How to compute the input and output gates

$$i^t = \text{softmax}(W_i \cdot a^t + U_i \cdot \frac{c^{t - 1}}{||c^{t - 1}||_1} + b_i)$$
$$o^t = \sigma(W_o + a^t + U_o \cdot \frac{c^{t - 1}}{||c^{t - 1}||_1} + b_o)$$
$$R^t = \text{softmax}(W_r \cdot a^t + U_r \cdot \frac{c^{t - 1}}{||c^{t - 1}||_1} + B_r)$$
Note that:
 * $i^t$ sums to 1
 * $0 \le o^t \le 1$
 *  $R^t$ sums to 1 along the columns

Remember as well that $\mathbf{a}^t$ is the "auxliary input". It does not control the input mass, rather it controls *how the mass will be distributed in the system*. The other parameters are learnable, except for $c$.

The reason for the normalization of the memory cells (eg $\frac{c^{t - 1}}{||c^{t - 1}||_1}$) is to "counter saturation of sigmoids and to supply probability vectors that represent the current distribution of mass across cell states". The reason for the 1-norm is so that the vector adds up to one, not that the vector has a length of 1 (which are different things).

This formulation is also the **time dependent redistribution**, basically the redistribution of mass can change per-timestep.

## Property Proofs

**Mass Conservation**

$$
m^{\tau}_c = m^0_{c} + \sum^{\tau} x^t - \sum^{\tau} m^t_h
$$
This says that the total mass in the system ($m^{\tau}_c = \sum^K c^{\tau}_k$) mass at $\tau$ is equal to the sum of all the input mass coming into the system at every timestep until $\tau$ minus all the mass that left the system, plus the initial mass.

**Boundedness of cell states**

$$
|c^{\tau}_k| \le \sum^{\tau}_{t = 1} x^t + m^0_c
$$
If the series of mass inputs converges, then the sum of cell states converges.

**Gradient flow**

Gradient flow is mostly determined by the redistribution matrix $R$. This implies that $R$ should be initialized with a redistribution matrix close to the identity matrix

**Computational Complexity**

In the general case, the input gates and redistribution matrix of an MC-LSTM are matrices, not vectors, so MC-LSTM is more computationally demanding than LSTM.

**Interpretability**

The representations within the model can be interpreted directly as accumulated mass. If the quanity is known, then this allows you to force a particular cell state to represent this quanity.

## Experiments

**Addition**: MC-LSTM generlaizes to longer sequences, input values in different ranges and more summands, with a success rate of around 80\%, which is slightly better than NAU and significantly better than LSTM whcih fails completely.

**Recurrent arithmetic**

**Static arithmetic**

**MNIST arithmetic**: Adding up MNIST digits, so the mass inputs are "extracted" from data.

**Traffic**: Inbound/output traffic requiring the "conservation of vehicles". All vehciles on outbound roads must have entered the city center or have been present in the first timestep, you can't have vehicles appearing from nowhere within the system.. MC-LSTM significantly outperforms regular LSTM.

**Pendulum**: "Total energy" is conserved. Kinetic energy redistributed into potential energy and vice versa and at each timestep, some energy leaves the system due to friction. Not a closed system, so you cannot use HNNs. In the friction-free case, no difference to HNNs, but significantly outperforms LSTM otherwise.

**Hydrology**: Mass inputs are precipitation and aux inputs are daily min/max temp, solar radiation, pressure and 27 basin characteristics