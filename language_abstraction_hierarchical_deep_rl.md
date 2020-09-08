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
       
Language Guided RL:
