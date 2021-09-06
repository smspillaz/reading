# Reinforcement Learning with Prototypical Representations

[[reinforcement_learning_prototypical_representations.pdf]]

https://icml.cc/virtual/2021/spotlight/10424

The goal of this work is improving sample-efficiency in image-based RL by pre-training.

The agent needs to learn both the representations and policy. How to close the gap?

 - Model-based mehtods
 - Auxiliary tasks
 - Data-augmentations


Learning a good representation requires a reward signal, leads to representations that are task-depedent.

Get close to the pre-training and fine-tuning paradigm.

## Decoupling Representation and RL.

 - We don't know what the dataset is
 - Dataset needs to be collected
 - Need a good exploration policy to collect new data, but we need good representations to figure out what states are new.

## Proto-RL

 - learn prototypical representations using self-supervised methods on collected dataset
 - explore environment using MaxEnt intrinsic reward based on prototypes to collect the dataset.


During the fine-tuning stage, take the pretrained representations and train a task specific policy, by casting image-based RL to state-based RL. Eg, treat the prototypes as states.

### Experiment

Image-based continuous control - no reward given, need to do unsupervised exploration.

Phase 1 - task agnostic pretraining. You can learn prototypical representaitons of different positions.

![[prototypical_rl_learning.png]]

Downstream task - navigate to red region of the maze. Encoder already pre-trained, prototypes scattered around the environment.

Experiments also show that initial pretraining means that once you find the goal in the new task, you learn the task very quickly.