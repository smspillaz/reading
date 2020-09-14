# Grounded Language Learning - Summary / Report

## Understanding Early Word Learning

### Environment 

Basic:
 - "Bump into an X"
  - X may have different properties in its binding
    - Eg, shape, color, shade, patterns, position


### Approach

 - CNN + LSTM for the sentence + GRU for the agent acting over time + A3C
 - Curriculum learning:
  - Present growing subsets of the words, each of which expands once you have 9.8/10 average reward.
  - This learns faster than if you just try to present all 40 shape words immediately

### Experiments

 - Sample efficiency: not great, curriculum learning requires 300,000 episodes
 - Visualization with t-SNE at least shows clusters of words that are from
   different categories, eg, color words in one cluster, shape words in another etc.

## BabyAI

### Environment

 - 2D Gridworld
 - Language contains 2.48 * 10^19 possible instructions with verifier
 
 "go to the red ball"
 "open the door on your left"
 "put a ball next to the blue door"
 "open the yellow door and go to the key behind you"
 "put a ball next to the purple door after you put a blue box next to a grey box and pick up a purple box"

 - Language exhibits properties such as different instructions,
   different temporal orderings within a sentence,
   different object bindings for instructions

To solve various tasks in the environment you need different competencies.
 - navigation
 - navigation with roadblocks
 - performing implicit actions (eg, unblocking the way, unlocking a door, etc)
 - going to a place
 - picking up an object
 - putting an object somewhere
 - comparing the location of objects

## Results on baseline

 - Very sample inefficient
 - Curriculum pretraining helps a littel bit, but not a lot.

## "Language as an Abstraction"

### Environment

 - Object arrangement task
 - Different sub-tasks:
    - Explicit arrangment
    - Sorting
    - Ordering
    - Sorting by shape
    - Ordering by shape
 - "Crafting" environment by Andreas et al.

### Basic Approach

 - Low Level Policy: Train a low level policy to interpret the language
 - High Level Policy: Train a high level policy to generate language instructions

#### Training the low level policy

 - Single policy network
 - Perform some actions conditioned on a language statement
 - If the goal is achieved, reward of 1 else reward of zero
 - Hindsight Experience Relabling using language as the new label


#### Training the high level policy

 - InfoGAN which generates language
 - Presumably the weights of the low level policy are frozen when you learn to generate the language instructions.

### Results

 - Still need millions of steps, though we learn faster than DDQN etc
 
## Learning Fast and Slow
 
  - Purpose: Learn new object bindings quickly with few-shot mechanism
 
### Environment
 
  - Custom "discovery" and "action" phase
  - Need to choose the right object based on the instruction
  - Language is quite limited: "Pick up an X", "Put the X on the Y"
    - Unclear what the language space is in their environment
 
### Basic Approach
 
  - GRU + Policy Network + Memory
  - Discovery phase encodes object representations to memory
  - Instruction phase retrieves the representation from memory as part of the policy
 
### Results

 - Getting high accuracy still requires about 600,000 "steps"
 - Not defined what a "step" is.
 - Nice results showing that you can at least generalize well to objects in the same class when using the memory.
 

# Opportunities

 - Only BabyAI seems to have a diverse set of language from the policy learning perspective
 - Everyone learns one big low level policy that intereprets the language.
   - Language as an abstraction learns to generate the language but this is not very interesting.
 - Language is compositional:
   - Can we for instance, learn several policies each of which can carry out a subtask, then
     use the language to route temporally ordered subtasks to policies.
   - Disentangled policy representations.
   - Planning MuZero style? If we know how an action will affect the environment, then we can
     use the language to help make a plan.
   - How to know when to learn a new policy vs re-use an old one?
   - How to ensure that you don't clobber old policies?
   - Testing: we should be able to carry out arbitrary compositions of tasks in a zero-shot style
     if we know how to break the task down into subtasks.
