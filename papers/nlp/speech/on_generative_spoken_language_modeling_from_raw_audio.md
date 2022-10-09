---
title: "On Generative Spoken Language Modeling from Raw Audio"
---
Introduces Generative Spoken Language Modelling - learning acoustic and lingustiic characteristics of language from raw audio.

In this case we study training the LM directly from audio and no text.

The high-level idea is that automatically discovered discrete units can be used to encode speech into "pseudo-text", which is use dto train a generative language model and train a speech synthesizer. In this sense, there's no "internal" representation of text or tokens at all, instead you encode quantized tokens, then decode a waveform from quantized tokens.

In this paper they also address model evaluation. This is sort of hard because speech is continuous

Contributions:

1. Two novel evaluation matrics for the generation mode of spoken language modelling. Use a  generic pretrained ASR system to establish model-independent assessments of the inteligiblity and meaningfulness of the produced outputs.
2. Validate these metrics with human evaluation
3. Show that these metrics are correlated with other metrics
4. Systematically study the effect of the type of encoding units.

## Evaluation Metrics

1. Speech resynthesis (S2u, encode speech into units and u2S which deocdes its back itno speech). Measure *intelligibility*.
	1. Phone-error-rate (acoustic model ASR without additional language model)
2. Speech generation and diversity: AUC on Perplexity and VERT


# System

Speech-to-unit models

 - Contrastive Predictive Coding: Encoder/predictor - predict your own future latent states, use contrastive loss.
 - wav2vec
 - HuBERT:  Tasked unit modelling


Unit-language model:
 - Transformer

Unit to speech:
 - Tacotron 2: Pseudo-text inputs, mel-spectrogram outputs
 -