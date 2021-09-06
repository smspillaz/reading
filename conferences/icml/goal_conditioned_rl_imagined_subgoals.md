# Goal conditioned RL with Imagined Subgoals

 Goal-conditioned reinforcement learning endows an agent with a large variety of skills, but it often struggles to solve tasks that require more temporally extended reasoning. In this work, we propose to incorporate imagined subgoals into policy learning to facilitate learning of complex tasks. Imagined subgoals are predicted by a separate high-level policy, which is trained simultaneously with the policy and its critic. This high-level policy predicts intermediate states halfway to the goal using the value function as a reachability metric. We don’t require the policy to reach these subgoals explicitly. Instead, we use them to define a prior policy, and incorporate this prior into a KL-constrained policy iteration scheme to speed up and regularize learning. Imagined subgoals are used during policy learning, but not during test time, where we only apply the learned policy. We evaluate our approach on complex robotic navigation and manipulation tasks and show that it outperforms existing methods by a large margin.
 
 [[chane-sane_goal_conditioned_rl_imagined_subgoals.pdf]]
 
 https://icml.cc/virtual/2021/spotlight/10148
 
 Exploit modularity by predicting subgoals. Hierarchical approaches rely on temporal design choices.
 
 Use subgoals to improve training.
 
 The subgoals are never actively pursued, they are only there during policy search.
 
 Train higher-level policy operating in the state space. Sample subgoals halfway to the goal.
 
 Use goal-conditioned value function as a distance estimate between states.
 
 ## Training
 
 Advantage-weighted high-level policy improvement
 
 $$
 \pi^{H}_{\psi_{k + 1}} = \arg \max_{\psi} E_{(s, g) \sim D, s_g \sim D} [\log \pi^H_{\psi} (s_g|s, g) \frac{1}{Z(s, g)} \exp{\frac{1}{\lambda} A^{\pi^H_k}}(s_g|s, g)]
 $$
 
 Sample subgoal candidates from replay buffer $D$.
 
 Maximize the log-likelihood $\log \pi^H_{\psi} (s_g|s, g)$  reweighted by their corresponding advantage $\frac{1}{Z(s, g)} \exp{\frac{1}{\lambda} A^{\pi^H_k}}(s_g|s, g)$.
 
 ## Incorporate subgoals
 
 Introduce a prior policy.
 
 In addition to maximizing the Q function, we encourage the policy to stay close to the prior policy:
 
 $$
 \pi_{\theta_{k + 1}} = \arg \max_{\theta} E_{(s, g) \in D} E_{a \in \pi_{\theta}(.|s, g)} [Q^{\pi}(s, a, g) - \alpha(D_{KL})(\pi_{\theta}(.|s, g)||\pi^{\text{prior}}(.|s, g))]
 $$
 
Evaluate this on four maze navigation tasks where you control the ant. Agents are trained to reach any goal. Standard goal conditioned RL approaches can learn to reach goals, but you don't need to rely on subgoals on inference time .