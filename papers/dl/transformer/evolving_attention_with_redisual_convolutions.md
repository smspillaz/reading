---
title: "Evolving Attention with Residual Connections"
---


Combine attention maps with CNN, plus a linear interpolation

The main contribution is having these CNN layers between the attention maps.

For the decoder you need to be a bit careful, since you don't want to "foresee subsequence positions".

 - For encoder self-attention the convoluton can look at everything
 - For decoder self-attention the convolution cannot "see the future"
 - For encoder-decoder attention the convolution cannot "look from the future to the past".