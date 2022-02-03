---
title: Language as an Abstraction for Hierarchical Deep Reinforcement Learning.
venue: NeurIPS
pages: 9414-9426
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/nips/JiangGMF19
ee: https://proceedings.neurips.cc/paper/2019/hash/0af787945872196b42c9f73ead2565c8-Abstract.html
url: https://dblp.org/rec/conf/nips/JiangGMF19
authors: ["Yiding Jiang", "Shixiang Gu", "Kevin Murphy", "Chelsea Finn"]
sync_version: 3
cite_key: conf/nips/JiangGMF19
---
# Language as an Abstraction for Hierarchical Deep RL

How do we solve complex temporally extended tasks? Probably by decomposing into parts, but this is not
yet solved. Acquiring good abstractings from hierarchical RL is challenging.

This work: Use language as the abstraction. Learn an instruction following low-level policy and a high level
policy that can re-use abstractons across tasks.

Tested on MuJoCo and CLEVR.

Result: We can do things like object sorting, multi-object re-arrangement.

## Background

Right now, solving long-horizon tasks requires sophisticated exploration and structured reasoning, risk
of overfitting due to a lack of samples in the problem space.

Hierarchical RL: Prior work shows that hard-coded abstraction lack modeling flexibility and
end up being task-specific. Learned abstractions tend to find degenerate solutions without careful tuning.

Have the higher level policy generate sub-goal state and have the low-level policy try to reach that goal.
Doesn't generalize to new goals.

## Contributions

Use language as the interface. Low level policy follows the language instructions, high level
policy produces language that gets gets the low-level policy to do what you want.

Advantages:
 - low-level policy can be re-used
 - high level policies are human interpretable
 - strict generalization of the goal state

How to do this? Generalize prior work on goal relabelling in the space of language instructions, allow
agent to learn many language instructions at once.

Generate scenes and language descriptions. Low level policy objective is to manipulate objects within the
scene such that a description or statement is satsified.

## Related Work

Two approaches on difficult domains:
(1) Learn low level policy end to end from the final task rewards, through option-critic, multi-task or meta-learning.
Depends entirely on the final task reward, scales poorly, sample inefficient.
(2) Augument the low level learning with auxilary rewards as a learning signal, including
 - mutual information
 - hand crafted rewards related to the domain
 - goal oriented rewards
   => This work fits in here, represents goal *regions* using language instructions, as opposed to individual goal states.
   => "region": set of states that satisfy more abstract criteria as described by the language
      ("red ball in front of the blue cube") -> this goal can be satisfied by many states which
      are different in pixel-space, rather than just measuring how $\epsilon$-close we are to
      the actual goal.
   => (comment: So this is sort of like regularization then. Making the loss about $\epsilon$-closeness
       probably makes you overfit to that problem)

## Some preliminaries

RL: $\max \pi(a_t, s_t) = \sum_t E_{s_t, a_t}[\gamma^t R(s_t, a_t)]$

Goal Conditioned RL: Augmented MDP, but with an additional element for a goal G
and reward function $S \times A \times G \to [r_{\text{min}}, r_{\text{max}}]$ -
reward under a given goal. Basically the goal is a parameter.

Q-Learning: Off-policy RL: Learn the Q function which represents the expected total
discounted reward if you take an action in a given state, then optimize by picking the
best action later.

Hindsight Experience Replay: Data-augmentation technique. Relabel each tuple's $s_g$ with
$s_{t + 1}$ or other future states and adjust $r_t$ to be the appropriate value. Basically
take the experience that you had and relabel it the rewards that you would have gotten
from some other goal(?)

## Language Conditioned RL

Basically we have a conditional density which maps an observation to
a distribution of language statements that describes $s$. We have a goal function
which is 1 if the goal specified by the language is satisfied, 0 if not.

Basic idea: Low level policy solves an MDP given a goal. The high level policy
gives you a goal. Both are trained separately. Can do joint fine-tuning.

For language instructions: Need to train to ensure that the action is actually
inducing the reward -> check if the indicator variable was 0 before and if it changed
to 1 as a result of taking this action.

Problem: how to determine a meaningful distance metric in the space of language statements
so we can know that we're closer to the goal. Proposal: trajectory re-labelling.
 -> Re-label states in the trajectory with elements of the support set of $s_t$ as the goal
    instruction using a relabeling strategy.
 -> Basic idea: your action didn't achieve *this* goal, but it achieved some *other* goal, so add that experience to the training set. Appendix doesn't seem to be in the paper...


Acting within the language:
 -> "We show how we might incorporate a language model in Appendix A which shows preliminary results but also challenges"
 -> Technically the size of the action space scales with the number of tokens in the
    language, but the fact that the grammar is consistent means that this isn't
    a problem in reality.

How to generate the language?
 -> Generate some isotropic noise and latent code
 -> Use a generator component to map from a latent code $\hat z$ to a vector
 -> Use a discriminator to determine if the generated sequence is from the distribution.

They don't actually condition on the language, but rather condition on these
disentanged embeddings (see Appendix A).

## The Environment

Basic difference between this and BabyAI: A *physical* simulation is developed, not
just grid-world.

High Level Tasks:
 - Object Arrangement
 - Object Ordering
 - Color Ordering
 - Shape Ordering
 - Color and Shape Ordering

In all cases, binary reward only.

## Policy Parameterization

Encode instruction with a GRU and feed the result + state into a neural network which
predicts the Q value of each action.

# Experimental Questions

## As a representation, how does language compare

## How does the framework scale with diversity of instruction and dimensionality of state

Can paraphrase 600 instructions to achieve about 10,000 total instructions. Compare
with:
 (1) One-hot representation of instructions
 (2) Non-compositional latent variable (autoencoder)
 (3) Bag of Words

One-hot degrades once you have many instructions, no sharing.

Latent variable representation does not work - agent does not make meaningful progress.

Bag of Words: Language agent does better in the long run.

## Can the policy generalize in systematic ways

Design training and test sets that are distinct. In principle, if you learn the language
you should be able to get good performance on the test set instructions.

Example: Remove all sentences with the word "red" in the first part from the training set,
test on sentences that have this property. Still do better than random, so you learn
the sentence, not just "red" being in that position.

## How does it compare with SOTA hierarchical RL

Compare vs baselines:
 - HIRO
 - Option Critic
 - DDQN

Only the proposed algorithm solves things correctly. High level policy has difficultly
learning from pixels alone.

## Limitations

Current method relies on instructions provided by a language supervisor which has access
to the instructions that describe a scene. In principle you could replace this with
an image captioning model.

Another problem: Instruction set is specific to the problem domain - can we make the
agent follow a much more diverse instruction set that is not specific to any domain.

Using an LM instead of InfoGAN to generate the instructions: LM seems to drop nodes.



## Interesting Parts
 - Generate language as an intermediate representation
 - Goal-oriented re-labeling (so that we don't waste training examples)
 - Even if you've never seen words in a particular position, can still do
   better than random choice.
 - Generate disentangled representation of the language, as opposed to using
   language model.


## Questions

 - The environment defines things like "this is a blue ball" or whatever. So really
   you just need to learn what the environment tells you. Can you use a language model
   to augment the policy?
   => For instance if you learn how to complete the task "put the dax on the bed",
   can you bind this to other objects with this method based on a statistical language
   model? In this way, could you learn generating the instruction for one object and then
   generalize to other objects (assuming that you knew what they were?)
   => ties into image captioning, describe the image in language
 - Instead of using language, can we generate a graph? The graph can be a kind of
   high level representation.
 - How do you deal with an unreliable teacher? Can we figure out information that's wrong,
   for example?