---
title: "Chunked Autoregressive GAN for Conditional Waveform Synthesis."
venue: "ICLR"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/MorrisonKKSCB22"
ee: "https://openreview.net/forum?id=v3aeIsY_vVX"
url: "https://dblp.org/rec/conf/iclr/MorrisonKKSCB22"
authors: ["Max Morrison", "Rithesh Kumar", "Kundan Kumar", "Prem Seetharaman", "Aaron C. Courville", "Yoshua Bengio"]
sync_version: 3
cite_key: "conf/iclr/MorrisonKKSCB22"
---

Learn a distribution of audio waveforms given some conditioning.

GAN produces artifacts. This happens because of inability to learn accurate pitch and periodicity.

Chunked AR-GAN produces pitch error by 40-60% and reduces training time by 58%.

In the paper they demonstrate a close relationships between pitch-phase and autoregression. Autoregressive models provide a good inductive bias for learning pitch and phase.

The main problem behind non-autoregressive GAN is that you do feature-matching loss. Feature matching loss has an L1 distance between all activations, so this means that you have to produce the correct waveform after one convolution and nonlinearity. So the generator needs to know the initial phase and this is not known in a non-autoregressive setting.

Relationship between autoregression, pitch and phase:

A perfectly periodic signal can be produced autoregressively. Eg, to compute the phase, compute $\phi_t = \phi_{t - 1} + \frac{2\pi}{r} f_t$.

Given a generator, what is the maximum length cumulative sum that it can learn? It is (m + 1)/2. You can learn a cumulative sum with length equal to causal receptive field.

## Chunked AR GAN

Previously generated samples are passed as autoregressive conditioning when generating the next chunk. The discriminator can also see the boundary between the previous and next chunk. To fool the discrminator you need to have a smooth boundary.
