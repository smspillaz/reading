---
title: PonderNet: Learning to Ponder.
venue: CoRR
volume: abs/2107.05407
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2107-05407
ee: https://arxiv.org/abs/2107.05407
url: https://dblp.org/rec/journals/corr/abs-2107-05407
authors: ["Andrea Banino", "Jan Balaguer", "Charles Blundell"]
sync_version: 3
cite_key: journals/corr/abs-2107-05407/Banino/2021
---
# PonderNet: Learning to Ponder

[[pondernet_learning_to_ponder.pdf]]

Prior work:
 - Adaptive Computation Time: Halting probability as a learnable scalar parameter
 - Adaptive Early Exit Networks: Terminate forward pass if part of the network used so far predicts correct answer
 - Usage of REINFORCE to perform conditional computation with a discrete latent variable.

PonderNet is like ACT in that they have a halting policy, but this is now a probabilistic model instead of being a fixed porbability.

Architecture:
 - Halting node predicts probability of halting conditional on having not halded beore (geometric distrbution)
 - Loss: Don't regularize PonderNet to minimize computation steps but instead incentivise exploration.
 - Inference: Probabilistic both in terms of computation steps and prediction produced.

The network produces three outputs:

$$
\hat y_n \gamma_n \text{ and } h_{n + 1}
$$
$\hat y_n$ is the scalar probability of halting at step $n$. $h_n$ is a hidden state and $\lambda_n$ is a scalar probability of halting at step $n$.

Rely on $\lambda_n$ to learn the learn the optimal value of $n$. $\Lambda_n$ is the bernoulli random variable represnting a markov process for halting.

$$
P(\Lambda_n = 1|\Lambda_{n - 1} = 0) = \lambda_n
$$

We condition on halting at step $n$ having not halted at $n - 1$.

Then you can estimate the probability of halting at $N$ by $p_n = \lambda_n \prod^{n - 1} (1 - \lambda_j)$

The prediction of PonderNet is the prediction made at the step $n$ at which it halts, which makes the predictions probabilistic in a sense.

## Loss Function

$$
L = \sum^N p_n \mathcal{L}(y, \hat y_n) + \beta \text{KL}(p_n||p_G(\lambda_p))
$$
$\mathcal{L}(y, \hat y_n)$ is any old prediction loss (note that we measuer the prediction loss *at each step* weighted by the probability of termination *at that step*).

The KL term is the KL between the halting probability and the prior which is a geometric distribution parameterized by $\lambda_p$.


## Evaluation Sampling

Sample first $\lambda$ to decide whether to continue or stop, the final point becomes the prediction.

Note that in training you DONT sample whether to stop. Instead the $\lambda_i$ is a weight on the loss function evaluations.

KL is in the same units as information theoretic losses such as cross-entropy.

## Experiments
1. Parity bit
2. bAbI Question Answering
3. Paired Associative Inference
4.


## Difference between PonderNet and ACT

PonderNet and ACT have the same step function, but the difference is how the halting node is used.

In ACT, you unroll until $\sum \lambda_n \ge 1 - \epsilon$. The output is not probabilistic but rather a weighted average over the outputs at each step: $\hat y = \sum^N_{\text{ACT}} \hat y_n \lambda_n$

In PonderNet the output is probabilistic - you halt and then take the output at the step where you halted. Instead you have a weighted average *loss*.

Also in PonderNet, the pondering process wraps the entire network, so if you process a sequence the step is in the outer loop, eg, process sequence, decide whether to halt, if no, process sequence again conditioned on previous input.