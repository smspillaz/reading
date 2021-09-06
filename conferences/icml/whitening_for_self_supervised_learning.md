# Whitening for Self-Supervised Learning

Most of the current self-supervised representation learning (SSL) methods are based on the contrastive loss and the instance-discrimination task, where augmented versions of the same image instance ("positives") are contrasted with instances extracted from other images ("negatives"). For the learning to be effective, many negatives should be compared with a positive pair, which is computationally demanding. In this paper, we propose a different direction and a new loss function for SSL, which is based on the whitening of the latent-space features. The whitening operation has a "scattering" effect on the batch samples, avoiding degenerate solutions where all the sample representations collapse to a single point. Our solution does not require asymmetric networks and it is conceptually simple. Moreover, since negatives are not needed, we can extract multiple positive pairs from the same image instance. The source code of the method and of all the experiments is available at: https://github.com/htdt/self-supervised.

https://icml.cc/virtual/2021/spotlight/10242

[[ermolov_whitening_ssl.pdf]]

## Contributions

1. Whitening-MSE loss function (constraints batch samples to lie on a spherical distribution and is an alternative to positive-negative instance contrasting methods)
2. Demonstration that multiple positive pairs extracted from one image improves performance
3. W-MSE outperforms commonly adopted contrastive loss


## Whitening MSE Loss

$$
\min_{\theta E[\text{dist}(z_i, z_j)]}
$$

such that $\text{cov}(z_i, z_j) = I$

So $L_{\text{W-MSE}}(V) = \frac{2}{Nd(d - 1)} \sum \text{dist} (z_i, z_j)$

where $z = \text{ZCA}(v)$

Reminder that whitening means that we first CENTER and STANDARDIZE the data, then compute the sample covariance matrix $\Sigma$, then take the eigendecomposition $PDP^{-1} = \Sigma$.

The whitening transform is $Px \times \text{diag}(\lambda)^{-\frac{1}{2}}$. $P$ rotates you into the orthogonal space, squashing the eigenvalues causes all the smaller frequencies to become noise.

We don't want the data to be from a dengenerate distribution.

![[whitening_optimization_process.png]]

1. Initially its clustered
2. After whitening it is centered and scattered
3. After normalization it is projected on the hypersphere
4. We minimize the distance between positive samples and preserve the scattering
5. At the end the clusteres are scattered around and they do not collapse into a single point


Training procedure - obtain common samples, apply whitening, normalize it, then minimize the MSE.

## Comparison with the SOTA

Outperforms contrastive loss and is on par with current SOTA.