---
title: "Style Transfer of Audio Effects with Differentiable Signal Processing."
venue: "CoRR"
volume: "abs/2207.08759"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2207-08759"
doi: "10.48550/ARXIV.2207.08759"
ee: "https://doi.org/10.48550/arXiv.2207.08759"
url: "https://dblp.org/rec/journals/corr/abs-2207-08759"
authors: ["Christian J. Steinmetz", "Nicholas J. Bryan", "Joshua D. Reiss"]
sync_version: 3
cite_key: "journals/corr/abs-2207-08759/Steinmetz/2022"
---
Impose audio effects and production style from one recording to another by example.

Predict the control parameters of the audio effects used to render the output.

Audio effects integrated by differentaible operators.

The point is the restrict the flexibility of the model such that processing artifacts are removed.

The basic architecture is to encode both the input and the reference sample, then determine the settings for audio effects to apply such that it makes the input like the reference sample.

## How do differentiable audio effects work?

Its better to implement them in the frequency domain as opposed to the time domain

## Neural Proxy Approaches

A neural network is trained to emulate teh behaviour of a signal processor.

 - Half-hybrid approaches: Use the proxy during the forward and backward pass of training, but use the DSP during inference
 - Full-hybrid approaches: Use the DSP device during inference and training forward pass, but not the backward pass.

## Self-supervised training

Select some random audio recording, augment by applying some filters like pitch=shift and time stretching.

The recordings are also split in half. During trianing, randomly select either $a$ or $b$ section as input, then use the other section as the refernce.

## Architecture

 - Convolutional network, time series of embeddings
 - Temporal average pooling
 - Controller network is an MLP, which produces some parameters to configure a set of audio effects.


## Loss

Audio-domain loss. Time-domain MAE and frequency-domain L1 distance between STFT of ground truth and estimated waveforms at different window sizes.