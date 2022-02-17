---
title: Think before you act - A simple baseline for compositional generalization.
venue: CoRR
volume: abs/2009.13962
year: 2020
type: Informal Publications
access: open
key: journals/corr/abs-2009-13962
ee: https://arxiv.org/abs/2009.13962
url: https://dblp.org/rec/journals/corr/abs-2009-13962
authors: ["Christina Heinze-Deml", "Diane Bouchacourt"]
sync_version: 3
cite_key: journals/corr/abs-2009-13962/Heinze-Deml/2020
---

This paper looks at the gSCAN benchmark on the following splits:

1. Random split (no distributional shift)
2. Yellow Squares: Yellow squares are the target object but the color is never specified (eg, "the square", "the big square", "the small square"). Then at test time it is referred to as "the big yellow square" or the "small yellow square". Therefore you have to generalize with respect to the target's references.
3. Red Squares: Red squares are never the target object, but other squares and other red objects are.
4. Relativity: Size adjectives are relative to other objects in the grid world.


# Approach / Architecture

1. World: Predict the target position based on the last hidden state of the command encoder $h^c_n$ and attention-weighted world encodings.
2. "Both": Predict taget position based on attention-weighted command encodings and attention-weighted world encodings.

In both cases you concatenate the world encodings with the command encoding along the channels use that with a linear classifier that predicts scores for each psoition to be the target position.

Anyway once you have the targets, you use those to "decode" an action sequence using an LSTM.

# Results

## Exact match %
![[think_before_you_act_baseline_exact_match.png]]

The paper then looks at the percentage of cases where you have an "exact match", eg, where the target output sequence was predicted exactly. In this case its imitation learning and you're testing on on a held out offline set.

Yellow Squares: In this case, you see a yellow square and target it in the training set, but don't know exactly what it is. Here there's an improvement 61.18 -> 87.31 .

Red Squares: Here there's an improvement 11.73 -> 81.07

## Error Analysis
![[think_before_you_act_target_prediction_accuracy.png]]
How much does taret prediction accuracy correlate with exact match performance?

So here what is happening is that you look at how well you can predict the target states. Prediction of target states is going to be better than prediction of trajectories.
