# On Disentangled Representations Learned from Correlated Data

The focus of disentanglement approaches has been on identifying independent factors of variation in data. However, the causal variables underlying real-world observations are often not statistically independent. In this work, we bridge the gap to real-world scenarios by analyzing the behavior of the most prominent disentanglement approaches on correlated data in a large-scale empirical study (including 4260 models). *We show and quantify that systematically induced correlations in the dataset are being learned and reflected in the latent representations, which has implications for downstream applications of disentanglement such as fairness.* We also demonstrate how to resolve these latent correlations, either using weak supervision during training or by post-hoc correcting a pre-trained model with a small number of labels.

https://icml.cc/virtual/2021/oral/9352

[[trauble_on_disentangled_representations_learned_from_correlated_data.pdf]]

## Problem

We train under far too idealistic data settings.

Experimental training setups are very idealistic:
 - Generative model: $x \sim \int_c p^* (x|c) p^* (c) dc$
 - Every combination of underlying factors is there in the training data.


See [[the_role_of_disentanglement_in_generalisation.pdf]].

This assumptions is unlikely to hold in practice. Realistic unlabelled datasets are likely to be correlated.

Humans can still conceive of both factors independently. Correlation can come from a causal relationship or from unobserved circumstances or confounders.

Why does this cause a problem, consider two factors, $c_1$ and $c_2$ that are correlated.

In a perfectly disentangled representation, latent factor 1 would model $c_1$ and $c_2$ - it should put probability mass outside the training distribution which would then violate the constraint imposed by the loss function.

Methods that optimize the lower bound of the log-likelihood would have a bias against disentanglement.

Why do we still want the disentanglement anyway:
1. Increased intepretability - meaningful and compact representations
2. They should generalize better and remain robust under distribution shifts
3. We want to sample out of distribution examples and intervene on individual factors individually.
4. Fairness


## Unsupervised Disentanglement under correlated factors

Large scale empirical investigation if SoTA can learn disentangled models from correlated data.

### Dataset

Introduce correlated dataset variants of Shapes3D, dSprites, MPI3D (between a single pair of factors - linear correlation with Gaussian noise). This single correlation already captures problems introduced by known correlations. Can tune the amount of correlation.

Other factors uncorrelated.

### Study

Train disentanglement models with multiple hyperparameters:
 - Beta-VAE
 - Factor-VAE
 - Annealed-VAE
 - Dip-VAE
 - Beta-TC-VAE

For strong correlations, trained models have two latent codes encoding the two latent variables simultaneously.

Pairwise entanglement score - how difficult is it to separate two factors of variation across their latent codes. Pair of correlated factors has a substantially higher score than the median of all other pairs and for weaker correlations the pair becomes easier to disentangle. Models can still disentangle weakly correlated factors.

## Robustness and Generalization Capabilities of these models

What happens if you sample from OOD?

Eg, large object size, small azimuth.

We analyze examples that haven't been sampled during training. The model can nevertheless reconstruct these samples - so the samples are meaningfully encoded and the decoder is capable of generating observations (cf [[the_role_of_disentanglement_in_generalisation.pdf]]).

Look at the projection of the latent space - contours of equal colour in the ground truth are not aligned in the latent space.

 - If we imagine the contour line of equal color in both plots over training data
	 - Latent encodings of happen to meaningfully extend and complete this structure of the latent space



## Can we resolve latent entanglement post-hoc 

If some labels are accessible, one approach is fast adaptation.

![[correlated_disentanglement_resolving_post_hoc.png]]

To identify the entangled dismensions - look at the maximum feature importance inferred from GB Trees. Train a substitution function to predict ground truth labels from entangled dismensions using the same M labels. This is equivalent to rotating in the space.

Entanglement drops substantially with "as few as 100 labels".

Can you mitigate these troublesome latent entanglements using weak supervision?
 
  - Assume access to pairs that share a fixed number of actors without knowing which (weak labels) and optimize the following
	  - $E_{(x_1, x_2)} [E_{q} \log (p(x_i|z)) - \beta D_{KL(q(\hat z|x_1, x_2)||p(\hat z))}]$


Works for datasets with perfectly independent factors - does it also work for correlated data (Ada-GVAE algorithm).

 - Models can resolve strong pairwise correlation in the trianing samples without latent entanglements.
 - We construct training apirs that satisfy the assumptions of the weak labels from the correlated training data.
 - Models can generate OOD samples

Question: What about extremely correlated data? Authors only tested $\sigma = 0.2$ as the most extreme correlation case?