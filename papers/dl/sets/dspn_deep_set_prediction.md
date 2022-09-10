---
title: Deep Set Prediction Networks.
venue: NeurIPS
pages: 3207-3217
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/nips/ZhangHP19
ee: https://proceedings.neurips.cc/paper/2019/hash/6e79ed05baec2754e25b4eac73a332d2-Abstract.html
url: https://dblp.org/rec/conf/nips/ZhangHP19
authors: ["Yan Zhang", "Jonathon S. Hare", "Adam Pr\u00fcgel-Bennett"]
sync_version: 3
cite_key: conf/nips/ZhangHP19
---
# Deep Set Prediction

https://github.com/Cyanogenoid/dspn/blob/master/dspn.py

Basic idea: We should be able to encode a set into a latent, then decode it from the same latent
in any order.

General idea: Can we make the output set assignments permutation equivariant and invariant?

Set Loss function: Hungarian loss: Match targets to prediction result based on loss minimizer.

Representation loss: Need to ensure that the latent representation is permutation invariant. To
ensure this, use gradient descent to reconstruct the input from the latent.

First encode the input.

Then fit $\hat Y$ by gradient descent - eg, take the encoder and optimize $\hat Y$
so that it encodes to the same $z$.

Target set should have low representation loss with itself.

When we train the set-to-set task, seems that we generate a random permutation every time.