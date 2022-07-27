---
title: Neural Event Semantics for Grounded Language Understanding
cite_key: conf/TACL/Buch2021
---

The general idea is to treat all words as classifiers that compose to for ma sentence meaning by multiplying output scores.

The classifiers apply to spatial regions and NES routes spatial regions (Events) to different classifiers via soft attention.

NEW offers stronger generalization capavbility than standard function-based compositional frameworks.

Related work: [[deep_compositional_question_answering_with_neural_module_networks]],  [[systematic_generalization_what_is_required_can_it_be_learned]] [[compositional_attention_networks]] [[closure_assessing_systematic_generalization_of_clevr_models]] [[latent_compositional_representations_improve_systematic_generalization_in_grounded_question_answering]][[gated_attention_architectures_for_task_oriented_language_grounding]] [[learning_to_reason_end_to_end_module_networks_for_visual_question_answering]]
[[explainable_neural_computation_via_stack_neural_module_networks]]
[[obtaining_faithful_interpretations_from_compositional_neural_networks]]
# Architectural Overview

![[neural_event_semantics_architectural_overview.png]]

In *conjunctivism* you assume tha the only operator is "and". Structure arises by routing evnet variables to function predicates.

Treat all words as event classifiers. For each word a single score indicates the presence of a concept on a specific input (eg, "red, above"). Then compose output scores from classifiers by multiplication, which generalizes logical conjunction.

The main challenge is routing. They do it by soft attentional event routing, which ensures that otherwise independent word-level modules recieve contextually consistent event inputs.

![[neural_event_semantics_end_to_end_architecture.png]]

## Conjunctivist Semantics

Consider:

$$
\exists e_1, e_2 \in V. \text{circle}(e_1) \land \text{on}(e_1, e_2)
$$

To evaluate this expression, you need an interpretation of the variables - an assignment of values in $V$ to event variables $e_i$. Then you route to the arguments of the predicates given the logical form. Do this with a routing tensor (a one-hot vector indicating which of the n event variables belongs to the argument slot).

How to translate an exists expression into a conjunctive one based on this? You could search over possible assignments to see if there exists one which makes the matrix true.

![[nes_classifying_routed_events.png]]

## Differentiable Event Argument Routingg

We need to predict the argument routing tensor $A$ from the input language. You can use softmax for this.

Predict attentions directly from the input tokenized text sequence - for each token $t_w$,  you pass the sequence through an LSTM and then use the bidirectional hidden state to output an attention matrix for each argument slot.

## Words as Event Classifiers

All words are event classifiers - words are associated iwth modules which outut a real-valued score of how true a lexical concept is for a given set of routed event inputs.

## Conjunctive Composition

To do the conjunctive composition, use log-addition. Length normalization is helpful to train on variable-length sequences.

## Existential Event Variable

![[nes_existential_event_variable_scoring.png]]

Decompose the world in a set of candidate event proposals. The existential closure is an operation that determines the best scoring assignment of event candidate values.

# Training

Train by gradient descent with a dataset of (T, W, Y), where T is the statement, W is some scene and Y is a true/false denotation. Use binary cross-entropy between prediction and ground truth label.

The main challenge is making the ranking operation differentiable - to do this, use a tunable approximation which approaches the max as $\beta \to \infty$ . $f_{\text{max}}(s, \beta) = \frac{\sum_q (s_q)^{\beta + 1}}{\sum_q (s_q)^{\beta}}$

## Learned Event Routing

![[nes_learned_event_routing.png]]

# Experiments

- ShapeWorld: Shapes with different color and spatial relationships. For each image, generaet multiple true/false statements. Standard generalization is where the distribution of ID and OOD are the same. Compositional Generalization is where the event distribution is unseen, every instance has at least one event sampled from a held out distribution. Eg, red triangles and blue squares present a train time, but blue triangles and red squares present at test time.


## End-to-experiments

In this setting, you do not offer the ground truth logical form input or supervision to the NES model.

## Real-world Language

Chairs-in-Context: Chairs and other objects from shapenet, paired with human generated language collected in the context of a reference game.

Language Generalization: Ground a specific chair from an input set given a referring statement.

Zero-shot generalization: Can you generalize to unseen object classes like tables and lamps?