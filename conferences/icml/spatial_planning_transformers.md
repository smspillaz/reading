# Differentiable Spatial Planning using Transformers

We consider the problem of spatial path planning. In contrast to the classical solutions which optimize a new plan from scratch and assume access to the full map with ground truth obstacle locations, we learn a planner from the data in a differentiable manner that allows us to leverage statistical regularities from past data. We propose Spatial Planning Transformers (SPT), which given an obstacle map learns to generate actions by planning over long-range spatial dependencies, unlike prior data-driven planners that propagate information locally via convolutional structure in an iterative manner. In the setting where the ground truth map is not known to the agent, we leverage pre-trained SPTs in an end-to-end framework that has the structure of mapper and planner built into it which allows seamless generalization to out-of-distribution maps and goals. SPTs outperform prior state-of-the-art differentiable planners across all the setups for both manipulation and navigation tasks, leading to an absolute improvement of 7-19%.

[[chaplot_spatial_planning_transformers.pdf]]

https://icml.cc/virtual/2021/spotlight/9102

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



