---
title: The Sensory Neuron as a Transformer - Permutation-Invariant Neural Networks for Reinforcement Learning.
venue: CoRR
volume: abs/2109.02869
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2109-02869
ee: https://arxiv.org/abs/2109.02869
url: https://dblp.org/rec/journals/corr/abs-2109-02869
authors: ["Yujin Tang", "David Ha"]
sync_version: 0
---

# Sensory Neuron as a Transformer: Permutation Invariant Neural Networks for Reinforcement Learning

Feed each sensory input from the environment into distinct but identical neural networks with no fixed relationship. Then they can communicate with each other via na attention mechanism to produce a globally coherent policy. Can still perform task even if the inputs are randomly permuted several times during an episode.

Apparently this has a generalization advantage.

Can train on a small fraction of patches and then give more patches at test time to improve performance (really?).

Can generalize to visual environments with novel background images (probably because you learn to only pay attention to the patches that matter - eg, those without a background).

## Permutation Invariance

Permutaton invariant function is one where if you change the order of the inputs, the output does not change.

Permutation equivariant function is one where if you change the order of the inputs, the output changes order in some deterministic way.

Self-attention is permutation equivariant, since the order of the decoder sequence specifies the output order.

Set-tranformer replaces the query with a set of learnable seed vectors, so its no longer a functon of the input and thus enables the output to become permutation invariant (because it doesn't matter what order the keys come in).

More detials:

Self-attention is:

$$
y = \sigma(SQ^T)V
$$

Q is fixed, K and V are functions of the input. Typically linear transformations. We want ot show that $y$ is the same regardless of the ordering of $K$ and $V$.

$$
y = \sigma(\begin{pmatrix} q_1 \\ q_2 \end{pmatrix} (k_1, k_2, k_3)) \begin{pmatrix} v_1 \\ v_2 \\ v_3 \end{pmatrix}
$$

$$
y = \sigma(\begin{pmatrix} q_1 k_1 & q_1 k_2 & q_1 k_3 \\ q_2 k_1 & q_2 k_2 & q_2 k_3 \end{pmatrix}) \begin{pmatrix} v_1 \\ v_2 \\ v_3 \end{pmatrix}
$$

$$
y = \begin{pmatrix} \sigma(q_1 k_1) v_1 + \sigma(q_1 k_2) v_2 + \sigma(q_1 k_3) v_3 \\  \sigma(q_2 k_1) v_1 + \sigma(q_2 k_2) v_2 + \sigma(q_2 k_3) v_3 \end{pmatrix}
$$

Basically we can then replace $k_1 ) v_1$ etc with $k_a ) v_a$ and get the same result for any permutation of $[a, b, c] = [1, 2, 3]$, because sum is permutation invariant. Therefore set-transformer is permutation invariant. Compare with the case where the query depends on the input - then a permutation of the queries would change the order of the output , because the query components are not being summed, they're in different rows.

## The architecture

![[attention_neuron_architecture.png]]

$$
K(o_t, a_{t - 1}) = \begin{bmatrix} f_k(o_t[1], a_{t - 1}) \\ .. f_k(o_t[N], a_{t - 1}) \end{bmatrix} \in R^{N \times d_{f_k}}, V(o_t) = \begin{bmatrix} f_v(o_t[1], a_{t - 1}) \\ .. f_v(o_t[N], a_{t - 1}) \end{bmatrix} \in R^{N \times d_{f_k}}
$$

Then just regular old attention where $Q$ is learned as a set of inducing points times $W_q$.

To interpret every singal separately you need to have a time dimension. Feedforward neural networks with stacked observations works OK. Can also use an LSTM.

## Experiments

CartPoleSwingUp: 5 inputs, can permute the inputs because you process them separately. You can also extend that to 10 inputs and have 5 extra inputs as white noise.

Pong: Image patches, shuffle them. AttentionNeuron takes a list of unordered observation patches and constructs a 2D grid representation.

 - Basically, you have an output message of cardinality 12800 and reshape it into 20x20x32. Then pass that to a CNN which downsamples and expands channels, flattens and uses an FC layer.
 - Output message cardinality doesn't depend on length of the input, so you can mask out patches if you want.
 - "Interestingly an agent trained at a high occlusion rate of 80% rarely wins against the Atari opponent but once it is presented with the full set of patches during tests, it is able to achieve a fair result." Why?
 - Clustered the outputs: AttentionNeuron learns to cluster inputs that share similar features.

CarRacing:
 - Two layers of attention:
	 - First layer outputs a latent code book to represent a shuffled scene (eg, reshaped to $R^{32 \times 32 \times 16}$).
	 - Second layer selects top $K = 10$ codes from the 2D codebook.


Visualization of pathces that receive the most attention:

![[derl_attention_visualization.png]]

Big question for me: How is this different from an image-transformer policy when you drop the positional encodings and use set transformer? Permutation in this case literally does nothing to help the agent learn.

Paper claims that this helps "generalization" as a result and does not give a hypothesis as to why.