---
title: Disentangled Recurrent Wasserstein Autoencoder.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/HanMHLZ21
ee: https://openreview.net/forum?id=O7ms4LFdsX
url: https://dblp.org/rec/conf/iclr/HanMHLZ21
authors: ["Jun Han", "Martin Renqiang Min", "Ligong Han", "Li Erran Li", "Xuan Zhang"]
sync_version: 3
cite_key: conf/iclr/HanMHLZ21
---
# Disentangled Recurrent Wasserstein Autoencoder

https://iclr.cc/virtual/2021/poster/3257

Represention learning of sequential data

![[representation_learning_sequential_data_example.png]]

 - Disentangle static latent code $z^c$ from dynamic latent code $s_t^m$ of sequential data
 - Unconditionally generate new samples.

$z^c$ doesn't change between the frames. $z_t^m$ changes between the frames.

![[structure_sequential_probabilistic_models.png]]

Use variational inference to learn an approximate posterior for inference model:

$$Q_{\phi}(Z^c|X_{1:T}) \Pi^T Q_{\phi} (Z_t^m|Z_{<t}^m, X_t)$$

Generative model

$$P(X_{1:T}, Z_{1:T}) = P(Z^c) \Pi^T P_{\psi} (Z_{<t}^m|Z^m_{<t})P_{\theta}(X_t|Z_t^m, Z^c)$$

The generative model depends on the corresponding latent variables at time t and the static latent.

Wasserstein Metric for Distributions wth Sequential Variables.

Optimal transport cost for distributions $X_{1:T}$ and $Y_{1:T}$ is:

$$
W_{P_D, P_G} = \text{inf}_{\Gamma \sim P(X_{1:T} \sim P_D, Y_{1:T} \sim P_G)} E[c(X_{1:T}, Y_{1:T})]
$$

And $P(X_{1:T}) \sim P_D, Y_{1:T} \sim P_G)$ is the set of all joint distributions with marginals $P_D$ and $P_G$ respectively.

When $Z^C$ and $Z^m_{1:T}$ are independent, the Wasserstain distance is given by:

$$
W_{P_D, P_G} = \text{inf}_{Q:Q_{z^c}=P_{z^c}, Q:Q_{z^m_{1:T}}=P_{z^m_{1:T}}} \sim P_D, Y_{1:T} \sim P_G)} E_{P_D}E_{Q(Z_t|Z_{<t},X_t)}[c(X_{1:T}, Y_{1:T})]
$$

Where $c(X_t, G(Z_t))$ is a reconstruction loss and $\text{inf}_{Q:Q_{z^c}=P_{z^c}, Q:Q_{z^m_{1:T}}=P_{z^m_{1:T}}}$ are the constraints.

The marginal distributions of the prior and posterior should match.

We can relax this constraint to a subset. We have an upper bound for practical optimization.

Therefore the loss function for R-WAE is:

$$
\sum^T E_{q(z_t|z_{<t, x_t})}[c(x_t, G(z_t))] + \beta_1 D(Q_{Z^c}, P_{Z^c}}) + \beta_2 \sum^T D(Q_{Z^m_t|Z^m_{<t}}, P_{Z^m_t|Z^m_{<t}})
$$

The terms given by $\beta$ are the regularization terms. They can be implemented by either GAN or MMD.

In this work they use MMD.

R-WAE minimizes an upper bound of Wasserstein distance between the model distribution and the target distribution.

R-WAE maximizes a lower bound of the mutual information between input and latent factors.

With KL divergence, regularizers in R-WAE jointly minimize KL between inference distribution and prior distribution and maximizet he mutual information between $X_{1:T}$ and $Z_{1:T}$ (which are $Z^C$ and $Z^m_t$)

Qualitative results.

[[qualitative_results_recurrent_wasserstein_autoencoder.png]]

R-WAE is able to generate smooth motion. Compare to MoCoGAN which changes the digit identities along the latent sweep.

## Weakly supervised model

Only the total number of actions is known.

## Limitation

Model might fail on video datasets with multiple foreground objects and complex background seens

Model might fail to disentangle fine-grained attributes within content and motion.