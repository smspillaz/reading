---
title: Alias-Free Generative Adversarial Networks.
venue: CoRR
volume: abs/2106.12423
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2106-12423
ee: https://arxiv.org/abs/2106.12423
url: https://dblp.org/rec/journals/corr/abs-2106-12423
authors: ["Tero Karras", "Miika Aittala", "Samuli Laine", "Erik H\u00e4rk\u00f6nen", "Janne Hellsten", "Jaakko Lehtinen", "Timo Aila"]
sync_version: 3
cite_key: journals/corr/abs-2106-12423/Karras/2021
---

# StyleGAN3: Alias Free Generative Adversarial Networks


GANs seem to depend on absolute pixel coordinates in an unhealthy manner.

The problem is "bad signal processing" which causes aliasing in the generator.

Typical GAN generators are analagous to hierarchical processing - you do the big stuff first, then refine it into the msaller stuff. But it doesn't really follow the natural hierarhcy. The coarse features include the prescence of finer features but not really their precise positions.

What does this actually look like in practice?

![[stylegan3_texture_sticking_problem.png]]

You would expect that when averaging together bits of the latent space which are nearby that you'd get a blurry image. But you don't get one - what happens is that the features actually stay the same and "stick" to coordinates in the image.

How is it that this "sticking" happens? Aren't convnets supposed to be convolutional? Wlel:

 - Image borders
 - Per-pixel noise inputs
 - Positional encodings
 - Aliasing

Aliasing in particular has two sources:
 - Nonideal upsampling filers like nearest, bilinear or strided convolutions
 - Pointwise application of nonlinearities like ReLU or swish.


## Equivariance via continuous signal interpretation

Lets go back to the Nyquist-Shannon theorem. Any samples signal can represent any continus signal containing frequencies between zero and half of the sampling rate. So the maximum frequency that you can sample is 2r.

Conversion from the continuous to the discrete domain corresonds to sampling the continuous signal at sampling points  of $Z[x]$ (the feature map which are at half the sample spacing).

Remember that multiplication in the frequency domain is the same as convolution in the spatial domain.

Convolution itself doesn't introduce new frequencies.

Upsampling/downsampling : Increases the output sampling rate to ad headroom to the spectrum where additional layers my introduce more content. When downsampling, we have to apply a low-pass filer first above the output bandlimit so that the signal is represented faithfully in the coarser discretization.

Nonlinearity: ReLU in the continuous domain could introduce arbitrarily high frequencies. The solution is to do the nonlinearity, then apply a low-pass filter.

## How to apply these insights to the generator

Original StyleGAN2: mapping network which transforms from an initial normally distributed latent to an intermediate latent code $w \sim W$. Then a synthesis network which starts from $4 \times 4 \times 512$ constant $z_0$ and applies a sequence of $N$ layers, each consisting of convolutions, nonlinearities, upsampling, per-pixel noise.

Tyr to make every layer of teh generator equivariant with respect to the continuous signal.

### Fourier features

To facilitate continuous translation and rotation of the input, replace the learned input constant with fourier features.

### Per-pixel noise

Remove these since they're at odds with a natural transformation hierarchy.

### Mapping network depth / regularization

Decrease the depth and disable mixing regularization and path length regularization. Address the issue by using a normalization before convolution. Track the EMO similar to batchnorm.

### The redesign

1. Boundaries: Replace bilinear 2x upsampling with a better approximation of the ideal low-pass filter. Large Kaiser window at n = 6, so each output pixel affected by 6 input pixels in upsampling
2. Filtered nonlinearities: Upsample and downsample by factor $m$ between each nonlinearity. This should account for new frequencies being introduced. In the generator you upsample more than you downsample, but the point is that between each nonlinearity, you always upsample.
3. Non-critical sampling: Lower the cutoff frequency to $s/2 - f_h$, which ensures that all alias frequencies are in the stopband.
4. Fourier features
5. Rotation equivariance: Replace all 3x3 convolutions with 1x1 on all layers and compensate for the reduced capacity by doubling the number of feature maps. Only upsampling and downsampling operations spread information between pixels.
6. Stabilization trick: Early on we blur the images the discriminator sees using a Gaussian filter. Prevents the discriminator from looking at the high frequencies earlier on.