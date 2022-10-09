---
title: "Contrastive Learning of Structured World Models."
venue: "ICLR"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/KipfPW20"
ee: "https://openreview.net/forum?id=H1gax6VtDB"
url: "https://dblp.org/rec/conf/iclr/KipfPW20"
authors: ["Thomas N. Kipf", "Elise van der Pol", "Max Welling"]
sync_version: 3
cite_key: "conf/iclr/KipfPW20"
---
# Contrastive Structured World Models (C-SWMs)

[[contrastive_structured_world_models.pdf]]

tl;dr:
 - Learn a structured world mode of objects, relations and interactions
 - Encode scene using CNN, each channel is an independent object.
 - Each channel summarized as a vector, vectors interact with each other by message passing in a fully connected network
 - Predict next latent state dynamics
 - Contrastive loss between next predicted state and corrupted st ate.


## Contrastive Objective

$$
\mathcal{L} = d(z+t + T(z_t, a_t), z_{t + 1}) + \max(0, \gamma -d(\tilde z_t, z_{t + 1}))
$$

where $\tilde z_t$ is a corrupted negative example

## Model

![[c-swm_model.png]]

 - Encode scene using CNN, each channel is an independent object.
 - Each channel summarized as a vector, vectors interact with each other by message passing in a fully connected network
	 - Learn $f_{\text{edge}}$ and $f_{\text{node}}$
	 - Complexity: $O(K^2)$
 - Predicted transitions from transition model: $\triangle z_t$ - we only predict the delta, adding $\delta z_t$ to the predicted object latent.
 - Possible to have many feature maps per latent


## Experiments

50x50x3 gridworld.

Discovers object prediction masks from environment and learns abstract state transition graph.

![[c-swm_learned_abstract_state_transition_graph.png]]

The nodes are "state embeddings obtained from a test set experience buffer with random actions" and the edges are "predicted transitions ($\delta t$)". Basically, we learn that in the latent space, while the green object moves around, this has no effect on the blue, purple and yellow objects, which stay in the same place in latent space.

Without contrastive loss, the structure of this latent space is pretty bad, see below:

![[c-swm_without_contrastive_loss.png]]