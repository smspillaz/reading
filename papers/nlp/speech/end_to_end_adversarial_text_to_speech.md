---
title: "End-to-End Adversarial Text-to-Speech."
venue: "CoRR"
volume: "abs/2006.03575"
year: 2020
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2006-03575"
ee: "https://arxiv.org/abs/2006.03575"
url: "https://dblp.org/rec/journals/corr/abs-2006-03575"
authors: ["Jeff Donahue", "Sander Dieleman", "Mikolaj Binkowski", "Erich Elsen", "Karen Simonyan"]
sync_version: 3
cite_key: "journals/corr/abs-2006-03575/Donahue/2020"
tags: ["DeepMind"]
---

# End-to-End Adversarial TTS

Modern TTS pipelines involve multiple processing stages, usually all decomposed and learned independently. Usually something like text normalization, featurization, mel-spectrogram synthesis, raw audio synthesis.

Drawbacks:
* Supervision at each stage
* Sequential training pipeline
* Can't really leverage "end-to-end" architecture. For example you can't get hints about mel-spectrogram synthesis from the word embeddings, this information is just lost and you're entirely reliant on the linguistic featureiation.

In this work, we look at synthesizing speech from normalized text or phonemes in an end-to-end manner. They call it EATS (End-to-end Adversarial TTS). Generate raw waveforms from text embeddings and try to discriminate this from real samples.

In this work they decompose into two submodules:

 * An *aligner* which processes the text and produces 200Hz aligned features in their own latent space.
 * A *decoder* which decodees the temporarily aligned linguistic features. Upsample from the aligner by 1D convolutions to produce 24KHz aveforms.

Then use some adversarial feedback and domain specific loss functions.

## Contributions

 * A fully-differentiable and efficient FF audio-aligner architecture that predicts the duration of each input token and produces an audio-aligned representation.
 * Use of flexible DTW based predition losses to enforce alignment with input conditioning while allowing the model to capture the variability of timing in human speech
 * A system that gets a mean-opinion-score of 4.083


## Method

### Loss Function

$$
\mathcal{L}_G = \mathcal{L}_{G, \text{adv}} + \lambda_{\text{pred}} \cdot \mathcal {L}''_{\text{pred}} + \lambda_{\text{length}} \cdot \mathcal {L}_{\text{length}}
$$

$\mathcal{L}_{\text{G, adv}}$ is the "adversarial loss" linear in the discriminator's output, paired with the hinge loss. The losses are mode-seeking

$\mathcal{L}_{\text{length}}$ and $\mathcal{L}_{\text{pred}}$ are the length and prediction losses, used by the aligner network and the auxiliary prediction.

## Aligner

Given a token sequence of length $N$, compute token representations $h = f(x, z, s)$ where $f$ is a stack of dilated convolutions and nonlinearities. The latents and speaker embedding $s$ modulate the sacle and shift parameters of the batchnorm layers.

Each token gets a predicted length: $l_{n} = g(h_n, z, s)$. The predicted token end positions are a cumulative sum of token lengths $e_n = \sum^{n}_{m = 1} l_m$ and token centre positions $cn = e_n - \frac{1}{2} l_n$. You can then interpolate the token representations into an audio-algined representation at 200Hz.

How do you get the interpolation weights? Use a Gaussian kernel.

By predicting the lenghs and then obtaining positions by using a cumulative sum, you enforce monotonicity.

## Windowed Generator

Can't pad all the sequences to a maximal length (20 seconds) during training.

Instead randomly extract a 2 second window, produce a 200Hz audio-aligned representation and decode it.

One problem: How do you know where you are in the text? They don't directly address this problem. Instead condition on the location of the two-second window and try to figure it out from there. You predict the token lengths but not their representations within each slot. Only predict within the window.

## Adversarial Discriminator

**Random Window Discriminator**:  Use RWDs of size 240, 480, 960, 1920, 3600, enabling each one to operate at a different resolution.. All discriminators are unconditional - they cannot access teh text. However they can access the speaker embedding.

**Spectrogram Discrimiantor**: Full training window in the spectrogram domain. Extract log-scale mel-spectrograms from audio and use BigGAN, so treat the spectrograms as images.

### Training Procedure

**What is required to learn alignment?**
  - Adversarial Feedback not enough: Aligner doesn't get an accurate alignment, so it looks like noise to the decoder, which just ignores it and tries to do unconditional prediction. That's also garbage, which means you don't learn anything. Essentially the ambiguity problem.
  - Guide learning with an explicit prediction loss in the spectrogram domain - minimize $L_1$ between log-scaled mel-spectrograms of the generator output and the training window.

Spectrogram prediction loss $\mathcal{L}_{\text{pred}}$ given by:

$$
\mathcal{L}_{\text{pred}} = \frac{1}{F} \sum^T \sum^F |S_{\text{gen}}[t, f] - S_{\text{gt}}[t, f]|
$$

$S_{\text{gen}}$ is the generated spectrogram and $S_{\text{gt}}$ is the ground-truth spectrogram. The loss is bascially just the absolute distance between the two.

**Why does this happen**? Seems to not be a problem in the autoregressive models. This is because those models have *teacher forcing* - you do next-step prediction and the ground truth is given for you

**Dynamic Time Warping** Iteratively find a minimal-cost laignment path $p$ between the genrated and target spectrograms. Its a greedy algorithm.

How does it work? Briefly: At each iteration $k$ do one of the following:

1. Go to the next timestep in both $S_{\text{gen}}$ and $S_{\text{gt}}$
2. Go to the next timestep in $S_{\text{gt}}$ only
3. Go to the next timestep in $S_{\text{gen}}$ only.

How do you pick it? Assign a cost based on the L1 distance between each $S_{\text{gen}}$ and $S_{\text{gt}}$ with a penalty $w$ for not advancing in lockstep (actions 2 or 3). Then you measure the loss along the warp path correspondences.

You can make this into a *dynamic programming* algorithm by determining the cost along *all paths*. Denote the set $\mathcal{P}$ as the set of all *valid paths* (eg, where the begin and end timesteps are aligned - we do not care about paths that start or end partway through the two sequences).

Then the cost of a path is:

$$
c_p = \sum^{K_p}_{k = 1} (w \cdot \delta_k + \frac{1}{F} \sum^F |S_{\text{gen}}[p_{\text{gen}, k}, f] - S_{\text{gt}}[p_{\text{gt}, k}, f]|)
$$

where $K_{p}$ is like the "degree of warping". The "hard" loss is then:

$$
\mathcal{L}_{\text{pred}} = \min_{p \in \mathcal{P}} c_p
$$

**Differentiability and Gradient Propagation of a sparse selection**: DTW is differentaible but the minimum across all paths makes optimization difficult since you only propagate gradients through that path. Solution, use a soft version of DTW, which replaces the minimum operation with a softmin:

$$
\mathcal{L}''_{\text{pred}} = -\tau \cdot \log \sum_{p \in \mathcal{P}} \exp{(-\frac{c_{p}}{\tau})}
$$

## Aligner Length Loss

Add a loss whcih encourages the predicted utterance length to be close to the ground truth length. Summing all token length predictions

$$
\mathcal{L}_{\text{length}} = \frac{1}{2} (L - \sum^N_{n = 1} l_n)^2
$$


## Text Pre-processing

Use *phonemizer* whih does partial normalization and phonemisation. Pre-pad and post-pad the sequence with "silence" tokens.