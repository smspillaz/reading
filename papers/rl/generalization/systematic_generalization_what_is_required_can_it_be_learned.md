---
title: Systematic Generalization - What Is Required and Can It Be Learned?
venue: ICLR
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/iclr/BahdanauMNNVC19
ee: https://openreview.net/forum?id=HkezXnA9YX
url: https://dblp.org/rec/conf/iclr/BahdanauMNNVC19
authors: ["Dzmitry Bahdanau", "Shikhar Murty", "Michael Noukhovitch", "Thien Huu Nguyen", "Harm de Vries", "Aaron C. Courville"]
sync_version: 3
cite_key: conf/iclr/BahdanauMNNVC19
---

Examines systematic generalization within the grounded language understanding context.

Compares generic models with "intuitively appealing modular models that require background knowledge to be instantiated". How much do they lend themselves to systematic generalization?

The generalization of modular models is much more systematic *but* it is highly sensitive to the module layout.

If modular models generalize well, they could be made *more* end-to-end by learning their layout and parameterization. End-to-end methods often learn inappropriate layouts or parameterizations.

Neural Module Network paradigm: A neural network is assembled from several neural modules, where each module performs a particular subtask. The main problem is the large amount of domain knowledge that is required to decide how the modules should be created or connected. Also performace has been matched by "just using FiLM".

Requirement of systematic generalization: One good model should be able to reason about all possible object combinations despite being trained on a very small subset of them.

New synthetic dataset: Spatial Queries on Object Pairs (SQOOP). Evaluated on all object pairs, trained on a subset.

# SQOOP Dataset

Minimalistic VQA task designed to test ability to interpret unseen combinations of known relation and object words. Given $X$, $Y$ and $R$, answer whether $X$ and $Y$ are in relation $R$. (eg, "is there a cup on the table"). The statements are machine-generated.

Each image contains 5 randomly chosen and positioned objects. To make negative example schallenging, ensure that both $X$ and $Y$ are always present in the associated image and that there are distractor objects that that the relation might be true for different sets.

Split: Each object appears in at least one question.

# Models

## Generic

1. CNN/LSTM
2. FiLM [[film]]
3. RelNet [[relnet_a_simple_neural_network_module_for_relational_reasonign.pdf]]
4. Memory-attention-control [[compositional_attention_networks]]

For the first three, encode the question into a fixed size representation using an LSTM.

RelNet uses a network $g$ which is applied to all pairs of feature columns (eg, channels) of $h_x$ (the encoded image) concatenated with the question to pool thme into $h_{qx}$ over both spatial dimensions.

FiLM weights channels according to the language representation.

MAC produces $h_{qx}$ by repeatedly applying a memory-attention-composition cell conditioned on the question through attention.

## Neural Module Networks
Construct a computation graph manually by answering:

a) How many modules will be used (layout)
b) How are the modules connected? (layout)
c) How are these modules parameterized? (parameterization)

Different module types used to perform different computations:

 - Find: Trainable computations on attention map
 - And: Element-wise maximum for two attention maps

End-to-End NMN: Learnable mechanisms and modules.

Repeatedly apply a generic neural module $f(\theta, \gamma, s^0, s^1)$ which takes inputs are shared parameters $\theta$, question specific parameters $\gamma$ and lhs/rhs inputs $s^0$ and $s^1$.

$$
\gamma^k = \sum^3 \alpha^{k, i} e(q_i)
$$

$$
s^m_k = \sum^{k - 1}_{j = -1} \tau^{k, j}_m s_j
$$

$$
s_k = f(\theta, \gamma_k, s^0_k, s^1_k)
$$

Refer to $A = (\alpha^{k, i})$ and $T(\tau^{k, j}_m)$ as the parameterization attention matrix and lyout tensor respectively.

Residual Module: All parameters depend on the convolution weights

Find Module: Only the elementwise multipliers change depending on the question.

### Sub-architectures

NMN Chain: Modules form a chain

NMN Chain Shortcut: Give image features as the right hand side input to all 3 modules

NMN Tree: Change connectivit yto be tree-like

Stochastic N2NMN: Treat the layout $T$ like a stochastic latent variable.

Attention N2NMN: Use the end-to-end method to learn the parameterization, $\alpha^k$ was computed as a softmax over logits.


# Experiments

NMN-Tree exhibits strong systematic generalization

MAC is the strongest competitor.

## What is essential to strong generalization?

No language encoder, instead built from modules that are parameterized by question words directly.

Structured in a paritcular way with the idea that modules 1 and 2 learn to identify objects and module 3 learns to reason about object locations independently of their identitites.

## Can we induce Neural Module Networks?

## Parameterization Induction

# Conclusions