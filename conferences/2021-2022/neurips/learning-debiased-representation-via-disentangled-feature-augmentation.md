# Learning Debiased Representation via Disentangled Feature Augmentation

Models learns shortcuts for classification.

Bias/aligned vs bias-conflicting samples 

The number of bias-conflicting samples is too small.

Diversity in data samples important for debiasing.

Diversity ratio: Diversity of bias-conflicting samples in the training set.

Sampling ratio: The ratio of bias conflicting samples in each batch-size.

With emphasized training of the bias-conflicting samples, we improve accuracy on the unbiased test set.

When increasing the diversity of bias-conflicting examples we do even better. More diversity of them leads the classifier to learn a more debiased representations.

If we emphasize bias-conflicting samples, we just learn another bias (eg, beard type as opposed to age).

## Solution

Diversity the bias-conflicting samples by augmenting them.

Encourage classifier to learn the intrinsic attribute.

Extract the "bias attribute" which corresponds to the gender type, and intrinsic ones corresponding to the age type. Then combine them with attributes from different images.

Generate this on the feature level as opposed to the image level. So augmentation at the feature level.

## Architecture

 - Two encoders - extract the intrinsic attributes $z_i$ and bias attributes $z_b$
 - Linear classifiers predict the class from $z$, which is the concatenation of $[z_i, z_b]$
 - Determine how the image is aligned towards the bias and use that as a weight.


But we want to *diversify the bias-conflicting samples*

Randomly permute the bias attributes in the mini-batch. Loss-swap.