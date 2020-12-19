# Continuous Control with Deep Reinforcement Learning: DDPG

Deterministic Deep Policy Gradients.

Basically extends Actor-Critic to continuous control spaces.

How this is done - instead of a discrete action space where you
learn the probability of taking some action, instead you
directly differentiate through the value function - so the
value function (or rather the Q function) needs to take your
action parameter as well.

One problem is that your critic and actor functions will exploit each
other. So what you should do is keep a separate "target critic" function
updating its weights on a moving average basis and use the target critic
to learn the value for the actor's actions.
