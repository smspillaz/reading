# Deep Reinforcement Learning Workshop

## Machines that invent their own problems

Child development - they explore the environment, they are driven
by intrinsic motivation, curiousity. Invent and pursue your own
problems.

Different forms of intrinsic motivation:
 - Knowledge based (generate intrinsic rewards upon visiting some staets)
   - inforamtion gain
   - uncertainty
   - prediction experiments

 - Competence-based intrinsic motivation
   - Imagine goals that you want to reach in the future
   - Reach self-generated goals
   - Decide which goal achievements you want to make
   - Discover repotoires of skills, skills parameterized by what you want to solve


This talk is about the second one.

Kids imagine very diverse kinds of problems and goals.
 - Concrete: grounded in the real world
 - Abstract: grounded in games
 - Mix of concrete and abstrac

Formalizing generalized goals in RL:
 - You need some kind of map of the space of goals
 - Need to embed the goals - how do you learn such an embedding?
   - You have to associate meaning to these goals - you need to
     self-evalaute how good you are at solving your goal
 - How to learn such a function
  - Use the goal-achivement function as self-supervsion

Intrinsically motivated goal-exploration farmework:
 - Observe the context
 - Sample a goal
 - Rollout the goal conditioned policy
 - Observe the outcome and update models

   - Some are population-based
   - Goal-condtition reinforcement learning
   - Some use learned or hand-defined goal embeddings

Importance of goal-sampling strategies and structured goal representations
 - Hand-defined embeddigns and goal-achievement functions
 - Its hard to learn some things because some goals are unachiveable
 - You need disentangled goal representations and curriculum learning
   for goals that are not too difficult
 - Modular representation of goals
   - Goal types
   - Goal values
   - Move Q(3) to position (x, y) while ignoring everything else in the scene.

 - Atuomatic curriculum learning:
   - problem: catastrotophic forgetting
 

Learning a goal-embedding space

 - Eg, from raw images
   - Train a generative model to learn an embedding of images and then
     sample from that embedding
   - Enables much more autonomy, but these systems are not yet robust to
     environments with distractors.
 - Robustness to distractors
   - MUGL: Use beta-VAE to learn disentangled embeddings, then clustering
     a group of dimensions

Learning goal-achivement functions:
 - Learning action distatnce
 - Similar images are not always a good sign that a goal is reachable
 - Predict the number of actions that need to be taken
 - Does not generalize to OOD goals

Learning diverse goal embeddings:
 - Meta-diversity search
 - Diversity-driven search in a single goal embedding space is a single
   way to represent all goals
   - need a diverse represetnation for diverse kinds of goals
 - Meta-diversity search:
   - Incrementally learn a diverse set of goal embeddings in an outer loop
     then search to achieve them in an inner loop
   - IMGEP-HOLMES - learn a hierarchy of diverse goal embeddings
     - start with a single VAE that is incrementally trained on the data
     - when reconstruction loss reaches a plateau, split and instantiate
       two new embeddigns
     - each new observation falls into one of the new embedding space
    - hierarhcy of goals - first sample a goal embeddings, then
      sample a goal from it.
    - prioritize exploration in areas that you don't know very much about.


Using language for power creatig exploration

 - Toward OOD and abstract goal generation
 - When using generative models to sampel goals, they're goals that you know about
 - Agents need to generate novel abstract goals - goals that are OOD of teh
   things that you have already seen

 - Language is compositional by nature - push the limits of the known to new frontiers
   - cat + bus = catbus

IMAGINE:
 - https://arxiv.org/abs/2002.09253
 - Language goal imagination for RL agents
 - Guided exploration with a social partner - "You grow the blue algae"
    - The social partner tells the agent what they did
 - Creative autonomous exploration - imagine new goals and train autonomously
   with language composition learned in the first phase.
 - Agent initailly tries random things - the social peer provides a description
   - the agent learns the mearning of these descriptions
   - meaning of sentences encoded in two ways:
     - goal achievement function
     - goal achievement function is used as a form of self-superversion
     - hindsight learning.
        - the social peer does not always provide a full description
 - The agent can now invent new OOD to form new sentences and
   model their achivement and train the policy to achieve these goals

 (1) How to imagine new sentences that are useful

   - model construction grammar framework

 (2) How can the goal achievement function generalize to out of distribution goals

   - Deep sets + affordance centered representation + attention

 - Test on test goals from a test set on goals never uttered by the peer

Open challenges
 - neural architectures
 - the use of time-extended goals
 - hierarchical skill collectiosn - re-using self-invented goals as
   macro-actions in higher level MDP
 - memory architectures


# Learning Functionally Decomposed Hierarchies for Continuous Control Tasks

Humans intuitively adapt path plans - eg, if you have acquired skills such
as navigating around, you can adapt this planning skills.

For RL - often overit to training. Hard to solve unseen test acses.

## HiDe

 - Explicit separatation of the state spaces allows for more efficient training
 - RL-based planners for efficient subgoal creation
   - solve longer horizon tasks
   - transfer across agents and domains

## Goal Conditioned HRL
 - Sparse rewards for training
 - Higher layers get fewer signals from training from the lower l;aywers
 - Problems become very hard to solve.
 - Nonstationarities introduced by the changing policies

## HiRO

 - Off-policy corrections dueing training to deal with nonstationarity

## HiRO-LR
 - Latent space representation of the state space
 - Learn from images

## HAC

 - 3-layered hierarchy
 - sparse reward, utilizes hindsight techniques

## HiDE

 - 2-layer HRL
 - Explicit task decomposition by explicitly separating the state
   spaces in each layer
 - Different layers have different state spaces 
 - Allow for different control agents ot be transferred across hierarchies
 - Planning in 2D and in 3D
   - Receives information for planning then provides subgoal

 - Planner input: Global information (position in space, final goal
   - MVProp: Based on value iteration and CNNs - produces a global value map
     - can't produce reasonable subgoals yet

     - attention mechanism: create a local value map around the agent
       gaussian distribution with covariance matrix parameterized by a CNN
     - agent-relative subgoals passed to the lower layer
     - we can better adapt to obstacles such as corners

 - Control layer: Learn how to reach the planner's subgoals
   - This is responsible for the low-level control to achieve the subgoals from the planner
   - Learn to blindly follow the planner
   - Control layers joined with relative subgoals which are important for generalization
     and scaling
   - Train the control layer with DDPG
   - Hindsight technqiues to deal with nonstationarity

 - Tested on control tasks.
   - Navigation:
     - Train ant in 3D environment with sparse rewards
     - You can solve the training task
     - If you flip the layout, SOTA approaches overfit, HiDe generalizes nicely.
       - attention mask learns reachable sequence - avoid obstacles such as corners.
   - Even possible to transfer across agents.
     - Attach the planner of the goal-setting agent to the controller of the humanoid.
   - Even possible to transfer across domains.


Directions for future work:
 - Occlusions
 - Multiagent

# Accelerating Reinforcement leanring with Learned Skill Priors (SPIRL)

https://clvrai.github.io/spirl/

When navigating we're using skills - infeasible to explore all of them on
a task. We have a good prior on which skills to explore.

 - We're using a lot of our prior experience navigating different buildings
 (1) Temporally coherent behaviours (skills)
 (2) Prior over which skills are meaningful to execute in a given situation


Assume access to a large offline dataset

 - Extract re-usable skills 
 - Learn a prior - which skills are the ones that I should export.
 - Efficient RL on new tasks.

Meta-RL: learns transferrable priors, require training task distribution and online meta-training

OfflineRL: Requires annotation with target rewards
  - need to re-annotate every time you have to learn a new task.


Skill-Transfer:
 - Needs no subtask reward annotation
 - Does not require training task distribution
 - Scaleable data collection and use of available data


What prior are we learning?
 - Eg, sample a skill from repotoire
   - Learn a distribution that captures only the skills that are actually meaningful


How to learn it?
 - sub-trajectory
 - takes the action trajectory
 - encodes it
 - decodes it back into the trajectory
   - regularize the embeddings towards a fixed prior

 - skill posterior: we learn to model this
   - also learn the prior which captures the distribution

Once we have learned this distribution, we can leverage it downstream.

 - Use the pre-trained skill prior to regularize the skills
 - Only explore the skills that are meaningful

Maximum entropy RL:

 - Adds entropy term to RL objective
   - rewrite min divergence between uniform action prior
   - for the skill space - explore all the skills

This approach

 - Similar to max entropy
 - Minimize divergence between learned skill prior.
 - Explore skills that are meaningful
 - Don't explore skills that are pointless.


Use soft-actor-critic (SAC) - modify a few update equations to incorporate
the divergence cost between learned skill prior.


You can also learn effective skill priors from substantially suboptimal training data

# Asymmetric Self-Play for Automatic Goal Discovery

# Planning from Pixels using Inverse Dynamics Models

https://arxiv.org/abs/2012.02419

Learning world models that are accurate enough planning is hard.

Its hard to make accurate predictions over a long time horizon is harder
over time because error accumulate. Also there are some aspects that essentially
look random (nonstationarity).

 - But those random things may or may not affect you in any way
 - L2 losses will focus more on mdoelling the things that don't matter.
 - Can we train it to contain only task-relevant information? Eg, muZero.
   - But then this compromises your ability to generalize to new tasks.

GLAMOR:

 - Learn a representation that tracks only the controllable aspects of the environment
 - Goal Condioned Latent Action Models for RL
   - Rather than prediction observations
   - Model the distribution of action that are necesasry to travel between states
   - Does well on visual goal-achievement tasks.

Multi-task setting: Distribution over tasks - task affects what you're rewarded for
 - Tasks are goal states.

Optimal plan: Maximize your expected discounted future reward. Probability that
you reach the state $G$ times the discount (exponential decay). You just need to
predict the probability that we reach the goal.

 - Make a latent world model that predicts the probability at each step
   that you're at a goal state
 - But finding an action sequence that actually lands the agent at a goal
   state is hard, because of sparsity

 - Can we do something smarter?
  - Bayes Rule: Model the evnrionment using the inverse dynamics and action prior:

   $a^*_1,...,a^*_{k - 1} = \arg \max_{a_1, ..., a_{k - 1}} \gamma^k \frac{p(a_1, ..., a_k|s_1,s_k=g)}{p(a_1, ..., a_{k - 1}|s_1)}$

  - Action prior - which action sequences are more likely to show up on our
    training sequences
  - We can model this autoregressively
  - Parameterize these features using a ResNet and predict using an LSTM.


  - Open-loop plan once at the beginning of each episode
   - Re-plan at each step.


  - Can we get away with only using the first model (inverse dynamics)?
    - think of it like image captioning
    - probability of a particular action sequence given a state and goal
      is dependent on the probability of reaching that goal and the probability
      that the action sequence is tried by the agent in the first place
    - a sequence of actions that has a high probability of reaching the goal may
      only have such a probability because the agent tried it more times during training
    - action proor disentangles the probability of reachign the goal from the prior
      probability of the action sequence showing up in the training distribution

GLAMOR is quite sample efficient.

How well can the planner find optimal solutions?
 - As the number of samples increases, the agent achieves more goals in
   few steps - by increasing the amount of compute used during planning - you
   achieve more goals and go to the goal with the shortest path.
 - GLAMOR has a mechanism for determining when it has reached its goal, baselines
   evaluated after a fixed number of steps.
 - GLAMOR's world more knows many different paths to the goal and the best
   one to get there.

# Grounded Simulation Learning for Sim2Real with Connections to Off-Policy RL

Teamwork - we have to decompose the task. You have to first teach the robot how to
do stable skills.

Sim2Real: Bridging the reality gap. Grounded simulation learning (GAT).

 - Some ideas: Add noise to environment, robustness
 - Take some real data and try to use that to improve the simulator.
 - We're probably never going to be able to make a perfect simulator. Try to
   make the simulated environment closer to the real environment

Grounded simulation learning:
 - (1) Real world policy execution
 - (2) Simulator grounding (key part of the method)
 - (3) Policy improvement (reinforcement learning done here!)
   - Collect more data in the real world

In principle, your simulated environment could be null to start with and the
grounding builds up the simulator.

Treat the simulator like a black box. Learn a wrapper around that transforms the
actions that come out of your policy into transformed actions such that the transformed
actions have the same behaviour in the simulated environment as they would in the real
one.

 - Learn $g(s_t, a_t)$ - "action transform function for this simulator"
 - What should we replace the simulation command with such that it goes to the
   same place in the real world?
 - We have an "inverse" dynamics model - what action generates the transition.


We learn these funcitons through a DNN.

 - Forward model: Trained with 15 real world trajectories of 2000 timesteps
 - Inverse model: trained with 50 simulated trajectories of 1000 timesteps


Off-policy policy evaluation:

 - $v(\pi) = E[\umR_t|H \sim \pi]$
 - Given a target policy and data generated from a behaviourpolicy, estimate $v(\pi)$
  - Metric: MSE between true value and estimated value
  - Importance sampling: re-weigt reward totals for each trajectory in the observed
    data. Re-weight by the relative likelihood and average the reward totals.

  Myth 1: The target policy is the optimal choice of behaviour policy to collect data
  for important sampling (eg, if you can, get data from the policy that you're trying to
  to evaluate)
    - Running a behaviour policy different from the target policy can minimize the
      variance of importance sampling estimates
    - Algorithm that gives you a lower variance

    - Importance sampling can achieve zero MSE with a single trajectory.
       - why? If you had an oracle which allows you to pick a policy, then you
         can weights such that no matter which action you pick, you get the optimal value

       - In the real world, you need to know what the value of the policy was to
         begin with. But you can adapt the behaviour policy toward the optimal
         behaviour policy

       - At iteration i, choose a behaviour policy, collect trajectories and
         estimate the value using the observed data
         - Adapt the behaviour policy parameters with gradient descent is
         - Cannot estimate the MSe, but you can estimate the gradient!
         - MSE is unbiased estimator of the variance


    - Behaviour Policy Gradient Theorem
       - Assume that the BP is differentable wrt theta
       - BP can represent evaluation policy
       - Then the graient of the MSE of the importance sampling is
         the expected value of the negative log action probability times
         the IS squared.

    - This BPG almost always leads to faster evaluation

   Myth 2: True behaviour policy should be used to compute the denominator of importance
   weights

    - But replacing the behaviour policy with an estimate of a policy that generated the
      data reduces the variance of the importance sampling estimator
    - Regression importance sampling - use the data to estimate the behaviour policy
      and use that estimate. This leads to faster convergence and lower errors.
    - When you have a batch of data, estimate what the policy was that generated that
      data. Replace the behaviour policy with an empirical estimate of it.


In RL we want to generate trajectores that are similar, not just actions.

 - Action transformer can be throught of as an RL function. The agent is
   the action transformer - generates new actions in order to get good trajectories.

An imitation from observation approach to sim-to-real transfer.
