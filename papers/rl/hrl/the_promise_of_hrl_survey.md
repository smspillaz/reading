# The promise of Hierarchical RL

From The Gradient:

 - https://thegradient.pub/the-promise-of-hierarchical-reinforcement-learning/

In general, Hierarchical RL, decompose the task into sub-tasks.
So in Hierarchical RL, we have two problems: figure out the sub-tasks
then figure out the main tasks.

Need to engage in *temporal abstraction*.

Temporal abstraction convers RL into hierarchical RL.

Promises:

 - Sample efficiency
 - Scaling up to a large state/action space
 - Generalization: Transfer learning
 - Abstraction: Simplify the problem, since the sub-tasks can be solved.


Simple RL only operates on the abstraction of the simplest possible action
granularity. Risk of overfitting and the reward signal is pretty small.

## Basic Idea

We're trying to solve an MDP.

HRL: Extend the available actions os that you can do
meta-actions as well as regualr actions. Meta-actions
take more time than regular actions.

Eg, we choose subroutine $\sigma$, which in turn uses
$\pi_{\sigma}$ to do some actions.

Promise of HRL:

 - Long term credit assignment: faster learning / generalization
 - Structured exploration: Explore within the sub-policies
 - Transfer learning

### Feudal Learning

Basically, your actions are to set goals for the
sub-policies. The sub-policies in turn optimize the set
goal by using their sub-policies, until you get to the baseline policy.


Information Hiding: You observe the hierarchy at different resolutions

Reward Hiding: Communicate through goals.

Feudal Q-learning algorithm: (Dayan et al 1993, NIPS): Only tailored
for specific kind of problems, does not converge to optimal policy.

### Options Framework

See:
 
 - The Option Critic Architecture (Pierre-Luc Bacon, Harb et al, 2017)
 - Between MDPs and Semi-MDPs: A framework for temporal abstraction in RL (Sutton & Singh, 1999)

Basically, you have a triple $o = (I_o, \pi_o, \beta_o)$

 - $I_o$: The initiation set
 - $\pi_o$: The option's policy (0 or 1)
 - $\beta_o$: The termination condition

Maybe you have a set of primitive actions and higher level actions. If you
combine the options and primitive actions, you can make an optimal policy.

Bottom-level policy:

 - Observe environment
 - Output actions
 - Run until termination

Top level policy:

 - Observe environment
 - Output sub-policy
 - Run until termination

Option framework doesn't specify how you do task segmentation.

Basic idea: Keep running the option until it doesn't make sense anymore,
then go back to figuring out what to do.

### Hierarchical Abstract Machines

Non-deterministic finite state machines, transitions may invoke
lower level machines. The FSMs are hand-written, the policy just figures
out which machiens to call.


### MAX-Q

Decompose $Q$-value into state-action pairs
of $Q(p, s, a) = V(a, s) + C(p, s, a)$.

$V(a, s)$: The total expected reward when executing $a$ in $s$.

$C(p, s, a)$: Total expected reward from the performance of the parent task.

$a$ can contain a sequence.

Learns a recursively optimal policy - policy for parent task is optimal given
the learnt policies of children.

Policy is context-free - you just solve the parent's goal, not the global goal.


### FUN (Feudal Networsk for Hierarhical RL)

 - https://arxiv.org/abs/1703.01161

Manager chooses a direction in the latent state space and worker learns
to achieve that through the environment.

Also a method that enables better long-term credit assignment.

### Option-Critic

Apparently end-to-end and can sale to very large domains with sub-policies
with theoretical possibility of learning options jointly.

Train the manager's output with gradients coming directly from the worker.


### HIRO (Data Efficient Hierarchical Reinforcement Learning)

 - Nachum et al. Data-Efficient Hierarchical Reinforcement Learning (2018)

More sample efficient due to off-policy correction. Train $\mu^{\text{lo}}$
with experience transitions using reward given by a goal-conditioned function.

Train $\mu^{\text{hi}}$ on temporally-extneded experience, where $\hat g_t$
is a re-labelled high level action to maximize probability of past low level actions.

(Basically, HIR).

### HAC

Learning multi-level hierarchices with hindsight

 - Jointly learn a hierarchy of policies
 - Hierarchies have a specific architecture consisting of a set of nested
   goal-conditioned policies that use the state space as the mechanism for breaking
   down a task into subtasks.
 - Apparently more efficient as HIRO which doesn't use this hindsight stuff.

### AlphaStar

Controller chooses a sub-policy based on current observations at each relatively
large time interval.

Then every second the sub-policy chooses a macro-action, mastered before
learning from the repetitions of human expert games.

### h-DQN

Hierarchical DQN - integrate hierarchical value functions operating on
different temporal scales with intrinsically motivated deep RL.

Allows for flexible goal specifications such as functions over entities
and relations.

Meta-controller chooses the goal which the controller then tries to
satisfy.

### Meta-Learning shared Hierarchies

### Strategic Attentive Writer

Build implict plans in an end-to-end manner by interacting with
an environment.

Build an internal plan which is continuously updated upon observation
of the next input from the environment. Learn how long you can
follow the pan for without having to re-plan.

### H-DRLN

"Deep Skill Networks"

 - Knowledge transfer from one task to another whiel retaining the previously learned knowledge base.

### Abstract Markov Decision Process

 - MDP whose states are abstract representations of the states of an underlying environment
 - Actions are either primitive actions from the environment or subgoals to be solved.
 - Tries to solve a limitation of MAXQ, which is that value funtions over the hierarchy
   are found by processing the state action space at the lowest level and "backing up" values
 - AMDPs model each subtask's transition and reward functions locally resulting in faster planning.


### Iterative Hierarhical Optimization for Misspecified Problems

 - What happens when a representation cannot express any policy with acceptable performance?
 - Use RL as a black box that iteratively learns options to repair the MPs.
 - Partition the state space and train one option for each class in the partition.

### HSP (self-supervised)

 - Use unsupervised asymmetric self-play for pre-training
 - Devise tasks for yourself via goal-embedding and then try to solve them
 - Then the high-level policy just needs to figure out how to set goals.


### Learning representations in model-free HRL

## Future of HRL

 - Are the behaviours completely specified? Options

 - Are the behaviours partially specified? HAM

 - If you don't know? MaxQ, Learned Options

Sample efficiency is still a problem: In the options framework, options are
atomic macro-actions independent from each other.


# Ideas

Task compositionality - ideally the sub-policies should each be doing something different, or delegating to another sub-policy.

Does the manager need to give a reward to the sub-policy? When does it do that?

