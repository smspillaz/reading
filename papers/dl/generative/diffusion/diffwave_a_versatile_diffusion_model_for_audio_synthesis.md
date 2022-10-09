---
title: "DiffWave - A Versatile Diffusion Model for Audio Synthesis."
venue: "ICLR"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/KongPHZC21"
ee: "https://openreview.net/forum?id=a-xFK8Ymz5J"
url: "https://dblp.org/rec/conf/iclr/KongPHZC21"
authors: ["Zhifeng Kong", "Wei Ping", "Jiaji Huang", "Kexin Zhao", "Bryan Catanzaro"]
sync_version: 3
cite_key: "conf/iclr/KongPHZC21"
---

Proposes DiffWave, a diffusion probabilistic model for conditional and unconditional waveform generation.

Nonautoregressive. Converts white noise into a waveform through a markov chain.

Matches a strong WaveNet vocoder in terms of speech quality while doing synthesis much faster.

## Introduction

Lots of diffferent ways to solve waveform generation:
 - Likelihood-based
 - Autoregressive
 - Flow-based
 - Distillation
 - VAE
 - GAN

Autoregressive models tend to generate made-up word-like sounds or inferior samples under unconditional settings. The main problem is that you have to deal with very long sequences.

## Diffusion models

**Diffusion Probabilistic Models**: Use a markov chain to gradually convert from a simple distribution into a complicated one. Optimize the ELBO. Works well on image synthesis [[diffusion_models_beat_gan_on_image_synthesis]].

Diffusion models use a noise-adding process without learnable parameters to obtain "whitened" latents. You don't need an additional network which you then throw away later like in GAN.

# DiffWave

 - It is non-autoregressive, so you can synthesize high-dmension waveforms in parallel
 - It is lfexible: does not impose any architectural constraints
 - Uses a single ELBO-based training objetive without any auxiliary losses
 - It is versatile: produces high quality audio signals for both conditional and unconditional waveform generation.

## Contributions

1. DiffWave uses Feed-forward and bidirectional dilated convolutions motivated by WaveNet.
2. A small DiffWave has 2.64M parameters and synthesizes 5x fater on a V100 GPU.
3. DiffWave outperforms WaveGAN and WaveNet in the unconditional and class-conditional waveform generation tasks.


## Diffusion probabilistic models

A diffusion process is a fixed Markov chain:

$$
q(x_1, ..., x_T|x_0) = \prod^T q(x_t|x_{t - 1})
$$

where each $q(x_t|x_{t - 1}) \sim \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t - 1})$. Add small Gaussian noise to distribution of $x_{t - 1}$. Convert data to whitened latents via a variance schedule $\beta_0, ..., \beta_T$.

The *reverse* process is this markov chain:

$p_{\text{latent}} = \mathcal{N}(0, I)$ and $p_{\theta}(x_0, ..., x_{T - 1}|x_T) = \prod^T p_{\theta}(x_{t - 1}|x_t)$ where $p_{\text{latent}}$ is diagonal-covariance gaussian and the transition probability is $\mathcal{N}(x_{t - 1}; \mu_{\theta}(x_t, t), \sigma_{\theta}(x_t, t)^2)$ . Both $\mu_{\theta}$ and $\sigma_{\theta}$ take two inputs - the diffusion step and the variable $x_t \in \mathbb{R}^L$. This process *eliminates* the Gaussian noise added during diffusion.

**Sampling**: Given the reverse process, the generative procedure is to sample some noise, then sample $x_{t - 1} \sim p_{\theta}(x_{t - 1|x_t})$ for $t = T, ..., 0$.

**Training**: $p_{\theta}(x_0) = \int p_{\theta}(x_0, ..., x_{T - 1}) p_{\text{latent}}(x_T) d x_{1:T}$. This likelihood is intractible. Maximize the EBLO

$$
\begin{aligned}
\mathbb{E}_{q_{\text{data}}} \log p_{\theta}(x_0) &= \mathbb{E}_{q_{\text{data}(x_0)}} \log E_{q(x_{1:T}|x_0)}) [\frac{p_{\theta} (x_0, ..., x_{T - 1}|x_T) p_{\text{latent}}(x_T)}{q(x_{1:T}|x_0)}] \\
&\ge \mathbb{E}_{q(x_{0:T})} \log \frac{p_{\theta}(x_{0:T}|x_T) p_{\text{latent}}(x_T)}{q(x_{1:T}|x_0)}
\end{aligned}
$$

Unpacking:
 - We maximize the expected likelihood of the data from the noise-diffusion process by maximizing the likelihood that the diffusion process matches the diffusion (noising) process

Some recent work by Ho et al showed that ELBO can be computed in closed form, which avoids the monte carlo estimates. This is motivated by denoising score matching (see also [[score_based_generative_modeling]]). Define some constants based on a variance schedule:

$$
\alpha_t = 1 - \beta_t, \bar{a}_t = \prod^t \alpha_s, \tilde{\beta}_t = \frac{1 - \bar{\alpha_{t - 1}}}{1 - \bar{\alpha_t}} \beta_t
$$

Then redefine $\mu_{\theta}$ and $\sigma_{\theta}$ as:

$$
\mu_{theta}(x_t, t) = \frac{1}{\sqrt{\alpha_t}}(x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_{\theta}(x_t, t))
$$

$$
\sigma_{\theta}(x_t, t) = \tilde{\beta}_t^{(-\frac{1}{2})}
$$

where $\epsilon_{\theta} : \mathbb{R}^L \times \mathbb{N} \to R^{L}$, a NN taking $x_t$ and the diffusion step $t$ as inputs.


This allows reparameterizing the ELBO as:

$$c + \sum^T \kappa_t \mathbb{E}_{x_0, \epsilon} || \epsilon - \epsilon_{\theta}(\sqrt{\bar \alpha_t} x_0 + \sqrt{1 - \bar{\alpha}_t \epsilon})||^2_2$$

where $\kappa_t$ is a weight, $\frac{\beta_t}{2 \alpha_t(1 - \bar{\alpha}_{t - 1})}$

The ELBO is a sum of KL divergences between tractable Gaussians. You can also drop the weight and just optimize the unweighted version.

**Fast Sampling**: You can also reduce the number of denoising steps, since most of the denoising happens at the first few steps.

## Network architecture of $\epsilon_{\theta}$

![[diffwave_network_architecture.png]]

$\epsilon_{\theta}$ is a bidirectional dilated convolutional architecture, whcih is different from WaveNet.

How does it work?

You have inputs and embeddings of each diffusion step. There are skip connections between each step and its prior steps.

One of the elements is a "Bidirectional Dilated Convolution" where dilation is $2^{\tau}$ similar to WaveNet.

Note that each step generates one entire audio sample of length $L$ and the audio sample is refined at each step for $T$ steps. The kernel size at each layer is 3. (The idea behind the dilation is probably to diffuse different frequencies)

## Why do you need a step embedding?

Its important to include an embedding of the step. Use a positional encoding:

$$
t_{\text{embedding}} = [\sin (10^{\frac{4 \times 0}{63}}, ...\sin (10^{\frac{4 \times 63}{63}}, \cos (10^{\frac{4 \times 0}{63}}, ..., \cos (10^{\frac{4 \times 63}{63}} )]
$$

These are sort of like fourier features.


## Conditional Generation

Local conditioner: Condition on the mel spectrogram

Global conditioner: Speaker id or word ids. Shared embeddings.

## Unconditional generation

Need to generate consistent utterances without conditional information. The receptive field needs to have a length larger than the desired size $L$.

DiffWave the advantage of enlarging the receptive fields of output $x_0$ by iteration from $x_T$ to $x_0$ in the reverse process.



