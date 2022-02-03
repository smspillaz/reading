---
title: Score-Based Generative Modeling through Stochastic Differential Equations.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/0011SKKEP21
ee: https://openreview.net/forum?id=PxTIG12RRHS
url: https://dblp.org/rec/conf/iclr/0011SKKEP21
authors: ["Yang Song", "Jascha Sohl-Dickstein", "Diederik P. Kingma", "Abhishek Kumar", "Stefano Ermon", "Ben Poole"]
sync_version: 3
cite_key: conf/iclr/0011SKKEP21
---

# Score based Generative Modeling through Stochastic Differential Equations

The usual generative modelling problem. We want to turn noise into something that looks like a realistic image.

Easy to turn realistic images into noise. Just keep adding noise until you end up with iid noise. Can we reverse this process somehow?

Basic idea of learning a generative model by corrupting with noise:

 (1) Score Matching with Langevin Dynamics (estimate the score at eahc noise scale, then use Langevin dynamics to sample from a sequence of secreasing noise scales during each generation)
 (2) Denoising diffusion probabilistic modelling: Train a sequence of probabilistic models to reverse each step of the noise corruption, using knowledge of the functional form of the reverse distributions to make training tractable.

 ![[score_based_generative_model_reverse_time_sde.png]]

 The basic idea behind this model is that if you know the gradient of the noise, then you can make a reverse stochastic differentiable equation.

 You can derive the reverse-time SDE from the forward-time SDE given the score of the marginal proability densities as a function of time.

 Contributions:
  - Flexible sampling and likelihood computation: Use any general-purpose SDE solver to integrate the reverse-time SE for sampling. Also propose:
	  - Predictor-corrector (combine numerical SDE solver with MCMC approach) (unifies and improves)
	  - Deterministic samplers: based on probability flow ODE. (fast adaptive sampling)
  - Controllable generation: eg, class-conditional generation, image inpainting, colorization and other inverse problems.
  - Unified framework: Single theory that explains SMLD and DDPM.


## SMLD

Let $p_{\sigma}(\tilde x|x)$ be a perturbation kernel (eg, noise with mean $\tilde x$ and variance $\sigma^2$. Then $p_{\sigma} = \int p_{\text{data}}(x)p_{\sigma}(\tilde x | x)$.

If we consider some positive noise scales that go from $\sigma_{\text{min}}$ to $\sigma_{\text{max}}$, then the min scale is small enough such that $p_{\sigma_{\text{min}}}(\tilde x | x) \approx p_{\text{data}}(x)$ and $\sigma_{\text{max}}$ is large enough that you get iid noise.

A Noise-conditional-score-network is a weighted-sum of denoising score-matching:

$$
\theta^* = \arg \min_{\theta} \sum^N \sigma^2 E_{p_{\text{data}}}[E_{p_{\sigma_i}(\tilde x | x)}[ ||s_{\theta}(\tilde x, \sigma_i) - \triangledown_{\tilde x} \log p_{\sigma_i} (\tilde x | x) ||^2_2 ]]
$$

Or in other words: the parameters of the NCSN minimize the expected MSE loss of the estimated score of the data given the scale and the actual score of the data given the scale.

Then with enough training and model capacity, for all $i$, $x_1^M$ becomes an exact sample from $p_{\sigma_{\text{min}}}(x) \sim p_{\text{data}}(x)$.

## DDPM

Denoising diffusion probabilistic models

Consider a sequence of positive noise scales.

Construct a discrete Markov chain such that $p(x_i|x_{i - 1}) = N(x_i; \sqrt{1 - \beta_i} x_{i - 1}, \beta_i I)$ and therefore $p_{\alpha_i}(x_i, x_0)  = N(x_i; \sqrt{a_i} x_0, (1 - \alpha_i) I)$ where $\alpha_i = \prod^i_j (1 - \beta_j)$,

Then train a re-weighted variant of the ELBO as above.

Then you generate samples from a reverse markov chain.

This is called *ancestral sampling*

## Score-based generative modelling

![[score_based_generative_modelling_sde.png]]

The main insight from the prior work is that perturbing the data with multiple noise scales is the key to success of many previous methods. So *generalize* this idea to infinite number of noise scales, such that perturbed data distributions evovled according to SDE as noise intensifies.

Map data to a noise distribution (prior) with an SDE and reverse this SDE for generative modelling.

Basically, construct a diffusion process indexed by continuous time $t \in [0, T]$ such that $x(0) \sim p_0$ where which we have a dataset of iid samples.

So $p_0$ is the data distribution and $p_T$ is the prior distribution.

$$
x = f(x, t) dt + g9t) dw
$$

where $w$ is Brownian motion and $f(\cdot, t)$ is a vector-valued function called the drift coefficient of $x(t)$. Finally $g(\cdot)$ is a scalar function known as the *diffusion coefficient* of $x(t)$.

## How to reverse the SDE and generate samples

Starting from samples of $x(T) \sim p_T$ and reversing the process, we can obtain samples form $x(0) \sim p_0$ (eg, the data distribution itself).

The reverse of a diffusion process is also a diffusion process:

$$
dx = [f(x, t) = g(t)^2 \triangledown_x \log p_t (x)] dt + d(t) dw
$$

where $w$ is a Wiener process with time running backwards from $T$ to $0$. *Once the score function $\triangledown_x \log p_t(x)$ is known for all $t$,
then we can reverse the diffusion process from Equation 6 and simulate it to sample from $p_0$*.

## How to estimate the scores for the SDE?

Basically - train a score-based model on samples with score-matching.

$$
\theta^* = \arg \min_{\theta} \sum^N \sigma^2 E_{p_{\text{data}}}[E_{p_{\sigma_i}(\tilde x | x)}[ ||s_{\theta}(x(t), t) - \triangledown_{x(t)} \log p_{\sigma_i} (x(t) | x(0)) ||^2_2 ]]
$$

All we did was replace $\tilde x$ with $x(t)$.

## Solving the reverse SDE

After training time-dependent score-based model $s_{\theta}$ you can use it to construct reverse-time SDE and simulate it with numerical approaches to generate samples from $p_{0}$.

### Predictor-corrector samplers

We have additional information which can be used to improve solutions.

Since we use a score-based model, we can do score-based MCMC to sample from $p_t$ directly and correct whatever solution the SDE solver gives us.

(1) Get the result of the numerical SDE solver at the next timestep (predictor)
(2) Use score-based MCMC to correct the marginal distribution of the estimated sample, correcting the prediction.


### Probabiluity flow and connection to neural ODEs

For all diffusion processes, there eixsts a corresponding deterministic process whose trajectories share the same marginal probability densities as the SDE

$$
dx = [f(x, t) - \frac{1}{2} g(t)^2 \triangledown_x \log p_t(x)] dt
$$

which can be determined once the scores are known.

This allows you to compute the exact likelihood on any input data.

Main reuslts:
 - For the same DDPM model, we obtain better bits/dim tahn ELBO, since likelihoods aer exact
 - Using the same architecture, train another DDPM model with continuous objective which further improves the likelihood


### Latent manipulation

Because the model is invertible, we can manipulate hte latent representation for image editing (interpolation, temperature scaling, etc).

## Controllable Generation

The fact that the framework is continuous allows you to produce data samples from $p_{0}(x(0)|y)$ if $p_t(y|x(t))$ is known.

Start from $p_T(x(T)|y)$ and solve a conditional reverse-time SDE.

Applications:
 - Class conditional generaton
	 - First sample $(x(0), y)$ from the dataset and obtain $x(t) \sim p_{0_t}(x(t)|x(0))$. We can train a time-dependent classifier $p_t(y|x(t))$
 - Imputation: You have an incomplete data point, sample from $p(x(0)|\Omega(y))$
	 - The drift coefficient is element-wise and the diffusion coefficient $G(\cdot, t)$ is diagonal.
 - Colorization


## Drawbacks

 - Still slower than GANs