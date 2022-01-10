# What kind of generalization do we expect to happen?

 - GAN only sees two objects - we expect generalization to 2 objects only
	 - Reality: log-normal distribution: you get 1, 2, 3 and 4 objects, with 2 being the model
 - What if the data is bimodal
	 - Two log-normal distributions
 - What if the modes are close
	 - Additive behaviour - can result in nontrivial generalization


![[gan_generalization_modes.png]]


Combinatorial Explosion: many different combinations can happen, inductive bias needs to indicate which ones are valid.


In continuous spaces, unbiased density estimation is impossible.

Data Augmentation for GAN - biases the model towards generalization in the direction that we want. But this might generalize in undesirable ways. Eg flying penguins.

Negative data augmentation: Discriminator which provides examples of images that should not be generated.

![[gan_negative_data_augmentation.png]]

Many kinds of negative data augmentation: Jigsaw transformation, permute patches, wrong global structure.

![[nda_data_agumentation_gan_jigsaw.png]]

Dataset bias:

 - How can we leverage the biased dataset?
 - We might not even know - no labels to characterize the dataset bias.

Idea: If you have some labels about the bias in your minibatch characteristics, then you can prevent the model from generating minibatches that have the same statistical properties that you want to avoid (eg, 3 women, 1 man).


The perfect bayes-optimal classifier can be used to re-weight the samples and figure out how representative they are with respect to the target unbiased dataset.

Upweight or downweight the samples - importance sampling weights that come from a classifier.

 - Re-weighting to distinguish between a source dataset and a target dataset.
 - Train a classifier such that $\frac{P(y = 1|x)}{P(y = 0|x)} = w(x)$

Correct for important attributes, eg, CelebA, control for the gender imbalance.

Use negative data as a source of fake data.