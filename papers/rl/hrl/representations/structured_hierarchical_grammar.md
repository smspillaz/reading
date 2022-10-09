---
title: "Reinforcement Learning with Structured Hierarchical Grammar Representations of Actions."
venue: "CoRR"
volume: "abs/1910.02876"
year: 2019
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-1910-02876"
ee: "http://arxiv.org/abs/1910.02876"
url: "https://dblp.org/rec/journals/corr/abs-1910-02876"
authors: ["Petros Christodoulou", "Robert Tjarko Lange", "Ali Shafti", "A. Aldo Faisal"]
sync_version: 3
cite_key: "journals/corr/abs-1910-02876/Christodoulou/2019"
tags: ["DeepMind"]
---
# Reinforcement Learning with Structured Hierarchical Grammar Representations of Actions

Basic Idea: Humans learn to use grammatical principles to combine words into sentences.

Action grammars: "There is an underlying set of rules" that govern how we hierarchically combine actions to
form new more complex actions.

To construct a valid sentence we generally combine a noun phrase with a verb prhase. Action grammars
are a similar idea - we form a grammar in hierarchical structures that allows us to produce new
actions by combining old ones.

Action Grammer Reinforcement Learning (AG-RL): Framework to incorporate the concept of action grammars.
Compose primitive actions (words) into temporal abstractions (sentences). The extracted grammar gets appended
to your action set in the form of macro-actions. Then you continue playing with a new action set that includes
the macro-actions.

## Prior Work

Strategic Attentive Writer (STRAW): Deep RNN with two modules:

 (1) Take an observation of the environment to produce an action plan, $A \in R^{|A| \times T}$,
where $A$ is the set of actions and $T$ is a pre-defined number of timesteps $> 1$. as $T > 1$,
creating an action plan involves making decisions that span many timesteps.

 (2) commitment plan: $c \in R^{T}$, used to determine probabilities of terminating macro-action and re-calculating action
     plan (similar to options framework)

AG-RL is different in that you are only allowed to pick macro-actions as defined by your grammar.

Fine Grained Action Reptition (FiGAR): Two policies:

 (1) Choose a primitive action as normal
 (2) Choosen how many times that action will be repeated.

AG-RL allows you to pick macro-actions that are not necessarily repetitions of single primitives, but
instead could be combinations of actions.


## How it works

Iterate two steps:

 (a) Gather experience for N episodes: Off-policy agent interacts with the environment and stores experience

   - Effectively random exploration for a fixed number of timesteps
   - But for some episodes we do no random exploration and instead store the experiences separately -
     this will be stored in a set which is used later in part (b)

 (b) Identify action grammar: Experiences used to identify the agent's action grammar appended to the action set.

   - "Feed the actions into a Grammar Calculator" (Sequitur): you receive a sequence of actions as input, then create
     new symbols to replace any repeating sub-sequences of actions.
   - Obviously the actions are noisy, so we need to regularize somehow
      - $k$-Sequitur: Only create a new symbol if a sub-sequence repeats itself at least $k$ times.
      - Information theoretic criterion: Does adding the new symbol reduce the total amount of information
        needed to encode the sequence.
      - (Idea: can we compare action sequences based on an edit distance criterion, then take the average sequence?
         You're still going to have some stochastic behaviour, requiring exact matches is a bit weird)
   - Append the new symbols ot the set of actions:
      - How to do this without destroying the policy you've already learned?
          - Transfer learning: Add a new node to the final layer, leaving all other nods unchanged
          - Initialize the weight of the new action to the weight of its first primitive, so
            that you're equally as likely to pick the new action in a situation where you would
            pick the first primitive.

   - Repeat this process, now the new symbol is a part of your action set.

Also some additional changes

(1) Hindsight Action Replay: Instead of re-imagining the goals, create new experiences by
    re-imagining the actions:
    (a) If you play a macro-action, then store the experiences as if you had played the individual actions
    (b) If you play a sequence of primitive actions that is a macro-action, store it as if you
        had played the macro action.

(2) Sample experiences from an action-balanced replay buffer - return samples of experiences containing
    equal amounts of each action.

(3) "Abandon Ship": During every timestep of a macro-action, work out how much worse it would
    be to just bail and pick the highest value primitive instead. Compute the value as $d = 1 - \frac{e^{q_m}}{e^{q_{\text{highest}}}$.
    Store also the moving average and standard deviation of this value. Then compare
    $t = D_{\mu} + D_{\sigma} z$ (z is a hyperparameter). If $d > t$, then abandon the
    macro-policy.

 (4) Random exploration si biased towards macro-actions.


## Example: Towers of Hanoi

There are 6 actions "a, b, c, d, e, f". After some time you pause the agent and figure out what
it learnt by asking it to replay a game on-policy. If you see repeated actions, eg "bc", "ec",
"baf", "bagbcd", put them into your grammar set. Then continue playing but now you can
pick a "macro-action" instead.

AG-DDQN can improve on DDQN baseline by quite a bit. Median improvement of 31%,
maximum improvement of 700%.

## Ablation Study

HAR is crucial for improved performance and without it you don't do much better than DDQN.

Abandon ship also imprortant.

The action balanced replay buffer is not so important.