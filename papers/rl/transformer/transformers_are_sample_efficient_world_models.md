---
title: "Transformers are Sample Efficient World Models."
venue: "CoRR"
volume: "abs/2209.00588"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2209-00588"
doi: "10.48550/ARXIV.2209.00588"
ee: "https://doi.org/10.48550/arXiv.2209.00588"
url: "https://dblp.org/rec/journals/corr/abs-2209-00588"
authors: ["Vincent Micheli", "Eloi Alonso", "Fran\u00e7ois Fleuret"]
sync_version: 3
cite_key: "journals/corr/abs-2209-00588/Micheli/2022"
---

The world model needs to be accurrate over extended periods of time, and this is a challenge if we want to learn inside the model. The method outperforms MuZero and is called IRIS.

The basic idea is this:
 - Discrete-encode the initial state into some tokens from some vocabulary (discrete autoencoder).
 - Decode tokens into a state using the same autoencoder.
 - Policy network predicts the action.
 - Transformer takes the discrete tokens + action and predicts the reward, termination state and then next discrete tokens for the next frame.

Use cross-entropy loss for the transition predictor. That means that the transformer has to predict *logits* for the next frame corresponding to what the discrete autoencoder would encode the world as.

Limitations: IRIS works well when you don't have distributional shifts in the training data as training progresses. But if you have some unseen event, eg, opening a box to get a key, your world model won't really understand that and will need to learn to reconstruct it first.

Increasing the number of tokens increases representation power.