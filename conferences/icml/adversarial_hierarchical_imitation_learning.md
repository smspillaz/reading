# Adversarial Option-Aware Hierarchical Imitation Learning


It has been a challenge to learning skills for an agent from long-horizon unannotated demonstrations. Existing approaches like Hierarchical Imitation Learning(HIL) are prone to compounding errors or suboptimal solutions. In this paper, we propose Option-GAIL, a novel method to learn skills at long horizon. The key idea of Option-GAIL is modeling the task hierarchy by options and train the policy via generative adversarial optimization. In particular, we propose an Expectation-Maximization(EM)-style algorithm: an E-step that samples the options of expert conditioned on the current learned policy, and an M-step that updates the low- and high-level policies of agent simultaneously to minimize the newly proposed option-occupancy measurement between the expert and the agent. We theoretically prove the convergence of the proposed algorithm. Experiments show that Option-GAIL outperforms other counterparts consistently across a variety of tasks.

[[jing_adversarial_option_aware_hierarchical_imitation_learning.pdf]]

https://icml.cc/virtual/2021/spotlight/8590

We want to learn from expert under a noisy environment.

Prior work:
 - Generative adversarial imitation learning method:
	 - Occupancy measurement matching problem: $p_{\pi}(s, a) = E_{\pi} [\sum_{t = 0} \gamma^t \mathbb{1}_{s_t = s, a_t = a}]$ where the distributions match if the policies are equal.
	 - GAIL: minimize the discrepancy of the occupancy measurement between the expert demo $\pi$ and the agent's self exploration $E$.
		 - $\min_{\pi} D_{KL} (p_{\pi}(s, a)||p_{E}(s, a))$
 - As the task becomes long, the efficiency of learning the entire sequence goes down
	 - Most long-horizon tasks have separable sub-tasks
	 - Imitation learning with unitary policy will be less efficient than with separate sub-policies for each sub-task.
	 - The combination of sub-tasks is various, learning a policy for scheduling sub-policies would be more data-efficient.
 - Idea: Use a mixture model instead of the unitary one on GAIL
	 - State-action pairs are clusterable



## Modelling
![[hierarchical_imitation_learning.png]]

Overall structure of the model:
 -some higher level policy $pi_{\mu}$ picks options, which in turn chose the lower level policy to use at the current timestep.
  - This is a switch-based hiearchical learning method - where you learn a different policy for different behaviours.


The option used by the expert is unobserved.

![[em_method_hierarchical_imitation_learning.png]]

Estimate the options using the EM-like method.

Effectively:
 - Take some expert trajectories
 - Take an initial policy
 - E-step: Infer expert options by estimating the options that have the maximum expert probability
 - M-step: With the currently estimated expert options, update the policy


Note that each expert trajectory is explained by a different option, we don't change options halfway through.

## Self-exploration

Without self-exploration, updating the policy with EM leads to hierarchical behaviour cloning and suffers from compounding errors.

We extend the occupancy measurement the "option-occupancy measurement", which requires matching both the high level policy and low level policy.