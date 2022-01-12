---
title: Diffusion Models Beat GANs on Image Synthesis.
venue: CoRR
volume: abs/2105.05233
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2105-05233
ee: https://arxiv.org/abs/2105.05233
url: https://dblp.org/rec/journals/corr/abs-2105-05233
authors: ["Prafulla Dhariwal", "Alex Nichol"]
sync_version: 0
---

# Diffusion models beat GANs on image synthesis (Guided Diffusion)

GANs currently hold the SOTA on most image generation tasks, but GANs capture less diversity than SOTA likelihood-based models due to mode collapse. They're also hard to train.

Diffusion models are a class of likelihood based modles which produce high quality images while offering desirable properties such as distribution coverage, stationary training objective and easy scaleability. They work by gradually removing noise from the signal.

The current gap probably comes from:
(1) Poor model architeture
(2) GANs trade off diversity for fidelity


Contributions:
 - Improving model architecture
 - Devising a scheme to do the diversity/fidelity tradeoff


## Architecture Improvements

U-Net seems to help a lot, with glboal attention layer at 16x16 resolution with a single head.

 - More heads or lower channels per head both improves FID
 - Mutli-resolution attention helps
 - Using the BigGAN residual block helps

### Adaptive Group Normalization

Basically, $\text{GroupNorm}(h) + y_b$. Incorporates both a timestep and class embedding into each residual block after group normalization operation. Similar to FiLM.

## Classifier to improve the diffusion generator

A pre-trained diffusion model can be conditioned using the gradients of a classifier.

Train a classifier $p_{\phi}(y|x_t, t)$ on noisy images $x_t$ and use gradients $\triangledown_{x_t} \log p_{\phi}(y_{x_t}, t)$ to guid ethe diffusion sampling processes towards an arbitrary class label $y$.

### Conditional Reverse Noising

Each transition is sampled as $p_{\theta, \phi}(x_t|x_{t + 1}, y) = Z p_{\theta}(x_t|x_{t + 1})p_{\phi}(y|x_t)$

This can be approximated as a Gaussian.

Classiier guided diffusion sampling, given a diffusion model, classifier and a gradient scale $s$:
 - Input: class label $y$ and gradient scale $s$
 - Sample $x_T$ from the normal distirbution
 - for $t$ to $T$
	 - get $\mu$, $\Sigma$ from the diffusion model
	 - $x_{t - 1}$ sample from $N(\mu + s \Sigma \triangledown_{x_t} \log p_{\phi} (y|x_t))$


### Conditional Sampling for DDIM

## Scaling the classifier gradients (diversity/fidelity tradeoff)

A larger graident scale focuses more on modes of the lcassifier, which produces higher fidelity but less diverse samples.