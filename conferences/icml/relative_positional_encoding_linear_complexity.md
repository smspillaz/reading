# Relative Position Encodings

![[liutkus_relative_pos_encoding_linear_complex.pdf]]

For each output, tell you which input you use to compute the output. If an entry is close to zero, the input should be ignored.

We apply some tokenwise linear transformation (values). Then compute the output sequence by averaging the values weighted by the attention coefficients.

To compute the attention matrix, compute output features (query) from each token, input features from each token (keys).

Then take $A = QK^T$, exponentiation to produce sparsity.

Then in reality, you have several heads, normalization, skip connections.

Note that attention matrix is linear complexity, sometimes this does not fit into memory, especially if you have many layers.

## Linear Transformers

Leveral RKHS, $A = \mathbb{E}_{\phi} [\phi(Q)\phi(K)^T]$ - apply some functions to the queries and keys.

Note that you don't have to compute $A$ anymore. You replace the attention matrix by its approximation. When you do this you get to a linear complexity because you never have to store or compute the very big attention matrix.

## Stochastic Positional Encoding

With the basic scheme positions are not taken into account. Random permutation of tokens would lead to the same result. Taking positions into account is desirable.

Idea: make positions of tokens part of their features.

Classical way to do it, add some information to the initial input. For each token add vector of sines and cosines of positions.

### Relative positional encoding

Add the encoding directly to the attention matrix. Put more emphasis depending on time lags. If you know that you should pay more attention to the outputs nearby, then you will add this information to the attention matrix directly.

$$A = \exp{QK^T + \Omega(m - n)} Y = AV$$

But to use it, you must explicitly compute the attention matrix.

You can also do $QPK^T$

### Our model - Stochastic Positional Encoding (SPE)

We want to do a linear transformer with relative positional encoding. So no touchign the attention matrix.

We must transform our attention matrix. We must create modified queries and keys that lead to this attention matrix.

Stochastic Positional Embedding. Any PD-toeplitz matrix is the autocovariance of a regularly sampled wide-sense stationary process.

We just $R$ independent samples from a stationary process that has a prescribed autocorrelation structure - we know that if $R$ is big enough, then its autocovariance will be toeplitz. We don't really care about positional encoding, but we want to get the right attention information.

This means that we can take random stationary positional encoding and express this as a product of two sums and the cross-terms disappear beacuse they are orthogonal. Therefore we get bakc to our initial dot-product attention. When we are there we can use linear transformers.

Note from experiments: If you just use absolute positional encoding, performance will degrade significantly for sequence lengths longer than those in the training data.


