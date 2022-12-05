---
title: "Neural Attentive Circuits."
venue: "CoRR"
volume: "abs/2210.08031"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2210-08031"
doi: "10.48550/ARXIV.2210.08031"
ee: "https://doi.org/10.48550/arXiv.2210.08031"
url: "https://dblp.org/rec/journals/corr/abs-2210-08031"
authors: ["Nasim Rahaman", "Martin Weiss", "Francesco Locatello", "Chris Pal", "Yoshua Bengio", "Bernhard Sch\u00f6lkopf", "Erran Li", "Nicolas Ballas"]
sync_version: 3
cite_key: "journals/corr/abs-2210-08031/Rahaman/2022"
---

In this work, a general purpose yet modular architecture called "Neural Attentive Circuits" is introduced.

It jointly learns the parameterization and sparse connectivity of neural modules without domain knowledge. It has its roots in [[deep_compositional_question_answering_with_neural_module_networks]], in that it learns the module configuration and also the parameterization of the modules end-to-end.

NACs can learn diverse and meaningful module confirgurations on NLVR2 and can do well on low-shot adaptation.

NACs implement a system of sparsely connected and attentively interacting modules and pass messages to each other along "connectivity graphs" that are learned or dynamically inferred from the forward pass. It is also possible to prune the modules to reduce complexity at inference time.

How does it work?
![[nac_generator_executor.png]]

You have a circuit generator and a circuit exector.

The generator makes a configuration over modules and defines both the connectivity pattern and the conditioning states for each module.

The executor consumes the design and input to perform the inference.

![[nac_design.png]]

What do the circuits look like and how are they generated.

There are several modules. Each module has:
 - A "signature" vector $s_i$
 - A "code" vector $c_i$
 - Some initial state and parameters

The signature vectors are used for self-attention between the modules and the code vectors are used for conditioning the computation of each module.

Starting with the code vectors, each module is given as a "ModFC", which is basically a linear layer with some gating on the inputs depending on the conditioning code. It is given as:

$$
\text{ModFC}(x; c) = W(x \odot (1 + \alpha \text{LayerNorm}(W_c c))) + b
$$

The default gate value is 1, so if you learn $\alpha =  0$, then the conditioning has no effect.

How about the attention between the modules? This is done via "Stochastic Kernel-modulated Dot-product attention".

What a mouthful. But basically it just just a kind of gumbel-softmax with no hard thresholding over the attention. Eg:

$$
K_{ij} \sim \text{Concrete}(P_{ij}, \tau), P_{ij} = \text{exp}(\frac{-d(s_i, s_j)}{\epsilon})
$$

where $d$ is any appropriate distance measure.

Then for the attention you have:

$$
\text{softmax}(\frac{QK^T}{\sqrt{d}} + \log K_{ij})
$$

So basically, $q_i$ interacts with $k_j$ with probability $\text{exp}({-d(s_i, s_j)})$.

How about the circuit executors?

 - read-in: Read-in attention which generates the query vector and uses $X$ to generate the keys and values.
 - propagator: Propagator layers sequentially update the state of each processor module $L$ times. Note that there is parameter sharing and you have rounds of communication via SKMDPA.
 - read-out: Read-out modules have their own signatures and codes parameters which are different from the proessor modules. Each read out-module has a confidence score which is used to weight also the final output.

Conditional circuit generation:

 - You can freely learn everything or have a prior on circuits
 - Some circuits do better than othes.
 - Graph priors:
	 - Scale-freeness: few well-connected hubs
	 - planted partition: stochastic block model, encourages cliques

Note that for multi-modal data, you can have one modality used to generate the circuit and another modality used as the input data.


Experiments:
 - There is lots of redundancy amongst modules. We can drop around 80% of modules before we start to see a large perforance drop on validation accurracy. Drop modules in order of connectivity.