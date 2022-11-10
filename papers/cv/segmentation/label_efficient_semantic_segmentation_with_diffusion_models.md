---
title: "Label-Efficient Semantic Segmentation with Diffusion Models."
venue: "ICLR"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/BaranchukVRKB22"
ee: "https://openreview.net/forum?id=SlxSY2UZQT"
url: "https://dblp.org/rec/conf/iclr/BaranchukVRKB22"
authors: ["Dmitry Baranchuk", "Andrey Voynov", "Ivan Rubachev", "Valentin Khrulkov", "Artem Babenko"]
sync_version: 3
cite_key: "conf/iclr/BaranchukVRKB22"
---

Question: Can DDPM serve as a representation learner?

Investigate the intermediate activations from a U-Net that approximates the step of reverse diffusion in DDPM.

Contributions:
 - What representations are learned by DDPM
 - Design a simple segmentation approach exploiting these representations
 - Compare DDPM to GAN based counterparts.

To extract representations: Corrupt $x_0$ with noise and pass that to the UNet. Then take the intermediate activations and upsample them to HxW with bilinear interpolation.

Then take the representation and train some MLP to predict. Training only happens on a small support set.

Representations at later steps are generally better.

Comparisons:
 - MAE
 - SwAV
 - GAN Inversion
 - GAN Encoder
 - VDVAE
 - ALAE

Some nice features:
 - DDPM has very good sample efficiency. You can outperform this few-shot learning compared to other methods.
