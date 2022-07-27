---
title: Few-Shot Subgoal Planning with Language Models
---

Given a text instruction, language priors allow you to infer subgoal sequences. You don't need subgoal supervision - the language model can generate it for you.

Proposes a simple strategy to re-rank language model predictions based on interactions with the environment.

![[few_shot_subgoal_planning_with_language_models.png]]

"Put a rinsed slice of apple on the table". Here the subgoals are actually implicit, you need to figure out the context from the environment.

The main contributions are:

 - Proposing "in-context learning" with mutual information to predict subgoals with "very little supervision"
 - Incorporating a small amount of feedback from the environment
 - Combine predicted subgols with a pre-trained policy to get a modular agent.

Note: using language models to do planning and actions has already been explored in prior works (eg, on ALFRED).

This work is also related to few-shot learning with language models, eg, providing the right context to meta-learn which token probabilities and sequences to amplify.

Assumption: Subgoal supervision is avaialble for a small number of training tasks and then the inferred subgoals can be used for unseen tasks.

## How to generate the subgoals

There's a small amount of training data:

$$
\{(\tau_1, g_1) ... (\tau_n, g_n)\}
$$

You prompt a language model with a comma-separated concatenation of the training examples, eg, $\tau_i = g_i$.

Then the probabilit of a hypothesis $h$ (text representation of the subgoal sequence) is given by:

$$
p(h|\tau) = \prod_i p_{\text{LM}}(h_1|h_{<i}, \tau, \{\tau_j, g_j\}^n_{j = 1}
$$

Use beam search to identify the top-k hypotheses

## How to dynamically re-rank subgoals

Every time you complete a subgoal, look at the environment state and re-rank the subgoal sequences, then edecute the next subgoal from the highest ranked plan. Training the ranking model uses rewards from the environment.

This is where the mutual information loss comes in.

Generate multiple hypotheses using $p(h|\tau)$ and the generated hypotheses are re-scored using a LERP of a mutual information metric:

$$
(1 - \lambda)\log p(h|\tau) + \lambda \log p(\tau|h)
$$

(Note that the first one is $h|\tau$ and the second one is $\tau|h$!)

$p(\tau|h)$ is given by the language model.


## Results

They test on the ALFRED benchmark.

Only the interaction subgoals are predicted since navigation subgoals are usually irrelevant. Basically there is supervision on the subgoals that you can check against but they don't actually use them in training.

In training, you have $N = 22$ instances, so 2 instances per fine-grained task type.

Prompt the language model with the concatenation of these training samples and the query instance.

Then do beam search with beam size 10 to generate the subgoal sequences.

Example: "Place a martini glass with a fork on it on the table"

Two hypotheses:
 (a) pick up fork, put in cup, pick up cup, put in sink
 (b) pick up fork, put in cup, pick up cup, put in table

When the context contains examples which mention "sink", then (a) gets ranked over (b). But when you remove those examples, then (a) is ranked below (b).

There are two ways to compute the ranking! You can compute $h|\tau$ or $\tau|h$ . As mentioned before, we compute mutual information as opposed to just conditional probability of one or the other.

Doing this boosts your success rate to about 20%

### Collecting Feedback

Collect feedback using 1000 training examples. This boosts performance to 24% success rate, which is pretty good compared to 30% when you have full subgoal supervision.
