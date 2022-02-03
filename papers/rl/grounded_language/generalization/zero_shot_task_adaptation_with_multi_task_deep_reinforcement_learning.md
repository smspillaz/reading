---
title: Zero-Shot Task Generalization with Multi-Task Deep Reinforcement Learning.
venue: ICML
pages: 2661-2670
year: 2017
type: Conference and Workshop Papers
access: open
key: conf/icml/OhSLK17
ee: http://proceedings.mlr.press/v70/oh17a.html
url: https://dblp.org/rec/conf/icml/OhSLK17
authors: ["Junhyuk Oh", "Satinder P. Singh", "Honglak Lee", "Pushmeet Kohli"]
sync_version: 3
cite_key: conf/icml/OhSLK17
---

Considers two types of generalization:
1. To previously unseen instructions
2. To longer sequences of instructions

For generalization over unseen instructions, propose a new objective which encourages learning correspondences between similar subtasks by making analogies.

For generalization over longer sequences, propose a hierarchical architecture where the meta-controller learns to use the acquired skills for executing the instructions.

The agent's overall task is to execute a list of instructions described by natural language while also dealing with unexpected events. We assume that each instruction can be executed by performing one or more high level subtasks in a sequence.

Why is this difficult?
1. Generalization
2. Delayed reward (not told which instruction to execute, only given a list of instructions, no signal on completing any one instruction)
3. Interruption: Unexpected events (low battery, bonuses, urgent interruptions)
4. Memory: Loop instructons like "pick up 3 pigs", which require doing the same instruction multiple times and taking into account the history of observations.


## Desiderata

1. Execute novel subtasks
2. Keep track of what has been done so far
3. Monitor observations
4. Interrupt ongoing subtasks
5. Switch to the next instruction when the current one is finished

## Approach and Architecture

![[architecutre_of_zero_shot_task_generalization_instruction_following.png]]


(1) Learning skills to perform a set of subtasks and generalizing to unseen subtasks
(2) Learning to execute instructions using the learned skills.

Assume that the subtasks are defined by disentangled parameteres. The first stage in the architecture learns a parameterized skill to perform different subtasks depending on its input parameters.

In the second stage, the architecture learns a "meta-controller" on top of the parameterized skill so taht it can read instructions and decide which subtask to perform.

To deal with the "delayed reward" problem, propose a novel neural network architecture that learns when to update the subtask in the meta-controller.

### Learning a Parameterized Skill

A **parameterized skill** is a multi-task policy corresponding to multiple-tasks defined by input task parameters. It is the cartesian product of many different task aspects (eg, action, object, target object, etc).

the parameterized skill is represented by a NN which maps input task parameters into a task embedding space, which is combined with the observation followed by the output layers.

#### Generalization via analogies

To generalize to unseen takss the network needs to learn about the relationship between the task parameters and the task embedding.

We propose an "analogy objective". The main idea is to learn correspondences between the tasks. Assume that the target objects and the action are independent and enforce the analogy (Visit X, Visit Y :: Pick up X, Pick up Y), which should mean that the difference between "Visit" and "Pick up" in vector space is the same regardless of the $X$ and $Y$  which is the target/source object. The same can also be applied to the objects as well - the distance between any two task embeddings concerning different should be the same for different tasks. More specifically:

$$
||\triangle(g_a, g_b) - \triangle (g_c, g_d)|| \approx 0
$$

where $g_a : g_b :: g_c : g_d$

$$
||\triangle(g_a, g_b) - \triangle (g_c, g_d)|| > \tau
$$

where $g_a : g_b \ne g_c : g_d$

$$
||\triangle(g_a, g_b)|| > \tau
$$

if $g_a \ne g_b$

where $\mathbf{g_k} = [g^{(1)}_k, g^{(2)}_k, ..., g^{(n)}_k]$

are the task parameters.

We then have some loss functions to enforce these and use a contrastive learning process to enforce the analogies.


### Network Architecture

The network architecture for the parameterized skill consists of four convolution layers and one LSTM. Then use actor-critic to learn a policy through the network.


## Results and Scenarios

1. Independent The task space is $\mathcal{G} = \mathcal{T} \times \mathcal{X}$ where T is  one of "pick up", "visit" or "transform" and $X$ is the set of object types. Should generalize ot unseen configurations of task parameters. With analogies, you more or less retain performance.
2. Object-dependent: Task space is defined as $\mathcal{G} = \mathcal{T}' \times \mathcal{X}$ where $T' = T \cup \{\text{Interact With}\}$. Divide the objects into two groups, one that should be picked up and one that should be interacted with. Applied analogy making so that analogies cna be made within the same group. Again with analogies, performance is more or less retained.
3. Interpolation / Extrapolation: $\mathcal{G} = \mathcal{T} \times \mathcal{X} \times \mathcal{C}$ where $\mathcal{C} = \{1, 2, ..., 7\}$. The agent should perform the task $c$ number of times. Only 1, 3, 5 are given during training and the other unseen numbers should work during testing. Performance retained somewhat with analogies.


## Executing instructions using the parameterized skill (meta controller)

![[zero_shot_task_generalization_meta_controller.png]]


We have a hierarchical controller which learns to output skills based on an identified subtask.

The meta-controller maps $\mathcal{O} \times \mathcal{M} \times \mathcal{G} \times \mathcal{B} \to \mathcal{G}$  where $\mathcal{M}$ is a list of instructions. It decides which subtask parameter $g_t \in \mathcal{G}$ conditioned on $x_t \in \mathcal{O}$, the list of instructions $M \in \mathcal{M}$ and the previously selected subtask $g_{t - 1}$ and its termination signal.

In this design the metr-controller can update its subtask at any time and takes the termination signal as an additional input.

In order to keep trakc of execution, the meta-controller maintains its internal state by computing a *context* vector and determines which subtask to execute by focusing on one instruction at a time from the list of instructions.

**Context Vector**: LSTM from states and hidden state previously.


**Subtask Updater**: There is an instruction memory. Retrieve an instruction using a pointer into the memory and compute the subtask parameters.

 - The instrucition memory is a size $K$ list of $E$ dimensional blocks, embeddings for each sentence. The subtask update maintains an *instruction pointer* which is non-negative and sums up to 1, indicates which instruction is being executed.
 - The idea is that the optimal policy keeps the instruction pointer unchanged while executing an instruction and increases the pointer by +1 precisely when the current instruction is finished.

**Learning on a long timescale**: The tasks change infrequently. Learn the time-scame of the metacontroller by introducing an internal binary decision which indicates whether ot invoke the subtask updater to update the subtask or not.

The meta-controller consists of three convolutional layers and one LSTM layer.