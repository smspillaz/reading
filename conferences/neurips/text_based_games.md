# Text based games

## Keep CALM and explore

[[calm_language_models_action_generation.pdf]]

Objective - train a game-agnostic language model to output useful action priors in text based games.

Choose meaningful actions from a large action space. Use a second model to decide which actions to take for each game.

Proposed model - train a language model to generate a compact set of action candidates at each game staet.

 - Pre-training on general text corupus
 - Fine-tuning on human gameplay on text based games.


Ranking algorithm, essentially.

Previous work:
 - RL models - need to be hardcoded
 - Language models: they're not tuned to produce actions that are valid.

### DRRN

![[calm_drrn.png]]

DQN with observation and action encodings given by two separate GRU layers.

To train the language model, use a dataset of trajectories on human gameplay. Two options:

 - N-grams
 - GPT2


The context is the trajectory until that point - but you approximate it with the most recent observation.

Language model - "actions" are conditioned on the context and the previous words (autoregressive).

Use an external program to resitrct the possible actions to verb + noun.

### Environment: Jericho

Open AI gym like interface for learning agents.

 - Provides optimal trajectories
 - Provides additional information on each game etc.


### Experiments

Can you predict optimal action priors and avoid inadmissible actions?

 - Average of precision of admissible actions
 - Recall of admissible actions
 - Recall of gold actions (optimal actions)

Fraction of admissible actions among $k$ predicted actions decreases with $k$.

GPT2 more easily able to find the optimal action.

Pre-training is useful.

### Remarks

RL is treated as a downstream task.

Zero-shot action prior.

Language works as a universal interface for all text based games.

GPT2 is able to propose optimal actions more often than an n-gram model trained on "human gameplay"

Action templates - shrinks the possibilities that you have. Pick a template, then fill in the blanks.

## RTFM - Ready to fight monsters

[[rtfm_generalizing_by_reading.pdf]]

Dynamics are described in the environment.

Look at which monsters are in the team - defeat the order of the forest. You have to check what is strong against certain monsters. Explicit planning and decisionmaking.

Text-to-$\pi$ model:

![[text_to_pi.png]]

 - Encode bidirectional LSTM and attention to summarize documents.
 - Use bidirectonal FiLM to modulate visual inputs using text inputs and vice versa. Modulate the text using the vision too.
 - Use summary of processed visual features as a representation for computing the policy and value baseline.

You have positional encodings for objects as well, plus visual features.

We do self-attention on the inventor and the goal. Attention is used on the Document.

### Baselines

1. FiLM instead of Bi-FiLM
2. Language conditioned residual CNN
3. Ablated versions of the original


Author's model is the best performign model.

CNN does worse than random choice.

### Curriculum Learning

Features of the task that increase difficulty

1. Size of the gridworld
2. Group of monsters
3. Moving monsters (dyna)
4. Using NL instead of templates to express goal and document

Transfer to 10x10 gets you an OK result but not great.

RTFM makes it impossible ot memorize a policy from experiment because the environment is nonstationary.

Looks like more of an associative task than language understanding.

Conv + concatenating the text features is rubbish. FiLM and attention really are necessary here.

GLuE - transformers with self-attention and cross-attention and iterate multiple times.