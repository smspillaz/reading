---
title: "High-Resolution Image Synthesis with Latent Diffusion Models."
venue: "CoRR"
volume: "abs/2112.10752"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2112-10752"
ee: "https://arxiv.org/abs/2112.10752"
url: "https://dblp.org/rec/journals/corr/abs-2112-10752"
authors: ["Robin Rombach", "Andreas Blattmann", "Dominik Lorenz", "Patrick Esser", "Bj\u00f6rn Ommer"]
sync_version: 3
cite_key: "journals/corr/abs-2112-10752/Rombach/2021"
---

Main idea: Do the diffusion in the latent space as opposed to the image space.

We want to find a perceptually equivalent but computationally more suitable space.

Only need to train the universal autoencoding stage once and then reuse it for multiple DM trainings.

Contributions:
 - Scales to higher dimensional data and can work on a compression level
 - competitive performance on multiple tasks
 - no delicate reweighting of reconstruction and generative loss required

## Perceptual Image Compression

Autoencoder with perceptual loss and patch-based adversarial objective.

The main point here is that we get some compression but really good reconstructions.

## Latent Diffusion

Encode the image and do the diffusion in the latent space.

## How to do conditional diffusion

Cross-attention layer, where the query is is flattened intermediate representation of the UNet, the keys come from the conditioning encoder and the values come from the conditioning encoder.

Then your conditional latent diffisuion model just denoises with that conditioning.

# Experiments

Latent Diffusion models trained in VQ-regularized latent spaces sometimes get better quality.

### Downsampling Factors

LDMs with different downsampling factors, eg, how does your reconstruction performance go with different levels of compression.

Small downsampling factors result in slow training progress. Large downsampling factors cause stagnating fidelity.

### Image Generation

Evaluate:
 - Sample quality
 - Coverage of data manifold (using FID scores and precision-and-recall)???

LDM-4 seems to do pretty well on CelebA, beating out FID scores there.

On FFHQ doesn't beat the FID scores but does a bit better on the data manifold.

Would be nice if they could compare precision and recall for the other methods. One can dream I guess.

On text-conditional image synthesis, they're not quite competitive with GLIDE, but their model is on par with most recent diffusion and autoregressive methods.

But in any event it does better than GANs. I think GANs are dead now.

## Conditional Latent Diffusion

So they train a KL-regularized LDM conditioned on language prompts from LAION-400M.

They also do image synthesis based on semantic layouts. Semantic synthesis is basically where you paint the class-conditional segmentation map and then ask the model to fill in the details. Sort of like reverse image segmentation.

### Inpainting

You can improve performance by at least 2.7x on pixel and latent based diffusion methods.
