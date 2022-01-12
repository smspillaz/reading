---
title: Embodied Intelligence via Learning and Evolution.
venue: CoRR
volume: abs/2102.02202
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2102-02202
ee: https://arxiv.org/abs/2102.02202
url: https://dblp.org/rec/journals/corr/abs-2102-02202
authors: ["Agrim Gupta", "Silvio Savarese", "Surya Ganguli", "Li Fei-Fei 0001"]
sync_version: 0
---

# Embodied Intelligence via Learning and Evolution

Introduces Deep Evolutionary Reinforcement Learning (DERL), can evolve diverse agent morphologies to learn challenging locomotive and manipulation tasks in complex environments using only low-level ego-centric sensory information.

Several relations demonstrated:
1. Environmental complexity fosters the evolution of morphological intelligence as quantified by the ability of morphology to facilitated the learning of novel tasks
2. Evolution rapidly selects morphologies that learn faster
3. Mechanistic basis for both the Baldwin effect and the mergence of morphological intelligence through the evolution of morphologies that are more physically stable and energy efficient.

![[derl_overview.png]]

How does DERL work? The agent can evolve by adding, deleting or configuring a limb. This is the outer loop. Then there is an inner RL loop which optimizes the parameters of he neural controller.

## Contributions

1. Efficient method for parallelizing computations (DERL)
2. UNIMAL: Morphological design space
3. How to evaluate the ingelligence of the agent based on how easy to is to learn a policy for that agent.


## DERL: What is it?

Evolutionary algorithms just replace entire populations each timesteps by applying mutations to the fittest individuals. Scales poorly  due to significant computation burden.

Decuple learning and evolution in a distributed asynchronous manner using tournament based evolution.

 - Start with 576 agents, each undergoing lifetime learning via RL.
 - Each worker conducts a tournaments in groups of 4 where the fittest individual is set as a parent and a mutated copy is added to the population after evaluating fitness.
 - Only consider the most recent P agents as alive. Can do the evolution step after a given worker finishes rather than waiting for the whole batch to come back.


## UNIMAL: Universal Animal Design Space

 - Kinematic tree corresponding to a hierarchy of articulated 3D rigid pats connected via motor actuated hinge joints.
 - Evolutionary process as described above (add, remove, edit a joint)
 - Assumption of bilateral symmetry. So you don't have to learn left/right balance.


## Testing in Complex Environments

(1) Flat Terrain
(2) Variable Terrain
(3) Non-prehensile manipulation in Variable Terrian

In Variable Terrain, each episode looks different. Requires 10^7 agent interactions.

In MVT the agent must rely on complex dynamics to manipulate the box while also traversing VT.

### What sort of agents do you learn in each environment?

In VT/MVT: you are longer along the direction of forward motion and shorter in height compared to agents evolved in FT.

DERL finds morphological solutions for all 3 environments, but you start from high average fitnes.

**Diversity of solutions** The hard part is maintaining diversity of successful solutions since usually 1 solution just dominates. By moving away from generational evolution in which the entire population competes to asynchronous small tournaments, this enables ancestors who have lower fitness to stick around for longer and increase the diversity of the pool.

## Environmental Complxity Engenders Morphological Intelligence

Across the test tasks, agents evovled in MVT perform better than agents evolved in FT.

In our framework, intelligent morphologies facilitated faster and better learning in downstream tasks.

Across all generations, morphologies that are more energy efficient perform better and learn faster.

## Task Suite

 - Patrol: Run back and forth between two goal locations. To succeed you have to move fast for a short duration and then quickly change direction repeatedly.
 - Point navigation: Spawned in a flat arena and you have to reach a random goal location in the arena.
 - Obstacle: Static obstacles, each varying in height. To succeed you have to manuever around the obstacles.
 - Exploration: Maximize the number of distinct squares visited.
 - Escape: At the center of a bowl surrounded by bumps. The agent has to maximize the geodesic distance rom the start location (eg, escape the hills).
 - Incline: Move on a rectangular arena inclined at 10 degrees.
 - Push box incline: Push a box up a hill
 - Manipulate ball: Have to move the ball from source to target.