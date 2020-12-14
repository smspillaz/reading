# Offline Reinforcement Learning

Offline RL is about learning agent functions

 - action = f(history of observations)
 - you can learn this from supervised learning or by offline RL
 - if you have an agent function, you have a mech for any machine being able
   to generate actions.


In many environments, you can't interact a million times. We typically have
log data though. Whenever we have that, this is all that's needed to learn
an agent function.

Micking vs selected imitation:

 - Behavioural cloning: supefvised learning to map states to actions, requires good
   agents.
 - If you have bad demonstrations, you'll learn suboptimal behaviour.
 - Teacher that tells you how to do something, you may do a few things wrong
   but the teacher never grades you. You will never be better than the teacher.

 - Selective imitation: Train from suboptimal (off-task) data
 - Leverage value function to identify useful signals.


 - Example: Start position, reward
  - Behaviour cloning: $\max E[\log \pi(a|s)]$ max log likelihood of
    producing actions given the states
    - We would like to do better for this
  - Selective imitation - you have a teacher that grades you
    - Label actions as good or bad.
    - Learn to do the good actions, bad actions are negative examples.

Critic Regularized Regression:

 - Suppose we follow a trajectory, we have some policy $\pi$
 - We have the BC loss, but then also some "filtering"
   - indicator function: $Q(s, a) \ge Q(s, \pi(a|s))$
   - where the data (eg, the action proposed by the teacher)
     has more value than what the agent would have suggested,
     maximize the likelihood that we predict that action
   - where the data has less value than the action we would have
     gotten from the agent, don't learn to predict that action
     (eg, set the indicator to zero).

Networks in offline RL have to be as big as the ones that we have
in supervised learning - they have to learn purely from data.

Online vs Offline RL:

 - Online RL has to explore the data as much as possible to gain knowledge
   quickly
 - Offline RL agents must exploit the data as much as possible. Better to
   be risk-averse.

   - If you go outside the data you're relying on extrapolation which may be wrong.


Extrapolation of offline data - dealing with extrapolation errors:

 - We're taking the max over the Q function - choosing the max from the extrapolation,
   this is likely to pick points that make us overconfident.
 - One solution is to just drop the max - closer to SARSA
   - at test time you still have to pick the best action!
 - Ranking regularization: Assign lower values to state-action pairs that have not
   been observed.
   - Minimize the cost and make the value lower.
   - Idea being that the q-function for actions that we haven't yet seen will
     be zero by default?
 - If you do offline RL with SARSA you can already do pretty wel.

Bellman equations are confounded regression problems:

 - You can think of it as a regression problem
 - We're trying to fit an r-function to Q - (r + gamma max future Q
   - We're doing nonlinear least-squares regression
   - We can't solve the expectation, so we sample from it.
 - But unlike standard regression, the noise affects the inputs and outputs - confounders!
 - If you just do normal fitting, you will get a wrong solution.
   - Move the confounded input into the target - the input should not depend on the
     future state
   - but now you need to maintain a target network with fixed parameters.


Hyperparameter selection:
 - Lets say you learn many policies given hyperparameters
 - How do you pick the one that works best?

   - Need to do off-policy evaluation and validation set
   - Fitted Q-iterations

Data-driven robotics:

 - What if you store all the data that all robots ever gathered
 - Collect data via demonstrations - annotate some of it with rewards
   - which ones were successful
   - learn the reward function

Learning reward functions with little supervision:

 - If we have humans in the loop, its important to learn from as few data as possible
 - Contrastive learning
   - label only a subset then use contrastive learning to learn reward functions
     and propagate labels.
 - Multi-instance learning
   - if you have reward-labels at the group, how do you infer individual labels
 - Semi-supervised learning

Challenges:
 - More real applications (language, safety, efficiency)
 - Promote philosophy of saving and sharing data
   - Need to store the data somewhere!
 - Offline RL enables richer simulation (simulator only needed for evaluation)
 - Improve off-policy evaluation
 - Combine off-line RL with on-line RL ideas
 - Scale the NNs
 - Should be sufficient to solve many tasks from one training session.

# Addressing Distribution Shift in Online RL with Offline Datasets

 - It is desirable to do fine-tuning online: domain shift
 - Leverage samples in the offline dataset as well as online ones
   - this is a nontrivial challenge due to distribution shift
   - harmful effects on finetuning - finetuned agent works worse than initial policy
   - bootstrap error - inaccurate targert Q

Balanced Replay with Ensemble Distillation (BRED):

 - Early fine-tuning stage (mix of both online and offline samples)
   - Stabilizes Q-learning

 - Later fine-tuning stage
   - Learn from more near-on-policy samples (faster-fine-tuning)


 - Ensemble distillation:

  - Ensemble of offline RL agents
  - Distil into a single policy (reduces variance)
  - Fine-tune the distilled policy with Q-ensemble
    - the individual Q-function may be inaccurate: Q-ensemble much more robust
    - essentially: Find the parameterization of the policy that maximizes
      all the Q functions that you have in your ensemble.

Take-awasy:

 - Fine-tuning better than training from scratch
   - Starting from decent policy hence safer
 - Balanced Replay necessary for safe fine-tuning
 - Don't need to do behaviour modelling
 - Mixing offline and online samples important, otherwise learning is slow or unstable


# Addressing Extrapolation Error in Deep Offline RL

 - Novel three-part solution for offline RL
 - Ablations
 - Two-new datasets

Challenge: Data convergence

 - You only cover a subset of the MDP - even if you collect millions of frames
   its not enough!
 - Extrapolation of Q-values is difficult!

Three components:

 - Use behavioural data in Q updates (instead of greedy actions)
 - Ranking regularization
   - Rank the actions in the dataset higher than the actions not in the dataset
     for a given state
     (how does this scale?)
   - You don't need to train a separate behaviour model
 - Reparameterization of the critic: Stabilize training, constrain outputs
   of Q-network to finite values
