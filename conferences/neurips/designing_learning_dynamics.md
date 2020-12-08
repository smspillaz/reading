# Designing Learning Dynamics

Assume that optimization has been solved.

Divide the world into two things:
 - Leaners: Architecture, algorithm
 - Objectives: What is optimized (dataset, loss, environment, reward)

All that's left is the objective:
 - How to construct objectives
 - How to evaluate objectives
 - How to combine objectives

How tasks are constructed:
 - Someone has to curate a dataset
 - Someone has to build an environment

 - Hard, simple (long tail of edge cases), too many (garden of forking paths)

Tasks are usually the main bottleneck of progress - we typically have
algorithms lying around for many years.

Tasks - no guarantees: we cannot formally specify what a cat or dog is except with
reference to some data.

Learning theory: provides formal generalization guarantees based on unrealistic
assumptions (eg, train and test data being IID).

How are tasks evaluated?
 - Usually they just aren't.

Evolution is not optimization - life is not a suite of tasks. Rewards are
insanely sparse, success depends on more than just the algorithm.

## Mechanisms for learning

As artificial learners proliferate it is important to understand and control their
interactions.

Classical mechanism design - humans are rational self-interested agents (assumption),
then figure out a strategy to maximize everyone's utility.

Mechanism Design for AI: implement solutions to problems that involve multiple interacting agents.
Classical mechanism design usually focuses on convex problems.

## Learning objectives

 - Learning: Don't hand-craft behaviorus, learn them (lose guaranatees)
 - Learning representations: Don't hand-craft features (nonconvexivity)
 - Learning losses: Don't want to hand-craft tasks. We can't design good objectives.
   Leads to adversaries finding loopholes in the objective (what is the task?)

## Games

Any dynamical system arises as simultaneous gradient descent on a game.
