---
title: Zero-shot Task Adaptation using Natural Language.
venue: CoRR
volume: abs/2106.02972
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2106-02972
ee: https://arxiv.org/abs/2106.02972
url: https://dblp.org/rec/journals/corr/abs-2106-02972
authors: ["Prasoon Goyal", "Raymond J. Mooney", "Scott Niekum"]
sync_version: 3
cite_key: journals/corr/abs-2106-02972/Goyal/2021
---

Proposes a setting where given a demonstration for a task (source task) plus a description of how the target task is different from the source task, do the target task zero shot.

"Language Aided Reward and Value Adaptation" (LARVA).

Inputs:
 - Source demonstration
 - Linguistic demonstration of how the target difers
 - Output either a reward or value funciton that accruately reflects the target task.

"Our approach is able to complete more than 95% of the target tasks on a when using template-based descriptions and more than 70% when using free-form natural language"

Example of a linguistic description: "In the third step, move the green flat bloc kfrom the bottom left to the top left".

## Architecture

Decompose into two problems:

1. Predicting the goal state of the target task given the source demonstration and the language (Target Goal Predictor)
	1. "This decomposition allows for additional supervision of the taret goal predictor using ground-truth goal state for the target task"
2. Predicting the reward / value of a state given the goal state of the target task (Reward / Value Network)

### Target Goal Predictor

**Demonstration Encoder**: Encode each image in the demonstration to a vector, concatenate and pad to get a single vector

**Language Encoder**: Two layer LSTM

**Target Goal Decdoer**: Concatenate both, deconvolution to obtain an image representation of the target goal state

### Reward / value network

Take predicted goal state $\hat g$ and another state $s$ from the target task and predict the reward or value function evaluation of the state under the target reward function. Cosine similarity is usually a good way to do it.


## Training

We have access to a dataset of source tasks, language adaptation dscriptions and taret tasks.

We have supervision both on the value function and on the target goal.

A datapoint is sampled at random from $D$. When predicting the value function, sample arget states from the target state set, sampling the rewarding state with 50% probability.

### Tuning Procedure

"We train the models using the entire training set (i.e. both synthetic and natural language examples across all adaptations), and report the percentage of successfully completed target tasks for both synthetic and natural language descriptions. For each experiment, we *tune the hyperparameters on the validation set, and report the success rate on the test set corresponding to the setting yielding the maximum success rate on the validation set.*""

## Environment / Dataset

**Organizer Environment**: Organizer with three shelves, 8 distinct objects per shelf, each object can take one of three colors.

Place objects in different configurations to create different states. Action space is 30 move actions, eg, 6 x 5 positions.


**Language Data**:

 Six different adaptations:

  - Same object in source and target, different positions
  - Differnet object, same final position
  - Move two objects with final positions swapped
  - Deleting a step from the source task
  - Inserting a step into the source task
  - Modifying a step in the source task

Also adapt the language by collecting paraphrases using Mechanical Turk.

## Experiments / Results

**Compositionality**: Humans can learn concepts like "blue box" and "red cylinder" and recognize a "blue cylinder". Can the proposed model do the same? To test this, create two new splits, in both splits the training data consists of data points that do not contain any blue cylinders or red boxes. Validate on blue cylinders and test on red boxes and vice versa. (This means that you tune the hyperparameters based on your ability to detect one of the unseen objects).

The results were that you can get good results (87.6%/62.4% success rate) but not as good as the case where everything is within-distribution (97.8%/75.7%).