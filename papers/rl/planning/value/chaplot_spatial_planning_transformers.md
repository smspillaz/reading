---
title: Differentiable Spatial Planning using Transformers.
venue: ICML
pages: 1484-1495
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/icml/ChaplotPM21
ee: http://proceedings.mlr.press/v139/chaplot21a.html
url: https://dblp.org/rec/conf/icml/ChaplotPM21
authors: ["Devendra Singh Chaplot", "Deepak Pathak", "Jitendra Malik"]
sync_version: 3
cite_key: conf/icml/ChaplotPM21
---

# Differentiable Spatial Planning using Transformers

Find the shortest path to a goal given an obstacle map. There is some regularity and distances between objects in the map.

Why do we need machine learning?
 - Exploit statistical regularities - classical methods optimize a plan from scratch. Learned planner can capture the regularities and be efficient at inference time.
 - Tackle unknown maps - you can deal with not having a map.


Prior solutions use VIN, GPPN (Convolutional LSTM).


In this solution, we can do long distance value propagation without multiple iterations.

Two settings:
 - Known Maps
 - Unknown maps.

Known maps: we predict the number of actions required to reach the goal (eg, action distance).

## Spatial Planning Transformer

![[spatial_planning_transformer.png]]

 - Embed each element using a 2-layer conv
 - Flatten embeddings and pass them through a transformer module
 - Add position encodings to each embedding
 - 5 layer transformer
 - decode each output token to get the predicted distance from the starting location .

Train using synthetic data - predict action distances from input maps and goals.

## Transfer to unkown maps

Then we can transfer to using unknown maps.

 - We have some observation space $o$ and a mapping function $f_M$ which predicts the map. Then use spatial planning on the predicted map to come up with predicted action distances.
 - Model weights for the SPT model are frozen.

Since the planning module is pre-trained and expects a structured map input. Training set: 100K.

## Supervision types

 ![[spt_supervision_types.png]]

 You can have dense and perfect supervsion, noisy supervision, also sparse supevision which consists of just a few paths to the goal and their associated distances.

 Map accuracy on sparse supervision is lower, but planning accuracy is just as good.

## Experiments

 - VIN
 - GPPN

Datasets, in-distribution (0-5 obstacles)

Proposed SPT model outperforms both baselines.
Outperforms baseline for out-of-distribution maps.

For unknown maps - SPT can predict the map accurately