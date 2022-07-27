---
title: Challenges of Acquiring Compositional Inductive Biases via Meta-Learning
---


Given an inductive bias, construct a family of tasks which inject the bias into the parametric model if meta-training is performed on the constructed task family.

Various approaches considered to the construction of the family of tasks and the process of selecting support sets for a particular single-task problem on SCAN.

Conclusion: existing meta-learning approaches to inject compositional inductive bias are brittle and difficult to interpret, showing high-sensitivity to the family of meta-training tasks and the procedure for selecting support sets.

Recent studies have shown that compositional generalization is a hard problem:
 - [[compositional_generalization_through_meta_seq2seq]]
 - [[generalization_without_systematicity_on_the_compositional_skills_of_sequence_to_sequence_rnns]]
 - [[a_study_of_compositional_generalization_in_neural_networks]]
 - [[compositionality_decomposed_neural_networks_generalize]]

It is possible to generate an architecture that does compositional generalization for specific tasks, but the level of expertise required for that is quite high. Meta-learning might help here.

They test on [[generalization_without_systematicity_on_the_compositional_skills_of_sequence_to_sequence_rnns|SCAN]]. 

It is rich enough to construct challenging compositional generalization tasks, including the "add primitive" split.

 - Training set contains "jump" command mapped to JUMP as well as composite commands not using JUMP. They are held out in the test set.

Meta-sequence-to-sequence [[compositional_generalization_through_meta_seq2seq]] tried this

# Experiments on Meta Seq2Seq

Experiments where test accuraccy was very low:
 - B: Only permute the non-jump verbs
 - C: Does meta seq2seq learn a useful inductive bias when meta-trained only on task where either the command or target verb words are permuted?

## How to select the support set?

Experiment 1: Choose support sets uniformly from the training set ith only the four primitive verb commands used as a support set

Experiment 2: Uniform sampling from the train set

Experiment 3: Enforce the constraint that all words used in the quyery commands are represented by the support commands

Experiment 4: Safe support set selection procedure in experiment 3 but for both train and test

Experiment 5 and 6: Permute the verbs and the connectives together.

# Conclusions

1. The procedure for selecting support set data plays a crucial role 