# DynaBERT: Dynamic BERT with Adaptive Width and Depth

Motivation: BERT is good, but requires a lot of parameters

Usually people train different BERT models to deal with different resource constraints.

Most methods compress a model to a fixed size. Only depth-adaptive by varying the number of transformer layers.

 - LayerDrop
 - FastBERT
 - DeeBERT

In this work, we get flexibility in width and depth. Better exploitation between accuracy and model size. Once trained, don't need fine-tuning for sub-networks.

## Determining the width

 - Multi-head attention layers + FFNN
 - N_H attention heads are concatenated
 - Rewrite multi-head attention so that they are computed in parallel. Instead of concatenating the heads and then waiting for each head to be complete before passing through a linear layer, pass each head through a linear layer and then sum the result.
 - FFNN: Sum the result of several small linear-layer computations instead of multiplying the GeLU activation by one big linear layer.


note that this makes the heads permutation invariant.

## Network rewiring
Then we can adjust the width of the width of the network.

For a width multiplier, retain the leftmost attention heads in the MHA and retain the leftmost leftmost neurons in the FFNN.

Rewrite the connections accordance to the importance - neuron's importance is the derivative of that neuron with respect to the loss if that neuron was removed.

Before training, arrange the network heads with respect to importance.

The teacher assistant helps, according to the ablation study

## Knowledge Distillation

 - Distillation over logits: $l_{\text{pred}}(y^{(m_w)}, y) = SCE(y^{(m_w)}, y)$
 - Distillation over work embedding: $l_{\text{emb}}(E^{(m_w), E) = MSE(E^{(m_w)}, E)$
 - Distillation over hidden states: $l_{\text{hidden}}(H^{(m_w), H) = \sum^L_l MSE(H_l^{(m_w)}, H_l)$

To convert BERT into DynaBERT, reformulate the loss in terms of these knowledge distillation terms.

After the width-adaptive BERT is trained, use it as a "Teacher network" for a given width setting (chosen by network rewiring). Then do knowledge distillation using the distillation loss to train a network of a different depth. Requires training data.

## Qualitative Study

As we adjust the width and height of the network, the attention maps also start to fuse.



