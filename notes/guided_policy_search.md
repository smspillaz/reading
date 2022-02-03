# Guided Policy Search

The main gist is that we use a moel for planning in order to train a policy.

Learn a model of the environment, then use a controller to plan rollouts in the model. For example the model can be a random controller initially, or it can be iLQR.

![[gps.png]]

Then with GPS, you use the rollouts to bootstrap the policy training

When running the controller again, we want the actions taken by the controller to match what the policy would do in those states.

$$
\min_{u_1, ..., u_T, x_1, ..., x_T} \sum c(x_t, u_t), x_t = f(x_{t - 1}, u_{t - 1}), u_t = \pi_{\theta}(x_t)
$$

Solve that optimization problem using *dual gradient descent*. Transform the equation into a lagrange dual:

$$
\mathcal{L}(x, \lambda) = f(x) + \lambda C(x)
$$
$$
g(\lambda) = \mathcal{L}(x^* (\lambda), \lambda)
$$

The steps are:
 1. Find $x^* = \arg \min_x \mathcal{L}(x, \lambda)$ by setting the gradient to with respect to $x$ to zero and solving for $x$. For example, this can be done with iLQR
 2. Compute $\triangledown_{g} \lambda = \triangledown_{\lambda} \mathcal{L} (x^*, \lambda)$ This can be done with SGD
 3. Update $\lambda$ with gradient descent.

The main intuition is that we want to limit the amount that the controller diverges from the policy on each iteration. Big changes will lead to large errors and unstable gradients. A trajectory is penalized if it diverges too much from the policy.