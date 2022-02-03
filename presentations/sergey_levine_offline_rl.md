Why do we need machine learning anyway? To produce adaptable and complex decisions.

What is a *decision*: The decision is about what to do after you make a judgement. If you tag a user in a photo, you're making a decision about something that will affect your environment.

Supervised learning is made easier by the fact that current outputs don't influence future observations. Decision making problems are tricky because optimal actions are not provided. 

Why aren't we all using RL?

Problem, its a framework for decisionmaking:

1. Map inpust to actions and those actions influence future inputs. Almost all real-world learning problems look like this.
2. Online learning setting for control. 


Supervised systems generalize world. Generalization with an online active learning framework, you'd need an imagenet sized dataset per step. Not ideal.

Can we make RL look more like supervised learning?

Distill the best policy you can. You don't copy what was done in the data, you use the data of evidence of how the world works.

## Offline RL workflow
1. Collect a dataset using any policy. Done once
2. Run offline RL on this dataset to learn a policy
3. Don't collect new data, but re-use the same data and modify the algorithm.

### Off-policy algorithms

You don't need on-policy data to make the LHS equal to the RHS.


1. Collect dataset using some policy and add it to $\mathcal{B}$.
	1. Sample minibatches from $\mathcal{B}
	2. Minimize squared difference between Q function and r + Q(s', a')


QTOpt: Offline learning with online finetuning. Large scale offline + online training could enable generalization in the real world.

How does the purely offline version compare to a version with online finetuning? Additional finetuning data was negligible.

Failure rate is 3x larger.

Why is offline RL hard?

 - Fundamental problem: Counterfactual queries required.
 - Training data is good data. You don't know what happens if you do something stupid. Online algorithms try it and die. Offline RL must figure out if the dataset is sufficient for us to take this into account. But you still must be better than the best thing in the data!

How does this problem show up in practice?

 - Collect and offline dataset for half-cheetah. Looks like overfitting.
 - Q funciton is an estimate of expected reward. How well do you think you are doing?
 - Massive overestimation? Why is that?
	- Distribution shift: When we minimize the squared error on target values we're doing ERM
	- Given $x^*$ is $f_{\theta}(x^*)$ correct?
		- Under training distribution, maybe, we minimize the error on average
		- Under testing, this will be bad, adversarial examples

How does this happen in $Q$ learning?

 - $Q(s, a) = r(s, a) + E_{s' \sim \pi_{\text{new}}} (Q(s', '))$'))
 - The objective is $\min Q$ under a distribution of $\pi_{\beta}$ (which collected the data.). When $\pi_{\beta} = \pi_{\text{new}}$. But we want $\pi_{\text{new}} \ne \pi_{\beta}$! We pick $\pi_{\text{new}}$ to be the max of the Q function.


To solve distribution shift, we could add a KL penalty to $\pi_{\text{new}} || \pi_{\beta}$. . First issue: we don't know what $\pi_{\beta}$ is. This is both too pesimmistic and not pessimistic enough.

 * Eg, if $\pi_{\beta}$ is random, then you're basically asking to be random
 * A small KL divergence from  $\pi_{\beta}$  does not guarantee that you do not suffer distributional shift.


Two principles:

1. Don't evaluate actions that are not the dataset.\
2. Train the Q function so that OOD actions never have high values. Find the erroneous peaks and push them down. Penalize non-indistrubiton actions that are not the max.



### Advantage-weighted actor-critic


Imagine a basic AC algorithm. 

What if we do "weighted" regression?

$\pi_{\text{new}(a|s)} = \arg \max E_{(s, a) \sim \pi_{\beta}}[\log \pi(a|s) w(s, a)]$

If we choose our weights to be be proportional to the exponential of the Q function, then this solves the constraint of KL divergence. This is not a sufficient principle for a fully offline RL method.

Works well with offline RL with online finetuning.

[[awac_accelerating_online_reinforcement_learning_with_offline_datasets]]

## Can we also avoid all OOD actions in the Q update?

$Q(s, a) = r(s, a) + E_{a \sim \pi_{\text{new}}}(Q(s, a))$

This is $V = \arg \min_{V} = \frac{1}{N} \sum^N l(V(s_i), Q(s_i, a_i))$

But the actions come from $\pi_{\beta}$ not from $\pi_{\text{new}}$.

As long as the value function generalizes a little bit we have a distribution of possible values that you might get given a state. Multple nearby states with a nearby action. If you use the MSE loss, then you get the expected value of this distribution.

Expectile regression: Modify the loss function such that the positive branch has a greater weight. Penalize positive errors less than negative values. If you choose $\tau$ appropriate, then the value function regresses to the $\max$ of Q and not the expected value. We can do regression using only the actions in the dataset. We just change the loss function and you get the effect of a max.


### Implicit Q-Learning

$Q(s, a) = r(s, a) + V(s')$

$V = \arg \min_V = \frac{1}{N} \sum^N l^{\tau}_2(V(s_i), Q(s_i, a_i))$

In practice the method never queries the q function for actions not in the dataset. When we're done we can extract the policy using the same weighted max likleihood policy.

By changing $\tau$ you change the asymmetry between the ovestimation penalty and the underestimation penalty.

[[offline_reinforcement_learning_with_implicit_q_learning]]

## Option 2: Train the Q function to avoid OOD errors

[[conservative_q_learning_offline_rl]]

$\mu$ is an adversarial distribution that tries to find large Q values and pushes them down. 

A better bound: Push up the Q values in the data.


## How should we evaluate offline RL methods?

Bad intuition: Imitation learning

Better intuition: Order from chaos. Stiching.

### Vivid Example

Grasping. If you include all the data, then you figure out how to put together the right pieces. Open the drawer and then pick up the object.

[[cog_connecting_new_skills_to_past_experience_with_offline_reinforcement_learning|COG: Connecting New Skills to Past Experience with Offline Reinfrocement Learning]]

Offline RL can do things that imitation learning can't. The dataset really needs to require *offline RL* and not just *behaviour cloning*.

MT-Opt: Could we learn the tasks without rewards using goal-conditioned RL. Train to reach those goal images. Sort of like BERT-for-robots. 

See also:

 - BADGR

## Model-based RL

- COMBO: A model-based version of CQL


## Open Problems

1. Workflow
2. Statistical guarantees
3. Scaleable methods


