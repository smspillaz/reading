---
title: Local plasticity rules can learn deep representations using self-supervised contrastive predictions.
venue: NeurIPS
pages: 30365-30379
year: 2021
type: Conference and Workshop Papers
access: closed
key: conf/nips/IllingVBG21
ee: https://proceedings.neurips.cc/paper/2021/hash/feade1d2047977cd0cefdafc40175a99-Abstract.html
url: https://dblp.org/rec/conf/nips/IllingVBG21
authors: ["Bernd Illing", "Jean Ventura", "Guillaume Bellec", "Wulfram Gerstner"]
sync_version: 3
cite_key: conf/nips/IllingVBG21
---

This paper proposes a learning rule that takes inspiration from neuroscience and recent advances in self-supervision.

Minimize a simple layer-specific loss function. Don't do backpropagation at all. Instead follow a local hebbian learning rule that only depends on pre-and-post synaptic neural activity.

Hebbian rules struggle when "stacked" eg when asked to learn hierarhical representations. But backpropagation doesn't.

This paper proposes a local biologically plauble unsupervised learning rule:

 1. Self-supervised learning from temporal data (this is closest to natural data).
 2. Context-dependent plasticitiy

Suggests the "Contrastive, Local and Predictive Plasticity" (CLAPP) model which avoids BP completely but still builds hierarhical representaitons.

## Main Goals

Represent a corticial area by the layer $l$ of a deep neural net, eg $z^{t, l} = \rho(a^{t, l})$ where $\rho$ is a nonlinearity and $a^{t, l} = W^l z^{t, l - 1}$ is the linear transformation.

The plasticity rule proposed exploits the fact that temporal structure of natural inputs affects representation learning. Assume that weigth changes follow Hebbian learning rules, which are local in space and time, $\triangle W^{t}_{ji}$ updates connecting neurons $i$ and $j$ may depend only on the current activity of pre-synaptic and post-synaptic neurons at time $t$, or at $t - \delta t$. Also allow $k$ to influence $\triangle W_{ji}$ updates as long as there is an explicit connection from $k$ to $j$ $W_{jk}$.


Assume that the dentritic input influences the weight updates $\triangle W_{ji}$ but not its activity $z^{t}_j$ (eg, stuff from the future can update the weights but not update your activity.)

Consider an agent perceiving a moving object at time $t$ and then deciding whether to change its gaze.

Learning rule prototype:

$$
\triangle W_{ji} \propto \text{modulators} \cdot (W^{\text{pred} c^{t_1}}) \cdot \text{post}^{t_2}_j \cdot \text{pre}^{t_2}_i
$$

## Related Work

Most previous learning rules which include global modulating factors interpret it as a reward prediction error. In this paper, interpret it as self-awareness that something ahs changed in the stimulus.

This paper takes inspiration from contastive predictive coding, where the contrastive learning is done in the latent space. CPC evaluates a prediction $W^{\text{pred}} c^t$ such that a score function $\mu^{\tau} = z^{\tau}W^{\text{pred}} c^t$ becomes larger for the true future $\tau = t + \delta t$ than for any other vector taken at arbitrary time points elsewhere in the training set (the negative examples). Predictions should align with future activity but not with negative examples.

Greedy InfoMax: Is a variant of CPC which makes a step towards a local BP-free learning. Split the encoder into gradient isolated modules and avoid backprop between them, though this is still biologically implausible. CLAPP solves the implausibilities and allows a truly local implementation in space and time.

## CLAPP rule

The most essential difference compared to CPC or GIM is that we do not require the network to access the true future activity and recall network activity seen at some other time. instead, consider a natural time flow where the agent fixates on a moving animal for a while and then cahnges gaze spontaneously. The prediction is expected to be meanignful during fixation but inappropriate right after shifting the gaze.

Ftuure activity and context are always taken from the main feedforwad encoder network.

### Derivation of CLAPP

Rather than a global loss funciton, consider a binary classifcation problem *at every layer*:

$$
\mu_t^{t + \delta_t, l^T} = z^{t + \delta t, l^T} W^{\text{pred, l}} c^{t, l}
$$

This is the layer's "guess" of whether the agent did a fixation or a saccade (change of gaze). Every neuron $i$ has access to its own dentritic prediction $z^{t, l} = \sum_j W^{\text{pred}}_{ij} c^{t, l}_j$ of somatic activity. The product can be seen as a coincidence detector of dentric and somatic activity communicated by burst signals.

Intepret $y^t$ as the lable of a binary classifcaiton problem and define the CLAPP loss using the hinge loss as:

$$
\mathcal{L}_{\text{CLAPP}}^{t, l} = \max(0, 1 - y^t \cdot u_t^{t + \delta t, l})
$$

where $y^t = +1$ for fixation and -1 for saccade.

### Gradients of CLAPP

$$
\frac{\partial \mathcal{L}_{\text{CLAPP}}}{\partial W^c_{ji}} = (W^{\text{pred}} c^t)_j \rho'(a^{t + \delta t}_j) x^{t + \delta t}_i
$$

$$
\frac{\partial \mathcal{L}_{\text{CLAPP}}}{\partial W^c_{km}} = (W^{\text{pred}} c^t)_k \rho'(a^{t + \delta t}_k) x^{c, t}_m
$$

$c$ is the "predicting layer", the source of hte prediction.

Then the modulating factor $\gamma_t - y^t \cdot H^t$ where $y^t$ is a network-wide broadcast signal indicating a saccade or a fixation and $H^t$ is a layer-wide broadcast signal indicating whether the saccade or fixation was correctly classified as such. So then you have:

$$
\triangle W^t_{ji} = \gamma_t \cdot (W^{\text{pred}} c^{t - \delta t}) \cdot \rho'(a^t_j) x^t_i
$$

Also introduce another matrix $W^{\text{retro}}$ which minimizes a loss function of the same form above using inverse temporal order.

# Empirical Results

## Hierarchical Representations

Use STL-10. Each image is split into 16x16 patches and the patches are viewed one after the other in vertical order. Train a 6-layer encoder using the CLAPP rule.

Select neurons randomly and show image patches which best activate these neurons the most. First layer neurons are selective to horizontal or. vertical gratings or homogenous colors. In the third layer, neurons are more selective of semantic features.

Use T-SNE to visualize the encodings of the STL-10 test set. First layer mostly unrelated tot he underlying class. In the third and sixth layers, coherent clusterings, separating furry animals and vehicles.

Linear Probing: Classification accuracy increases monotonically with the layer number and only saturates at layers 5 and 6.

## CPC and CLAPP




## Speech and Video
