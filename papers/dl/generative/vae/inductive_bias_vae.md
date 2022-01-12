---
title: On incorporating inductive biases into VAEs
---

# On incorporating inductive biases into VAEs (InteL-VAE)

 - InteL-VAE uses an intermediary set of latents to control the stochasticity of the encoding process before mapping these in turn to the latent representation.
 - This allows you to impose properties like sparsity or clustering on learned representations.



Standard VAE assumes isotropic Gaussian prior. But issues when one desires the learned representations to exhibit some properties of interest like sparsity or clustering .

Can we use non-Gaussian priors?

 - This can be problematic because
	 - Non-Gaussian priors necessitate complex encoder models, which no longer permits simple parameterization.
	 - Latent encodings not guaranteed to follow the desired structure and the prior is not really ap rior in the bayesian sense and is only a regularizer.
	 - Changing the prior is typically insufficient to learn the desired representations at the population level.


## InteL-VAE - this model

![[intel_vae_figure.png]]

 - First map to $y$ using a Gaussian encoder
 - then map to $z$ using a mapping function $g_{\psi}(y) \to z$
 - Decode from $z$.

## Why do we need an inductive bias in VAE?

 - Sparse features can be desirable because they can improve data efficiency and provide robustness to noise.
 - One might desire clustered, disentangled or hierarchical representations.
 - Standard Gaussian distribution doesn't give you desired characteristics.


For the generator this is also difficult. If your data really isn't well represented by a Gaussian, say because its bimodal, your encoder is going to try and turn it into something that's unimodal, then decoding it back into something that's bimodal is not going to work very wel.

## Why a non-Gaussian prior isn't enoguh.

Only influence that the prior has is as a regularizer on the encoder through the KL term. This is competing with the need for effective reconstructions and only has an indirect influence on the $q$ distribution.

This can be hard if $p(z)$ is a complex distribution that is difficult to fit. Its much easier to estimate a complex distribution with a single wide gaussian than it is to try and fit a complex distribution to it which might be a mismatch.

## InteL-VAE Framework

Introduce an intermediary set of latent variables $y$ used as a stepping stone in the construction of the representation $z$. Go from $y$ to $z$ using $g_{\psi}(y) \to z$

The prior on $y$ is just a standard Gaussian.

Note that $g_{\psi}(y) \to z$ can be whatever you want. It doesn't have to be learned, differentiable or anything like that (but its more convenient for end-to-end training if it is differentaible).

How to train them:

 - Maximizing the ELBO on the log-evidence and minimizing KL between $q$ and the normal distribution on the encoded $y|x$.


## Specific Realizations of the InteL-VAE framework / dealing with multi-modality etc

 - Design a mapping $g_{\psi}$ with a localized high-Lipschitz constant that splits the continuous Gaussian into K disconnected parts and pushes them away from each toher.
 - Example: MNIST and MNIST-01. This is strongly clustered. Decrease the latent dimension to 1. Halfway between you get mixing between 0 and 1. This is not ideal.


## Sparsity

 - InteL-VAE can simultaneously increase sparsity and generation quality
 - In this case $g_{\psi}$ needs to be a more flexible function so ithat it can both map the points in a data-specific way and induce sparsity without harming reconstruction.
 - Use $g_{\psi} = y \cdot \text{DS}_{\psi}(y)$ where $\text{DS}$ is a "dimension selector". Sigmoid for each dimension bascially. The more dimensions deactivated, the more sparse the representation.
 - Add a sparsity regularizer to the ELBO:
	 - $L_{\text{sp}}(\phi, \psi) = E[\frac{1}{M} \sum^M (H(\text{DS}(y_i))) - H(\frac{1}{M} \sum^M \text{DS}(y_i))]$
	 - What does this do? It says that you want the mean entropy of each individual sample weight to be *low* and the entropy of the mean weights to be *high*
	 - This basically ensures that you have both diversity between samples, but also sparsity within samples.

