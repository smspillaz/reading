# Deep Set Prediction

https://github.com/Cyanogenoid/dspn/blob/master/dspn.py

Basic idea: We should be able to encode a set into a latent, then decode it from the same latent
in any order.

General idea: Can we make the output set assignments permutation equivariant and invariant?

Set Loss function: Hungarian loss: Match targets to prediction result based on loss minimizer.

Representation loss: Need to ensure that the latent representation is permutation invariant. To
ensure this, use gradient descent to reconstruct the input from the latent.

First encode the input.

Then fit \hat Y by gradient descent - eg, take the encoder and optimize \hat Y
so that it encodes to the same z.

Target set should have low representation loss with itself.

When we train the set-to-set task, seems that we generate a random permutation every time.
