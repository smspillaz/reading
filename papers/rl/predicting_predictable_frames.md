---
title: Time-Agnostic Prediction: Predicting Predictable Video Frames.
venue: ICLR
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/iclr/JayaramanEEL19
ee: https://openreview.net/forum?id=SyzVb3CcFX
url: https://dblp.org/rec/conf/iclr/JayaramanEEL19
authors: ["Dinesh Jayaraman", "Frederik Ebert", "Alexei A. Efros", "Sergey Levine"]
sync_version: 3
cite_key: conf/iclr/JayaramanEEL19
---
# Time Agnostic Prediction: Predicting Predictable Video Frames

Basic Idea: Predicting between the waypoints is hard, but there are bottlenecks or
"waypoints" that we can probably predict with more certainty.

Decouple visual prediction from time - time agnostic predictors are not tied to specific
times, instead they discover predictable "bottleneck" frames.

If we just try and predict all frames, usually you get blurriness - this makes sense
because it predicts a mean value with high-ish variance, which is what minimizes the MSE
loss.

Time Agnostic Prediction:

 (1) Predictor may skip more uncertain states in favor of less uncertain ones
 (2) You can predict the write frame at the wrong time

Contributions:

 - Reframe the video prediction problem to be time-agnostic
 - Novel technical approach
 - Identify "bottleneck" across several tasks
 - Bottlenecks correspond to subgoals that aid in planning

Bottlenecks have been proposed for the discoery of
options. Eg, multi-instance learning - mine states that occurr
in successful trajectories but not in others.

Use "predictability" to identify bottlenecks. Similar to Neitz -
allow a predictor to select when to predict.

## Loss Function

### Min-over-time loss

$G^* = \text{arg} \min_G L(G) = \text{arg} \min \min_{t \in T} \text{Err}(G(c), x_t)$$

Effectively, your loss is the frame that you're most closely matched with. Therefore
you latch-on to "bottleneck" states in the video, those with low uncertainty.

Question: Won't this just regenerate this input? Authors say that lowest uncertainty
frame isn ot always the input. Must be different by at least one step, no worse
than one-step-forward.

Question: How to do this recursively? Just make the timesteps that you take the
prediction minimizer over a function of the recursion step. Eg, set $c(r)$ to the
previous prediction so that you target all times after the last prediction.

### Generalized Minimum TAP loss

How do we specify preferences for some times over others?

$$
L(G) = \min_{t \in T} \text{Err}_t = \text{Err}_{\text{arg} \min_{t \in T} \text{Err}_t}
$$

$\text{Err}_t$ could be designed to express preferences about which frames to predict.

Let $w(t)$ express a preference value for all target times, then set $\text{Err}'_t = \frac{\text{Err}_t}{w(t)}$
so that times $t$ with higher $w(t)$ are preferred in the arg min. Eg, set $t$ to increase with time,
or to a truncated Gaussian centered in the midpoint. Note that we don't pass this downweighted thing
to the loss, we only use it to figure out what to compare against.

### Time Agnostic Conditional GANs

You don't need to have $l_1$ or $l_2$ error - you can also use a perceptual loss.

CGAN: Given a discrimiantor that outputs 0 for input-prediction tuples and
and 1 for input-output tuples. Train the generator to fool the discriminator.

$
L_{\text{cgan}}(G, D) = \log(D(c, x_t)) + \log(1 - D(c, G(c))
$

Train $|T|$ descriminators per timestep, then define a time-agnostic CGAN loss:

$G^* = \arg \min_G \min_{t \in T} \max_{T_t} L^t_{\text{cgan}}(G, D_t)$

Essentially the generator tries to maximize the discriminator loss. We pick the one
that is the lowest amongst all discriminators.

### Conditional VAEs

A training time, sample $z$ from a posterior distribution, conditioned
on the input $X$. At test time, sample it from a prior (uniform random noise). Training
loss incentivises us to not diverge too far from the prior, while at the same time
maximizing log-likelihood.

## Some Results

Trying to predict fixed points in the sequence results in frames that don't look very realistic,
have a lot of blurriness etc. Trying to predict predictable frames results in frames that look
nicer. They're still kinda blurry but don't contain huge visual anomalies.


### Visual MPC
Visual MPC planner (Ebert et al). Internally Visual MPC makes action conditioned fixed-time
forward predictions of future object positions to find an action sequence that reaches the subgoal.

Given start and goal images, produce subgoals. Visual MPC plans towards this subgoal
for half the episode length, then switches to the final goal.

Visual MPC planner makes fixed-time forward predictions given a sequence of actions -
pick the one that brings you closest to the goal state (cross-entropy method).

## Limitations

 - Can we figure out timestamps?
 - Repeated frames, mgiht just collapse to predicting the input state.
