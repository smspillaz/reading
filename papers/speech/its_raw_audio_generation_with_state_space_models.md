---
title: It&apos;s Raw! Audio Generation with State-Space Models.
venue: ICML
pages: 7616-7633
year: 2022
type: Conference and Workshop Papers
access: open
key: conf/icml/GoelGDR22
ee: https://proceedings.mlr.press/v162/goel22a.html
url: https://dblp.org/rec/conf/icml/GoelGDR22
authors: ["Karan Goel", "Albert Gu", "Chris Donahue", "Christopher R\u00e9"]
sync_version: 3
cite_key: conf/icml/GoelGDR22
---
SaShiMi - a new multi-scale architecture for waveform modeling built around the recently introduced S4 model for long-sequence modeling.

Things you're looking for with audio:
 - Global coherence
 - Computational efficiency
 - Sample efficiency

We have things like WaveNet and RNN but scaling them to really long sequences in a way that maintains global coherence is hard.

Technical contributions with this approach:
 - Improve S4's parameterization to improve stability during training
 - Pooling layers between blocks of residual S4 layers to capture hierarchical information
 - Bidirectional relaxation to flexibly incorporate S4 into non-AR architectures.

## State Space Models

The state space model is defined in continuous time as follows:

$$
h'(t) = Ah(t) + Bx(t)
$$
$$
y(t) = Ch(t) + Dx(t)
$$

To operate in discrete time, just discretize the step size. You need to make a discretized state matrix and make $h$ and $x$ no longer functions of time:

$$
h_k = \bar Ah_{k - 1} + \bar B x_k
$$
$$
y_k = Ch_k + Dx_k
$$
$$
\bar A = (I - \triangle / 2 \cdot A)^{-1}(I + \triangle/2 \cdot A)
$$

One important property of an SSM is that the recurrence is equivalent to a convolution by a kernel $\bar K$

$$
\bar K = (C \bar B, C \bar{AB}, C \bar{A^2B}, ...)
$$

$$
y = \bar K * x
$$

S4 is a particular instantiation of an SSM that parameterizes $A$ As as diagonal-plus low rank martrix, $A = \Gamma + pq^*$

Uses a special matrix called a HiPPO matrix.

To stabilize S4 for recurrence, use the parameterization $\Gamma - pp^*$ instead of $\Gamma - pq^*$, eg, typing the parameters $p$ and $q$.

$-pp^*$ is a negative semidefinite matrix, so we know the signs of its spectrum. Every eigenvalue has a negative real part. This is also known as a "Hurwitz Matrix".

These are also called "stable matrices". If unrollign the RNN involves raising $\bar {A}$ to some power repeatedly, then this is stable if and only if all the eigenvalues lie inside or on the unit disc.

## Architecture

Consists of multiple tiers, with each tier being composes of a stack of residual S4 blocks. Lower tiers downsample the waveform and process that. Output of the lower tiers is upsampled and combined with the input of the tier above it to provide a stronger conditioning signal.

## Results

Works more effectively than baseline AR methods in leveraging longer contexts.