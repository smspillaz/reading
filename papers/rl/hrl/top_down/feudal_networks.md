---
title: FeUdal Networks for Hierarchical Reinforcement Learning.
venue: ICML
pages: 3540-3549
year: 2017
type: Conference and Workshop Papers
access: open
key: conf/icml/VezhnevetsOSHJS17
ee: http://proceedings.mlr.press/v70/vezhnevets17a.html
url: https://dblp.org/rec/conf/icml/VezhnevetsOSHJS17
authors: ["Alexander Sasha Vezhnevets", "Simon Osindero", "Tom Schaul", "Nicolas Heess", "Max Jaderberg", "David Silver", "Koray Kavukcuoglu"]
sync_version: 3
cite_key: conf/icml/VezhnevetsOSHJS17
---
# Feudal Networks

Modular Neural Network consisting of a worker and a manger.

Worker produces actions conditioned on external observation, its own
state and the goal of the manager. The Manager's goals
are trained using an approximate transition policy graident. Manager operates
at a lower temporal resolution than the worker.

Goals from the manager are average-pooled over the last few timesteps,
so the transition from one goal to the next is smooth.


Contributions:

 (1) Consistent, end-to-end differentiable model that embedies the general principles of FRL
 (2) Novel "transition policy gradient upgrade" for training the Manager, exploiting the
     semantic meaning of the goals that it produces
 (3) The use of goals that are directional rather than absolute
 (4) Novel RNN design for the manager (dilated LSTM)

Ablation study shows that transitional policy gradients and directional goals
are required to really make it work.

The work builds on Tessler et al (2016) which showed that if you defined some sub-routines
and then did RL over that, you can make things work, even if sub-goal discovery not defined.

Problem with options framework: They tend to dengenerate into one of two trivial solutions

 * (1) only one active option that solves the whole task
 * (2) a policy over options that changes options at each step and micro-manages

 - solution for these problems is regularization where you prefer options that run for some time.


## Training

Train the goals and workers independently - the manager
predicts advantageous directions in the state space,
then we reward the worker to follow those directions.

$\triangledown g_{t} = (R_t - V_t^M(x_t, \theta)) \text{cos}(s_{t + c} - s_t, g_t(\theta))$

Basic idea: Advantage function for manager times the cosine distance
between the state and the goal embedding


### Model Formulation

From the inputs, $x_t$ produce $z_t$.

This gets sent to the manager who produces a goal $g_t$ by taking a step on an RNN.

The input also gets sent to the worker, who produces a state using an RNN ($U_t)$.

The worker produces $w_t$ based on $\phi(\sum^t_{t - c} g_i)$ (so basically, the "instruction"
is actually the moving average of the last few goals).

Then the worker takes action $a_t$ based on $w_t$ and $U_t$.

### "goal embedding"

Apparently $w_t$ can never be near-zero because $\phi$ has no biases.

### Learning

Independently train the manager to "predict advantageous directions"
and reward the worker for following those directions.

Update rule for the manager:

 - $\triangledown g_t = A_t^M \triangledown_{\theta} d_{\text{cos}} (s_{t + c} - s_t, g_t (\theta))$
 - $A_t^M = R_t - V_t^M(x_t, \theta)$ - the Manager's advantage functon (actor-critic)

 Then you have this $d_{\text{cos}}(s_{t + c} - s_t, g_t(\theta))$

 - $s_t = f^{\text{Mspace}}(z_t)$ - $c$ is a "horizon", defines the temporal resolution of the Manager
 - So we're taking the cosine distance between the state-representation delta over $c$
   and $g_t(\theta)$.
 - "Notice that now $g_t$ acquires a semantic meaning as an advantageous direction in the latent state
    space at a horizon $c$"
   - Essentially, the goal is "go that way in the state space"

 - NB: The goal is a kind of "direction"

 - Then to get the worker to follow the goal, $r^I_t = \frac{1}{c} \sum_i^c d_{\text{cos}} (s_t, s_{t - i}, g_{t - i})$
   - Eg, check that over the time horizon, check that we're going in the direction of the goal.
   - This all sort of assumes that there's an orientation in the state space.

 - Manager and the worker can have different $\gamma$ discount factors for computing the return -
   meaning that worker can be more greedy and manager can be more long term.


### Transition policy gradients

Update rule for the manager: "a novel form of policy gradient with respect to a model of the worker's behaviour"

We have some high-level policy $o_t = \mu(s_t, \theta)$ that selects between sub-policies, where
each sub-policy is a fixed-duration behaviour lasting for $c$ steps.

Each sub-policy has a transition distribution $p(s_{t + c}|s_t, o_t)$ which describes the
distribution of states we end up in at the end of the sub-policy (eg, $s_{t + c}$ is
the state at the end of the sub-policy, given the start state and sub-policy).

Then the high-level policy is transition policy over end states and start states:
$\pi_{^TP}(s_{t + c}|s_t) = p(s_{t + c}|S_t, \mu(s_t, \theta))$

Since we now that the state transitions always end on a state picked by the transition policy,
we can apply policy gradients to find the performance gradient with respect
to the policy parameters.

The main idea here is that we don't need to care about the worker's trajectory. We just need
to care about where the worker is likely to end up, assuming that the worker will succeed
in ending up in the right state.

 - von Mises-Fisher distribution: The mean direction is given by $g(o_t)$,
   we have: $p(s_{t + c}|s_t, o_t) \propto \exp{d_{\text{cos}}(s_{t + c} - s_t, g_t)}$
 - As a result, the update heuristic for the manager (remember that we used the cosine distance)
   will be a proper form for the transition policy gradient arrived at in eqn 10.


### Dilated LSTM

Nothing too fancy here, similar to dilated convolutions. We have several cores in the LSTM
and at each timestep update a different one, then pool the cores, which increases your spatial
resolution.

Set $r$ to something relatively large, like $r = 10$ to downsample by 10.

# tl;dr: What is the general idea

 - Separate manager and workers. Manager defines a "goal" (a direction in the state space),
   workers follow that goal by navigating to that part in the state space using their policy.
 - It seems like the worker is not trained to follow the goal per-se, but rather it is just trained
   to maximize advantage using actor-critic by acting in the environment on its own.
 - However, when used in conjunction with the manager later on, the worker policies
   have an extra "intrinsic" reward: $r^I_t = \frac{1}{c} \sum^c_{i = 1} d_{\text{cos}} (s_t, s_{t - i}, g_{t - i})$
   which should cause them to have a higher reward for following the goal given by the manager.
 - Training the high level policy:
   - What we want is for the manager to maximize its advantage by going to a new state
     in $c$ timesteps $s_{t + c} - s_t$. So its update rule is its advantage times
     the cosine similarity for the trajectory and the goal.
   - We also want the manager to produce a "goal" in line with this trajectory, hence the cosine similarity
   - "Transition policy gradients": Gradient of $E[A^M_t \triangledown_{\theta} \log p(s_{t + c}|s_t, \mu(s_t, \theta))]$
     - In practice this means that we have a probability distribution over future states at timestep $c$ steps
       ahead as a result of choosing a sub-policy by $\mu$
     - Then parameterize $p(s_{t + c}|s_t, \mu(s_t, \theta))$ by $e^{d_{\text{cos}} (s_{t + c} - s_t, g_t)}$,
       which when you subsitute that into the policy gradient gives you the desired update rule for the manager.
     - This doesn't seem to explicitly choose a sub-policy? Rather it is just saying that we choose one by
       setting this goal somehow.
     - But then there are apparently different subpolicies! How do you learn the different sub-policies?
       It seems like there is only one training mechanism for the sub-policy in general, so why are they different?
       How do they extract the weights? Still questions about this...


# Results

 - Kinda mixed
 - On some environments, you do very well (amidar, gravitar, enduro, frostbite)
 - On others you do about as well as the current SOTA
 - Seems kinda limited to tasks where you set goals that navigate the state space,
   not clear that the sub-policies are actually anything useful.