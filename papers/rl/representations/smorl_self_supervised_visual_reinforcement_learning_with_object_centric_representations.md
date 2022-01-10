# Self Supervised Visual Reinforcement Learning with Object-Centric Representations

https://iclr.cc/virtual/2021/spotlight/3422

Autonomous Learning has several challenges - learning is self-supervised. Observations are high-dimensional, tasks and observations are compositional.

How can we enable a robot to autonomous learn in such environments.

Prior work: self-supervised RL: Goal images, observation needs to manipulate its environment such that the environment is as close to the goal as possible.

Prior work: Use latent space, use distance in latent space as reward signal. Harder for complex tasks where objects are involved.

Problem: Binding problem. Even if you successfully represent many objects in one representation, hard to represent combinations if both are there.

Some dimensions encode task-irrelevant information, but they're needed for reconstruction.

![[scalor_object_centric_representations_disentangled.png]]

Object-centric representations provide better goals. Observations and represented as a set of low-dimensional vectors. Each object representaitons can be additionaly structured. Disentangling location and appearance methods.

SMORL (Self-Supervised Multi-Object RL)

We design a novel goal-condtioned attention policy compatible with object-centric representations.

Propose an efficient self-supervised training mechanism that explores additional structure in the latent space.

We encode the observation and goal. We pick a subgoal $z_g$ from the set of possible sub-goals and provide that as an input to the goal-conditioned attention policy. Then solve for all the sub-goals.

Now as our input to the policy is a varying length-set, we have an attention-based policy. Based on multi-head attention policy where queries depend only on sub-goals and keys and values are based on the input set. This is compatible with variable-size input sets $Z$. Attends to elements that are important for sub-goal.

Training SMORL:

First we need to provide a feasible goals

Provide goal-dependent roal function.

Train as usual goal-conditioned RL agent.

Goal Generation:
 - Use first observations:
	 - $p(z^{\text{where}}|z^{\text{what}})$ to observed data to estimate valid location
	 - Pick random object representation
	 - Sample new $z^{\text{where}}$ from $p$ given $z^{\text{what}}$
 - Reward function for each timestep:
	 - Find most similar object: $k = \arg \min_i ||z^{\text{what}} - z^{\text{what}}_g||$
	 - Reward in a subsapce of locations: $-||z^{\text{where}}_k - z^{\text{where}}_g||$
 
 SMORL training combines SAC with object-centric representaitons.
 
 Tested the object in several multi-object environments of `multiworld` environment.

Environment has dense reward.