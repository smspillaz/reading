# Learning to Explore from data

https://neurips.cc/virtual/2021/workshop/21874

The Deep RL promise: exploration from scartch.

Its too slow.

## How can we use data to improve exploration?

 - Goal location is unknonw
 - Data from agents trained to reach different goals
 - Learn the distribution of goals and how to reach particular goals
 - When get a new tasks, sample a goal from that distribution, go there, if not there, update.
 - This is called *thompson sampling*
 - This is PEARL.


Is this the best exploration that we can learn here?

 - Walk along the half-circle until you find the goal and only then go to it.
 - Can we learn this better strategy from the same data?
 - Seems more difficult since this behaviour is quite different.


Fundamental questions:
1. Can we learn optimal explroation from offline data
2. How to collect effective data
3. How much data do we need?

Motivation:
 - Exploring from scratch is too hard / dangerous
 - Collecting offline data is safe
 - Task is a general concept


What is optimal exploration?
- No prior information
	- The best thing we can do is guarantee that we don't waste time on things that are not interesting
	- UCRL
	- Regret bounds, PAC bounds etc.
- Prior over MDP
	- Bayesian RL
	- "Plan to obtain information/reward"
	- Well-defined optimal exploration



In Bayesian RL:
 - Distribution over possible MDPs
 - We want to maximize our expected reward where our expectation comes from our MDP and we have an outer-expectation over all MDPs
 - POMDP: We don't know what MDP we're in, but we need to keep track of observation history to make a guess as to what MDP we're in.
 - Deep Bayesian RL
	 - Basically we do variational inference with an RNN.
	 - Map from history to approximate belief. Gaussian over latent variable.
	 - With this approximate belief, combine it with the state and plan in the belief space.


Can we learn beliefs offline? In principle if you just run the same algorithm for training the RNN, does it work well? Doesn't work. Identifiability prolem. MDP ambiguituity. Each agent in the data can visit different parts of the state space. Is it two different MDPs or one MDP with rewards at both locations.

Data identifaibility: No single MDP and two arbitrary policies cna induce both $p_i$ and $p_j$.

If we know that all the MDPs can only have a reward at a single location, not a problem. Hard to inject this into a neural net.

Sufficient to guarantee that every two MDPs 