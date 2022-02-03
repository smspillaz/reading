# Self-supervised learning

**Self-prediction**: Given an individaul data sample, the task is to predit one part of the same given the other part - intra-sample prediciton. Masking words/patches.

**Contrastive learning**: Predict relationships between multiple samples. Which samples are similar to each other and which are not. We know the true relationship between samples but pretend to not know it. Eg, words within the same corpus, multiple camera views, augmented versions share representations.

## Self-prediction

 - Predict future from the past
 - Predict future from the recent past
 - Predict past from the present
 - Predict top from the bottom
 - Predict occluded from visible


1. Autoregressive generation
2. Masked generation
3. Innate relationship prediction
4. Hybrid self-prediction


### Autoregressive

 - WaveNet, WaveRNN
 - Autoregressive language modelling
 - Images in a raster scan (PixelCNN, PixelRNN, iGPT)

### Masked Generation

 - Masked Language Modelling
 - Patch prediction


### Innate Relationship Prediction

 - Shuffle patches, predict the order
 - Rotate the image, predict which direction the rotation has been applied
 
 
 ### Hybrid Self-Prediction Models
 
  - [[vq_vae|VQ-VAE]]: Learn a discrete codebook. Together with transformer to autoregressively model.
  - VQ-GAN


## Contrastive Learning

 - Similar pairs stay close, dissimilar ones move apart
 
 
 1. Inter-sample classification
 2. Feature clustering
 3. Multiview coding


Inter-sample classification is the most dominant approach.

Give both similiar and dissimilar candidates - determine which is similar to the anchor data point. 

Take the original input as anchor and apply a set of transformation as distorted versions - the distorted versions are positives.

### Multiview coding

Data that captures the same target from different views

### Loss function

We can use cross-entropy loss.

A few variations:

 - Contrastive loss
	 - minimize distance between $x_i$ and $x_j$ if they share th same class $1_{y_i = y_j} ||f(x_i) - f(x_j)||_2  + 1_{y_i \ne y_j} \max (0, \epsilon - ||f(x_i) - f(x_j)||_2$
 - Triplet loss
	 - Demands an input triplet containing one anchor, one positive and one negative
	 - Compute distance to anchor for both positive and negative example
	 - Try to ensure that distance to anchor is shorter for the positive example.
 - N-pair loss
	 - Generalizes the triplet loss to include comparison with multiple negative samples
	 - $- \log \frac{e^{f(x)^T f(x^+)}}{e^{f(x)^T f(x^+)} + \sum e^{f(x) + f(x_i^-)}}$
 - Lifted structured loss: Utilizes all pairwise edges wihtin one training batch for better computational efficiency
	 - Construct multiple similar or dissimilar pairs
	 - Utilize all the pairwise edges within one training batch.
 - NCE
	 - Given target sample distribution $p$ and noise distribution $q$
	 - $L = -\frac{1}{N} [\log \sigma(l_{\theta} (x_i) + \log(1 - \sigma (l_{\theta}(x_i))))]$
 - InfoNCE
	 - Use categorical cross-entropy to identify the positive sample among a set of unrelated noise samples.
 - Soft-nearest neighbors loss:
	 - Include multiple positive samples given known labels
	 - Basically, log-ratio of energy of positive examples by energy of all examples


### Feature clustering

Find similar data samples by clustering them with the learned features. Use clustering algorithms to assign pseudo-labels, st we can run intra-sample contrastive learning.

DeepCluster, InterCLR.

### Contrastive Learning between modalities

 - Image/Test: CLIP
 - CodeSearchNet: Text and code



