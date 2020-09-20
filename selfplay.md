# Learning Goal Embeddings via Self-Play for Hierarchical Reinforcement Learning

Basic Idea: Automatically learn a good representation of sub-goals in the environment and a
low-level policy that can execute them.

Automatically learn a good representation of sub-goals in the environment and a low-level policy that can
execute them.

What is the challenges:

 (1) Space should be general enough to cover the full range of sub-tasks within the environment
 (2) Task-irrelevant details of the environment should be abstracted away
 (3) You should enocde sub-goals achievable by the low-level poicy (correct level of difficulty).

Use unsupervised asymmetric self-play as a pre-training phase for low-level policy.

Adversarial reward structure forces the agent to come up with new tasks, ensuring a diverse
goal representation. Time limit imposed on each task which limits complexity and good
convergence of goals to a given difficulty.

Parameterization of the low-level policy, input: current state and goal vector.

"Unsupervised Learning of goal spaces for intrinsically motivated goal exploration": Use an autoencoder of
the state space to discover what the goals are. Use a goal-discovery algorithm on top of the learned rerpesentation.

This work: Use an intrinsic motivation approach. Learn both a low-level actor and representation
of the state space at the same time, but left goal discovery in the manager to a future work.

So in self-play, we have two agents, alice and bob. Alice is bob's manager.

 (1) Alice and Bob are randomly initialized. Alice takes a step in the environment using $\pi_A$. This
then becomes Bob's goal.

 (2) Reset the goal back to $s_0$ and Bob takes control, following actions according to $\pi_B$. You succeed
     if you're close to alice after $T_B$ steps.

Bob's reward 1 if success, 0 if fail. Alice' reward is 1 if bob fails, 0 if bob succeeds. So the idea is that
Alice sets goals that Bob will likely fail at.

 - Problem: Bob only does tasks that can be solved in $T_A$ steps, meaning that some states are unreachable.
   to solve this problem, perform several self-play games within the same episode. So, eg, if bob
   is successful, then you continue with another self-play game at the current state.

Bob's loss function $L_B = E_{a^B_1 \sim \pi_B] [-R_B] + \alpha E_{a_t}^A \sim \pi_A [\log (\pi_B (a_t^A|s_t^A)]$

So basically, we take the expected reward for action $a$ (which is negative $R_B$) times the $\alpha$ weighted
negative log probability of taking action $a$.

Reward function for Alice: Add entropy regularization to encourage her to propose diverse tasks.

See also: "Intrinsic Motiviation and Automatic Curricula via Asymmetric Self-Play"

This paper is different in the following ways:

 (1) Number of steps taken by Alice and Bob are fixed, which constrains the scope of work done by the low-level policy
 (2) Episodes are broken into multiple shorter segments with the environment reset to the beginning of the segment.
 (3) No reward for Bob based on time
 (4) Bob's architecture

Architecture of the Bob agent:

 - first need to encode the current and goal states into a compressed embedding
 - two forms of goal encoder:
   - one based on taking the difference
   - one based on the absolute representation

Then, you have a policy conditioned on the goal embedding only

## How to train "charlie" (the manager)

Charlie operates on a different timescale, since charlie chooses a goal and then lets Bob execute for $T$ timesteps.

Use the external reward to train charlie. In this case $T_C = T_A$.

## Experiments

Grid-world like scenario - MazeBase. Observation is MapWidth x MapHeight x VocabSize

Comparing hierarhical self-play to self-play,, you get pretty good sample efficiency. You get to a high
expected reward within about 10M steps as opposed to 70M steps required for REINFORCE baseline
and 40M steps required for self-play.

The learned embeddings also appear to be quite nicely linearly separable depending on what the
expected staet of the world is (eg, door locked embedding is visually below
the door unlocked embedding).

The plots don't include the pre-training steps, so presumably, you've done enough pre-training
on self-play before you then train "charlie" (the manager). Its not clear how much pre-training is actually
done in this case.


## Limitations

The choice of distance function to the goal to determine if self-play was successful or not requires
some domain knowledge. Easy in the case of ant, harder in the case of MazeBase.
