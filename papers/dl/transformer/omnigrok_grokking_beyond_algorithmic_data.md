---
title: Omnigrok: Grokking Beyond Algorithmic Data
---

Grokking remains elusive. Where does it come from? This paper identifies the mismatch between training and test loss landscapes as the cause for grokking.

"LU" mechanism. Train loss vs weight norm looks like L. Test loss vs weight norm looks like U.

Grokking can be induced on tasks involving images, language and molecules.

![[omnigrok_loss_landscape.png]]

Generalizing solutions are concentrated in weight space in an area where the weight norm is some $w_c$. Training loss and test loss have shape of L and U.

You can define some function of minimizing training loss over angular directions, eg, $\tilde f(w) = f(w^*(||w||))$ where $w^*(||w||) = \arg \min_{||w||_2} l_{\text{train}}(w)$

Basically, minimize by rescaling the model weights back to their original norm after each unconstrainted optimization step. This loss landscape is easier to visualize (its just a radial vector) and captures important features about grokking.

OK, so what are the findings:

 - Grokking Dynamics: If the weight norm is initialized to be large, then you move to an overfitting solution by minimizing the training loss. Without regularization you just stay where you are. However when weight decay is on, then radial motion can be slow, but you slowly move towards the "goldilocks zone".


## Teacher-student experiment

Teacher and the student are both a 5-100-100-5 MLP but are initialized to different seeds. Student has normalized weights. Teacher network does not have normalized weights. The point of the teacher network is to generate labels for the student network.

So, what happens. When we don't have regularization, then as training loss decreases, test loss goes up. That's normal. But if we do have weight decay, we learn a little bit slower but we get generalization.


## Omnigrok: Grokking for more interesting tasks

Loss landscape of MNIST. Larger initializations lead to grokking (slow generalization). Large datasets de-grok (eg, you get faster generalization). 

The plots are of training loss/test loss decrease as a function of dataset size N and relative weight norm $w / w_0$.
