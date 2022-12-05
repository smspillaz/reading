---
title: "Learning Iterative Reasoning through Energy Minimization."
venue: "ICML"
pages: "5570-5582"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/DuLTM22"
ee: "https://proceedings.mlr.press/v162/du22d.html"
url: "https://dblp.org/rec/conf/icml/DuLTM22"
authors: ["Yilun Du", "Shuang Li", "Joshua B. Tenenbaum", "Igor Mordatch"]
sync_version: 3
cite_key: "conf/icml/DuLTM22"
---


Deep learning works really well with pattern recognition, but it doesn't work well with tasks that require nontrivial reasoning. How to "spend more time" thinking about a task.

In the "energy based model" framework, this is possible!

The basic idea is to learn an energy function over all outputs, then implement gradient-based iterative reasoning such that you take a step in the direction that minimizes energy each time.

We frame the problem as such:

$$
y^t = f_{\theta}(x, y^{t - 1})
$$

In this case:

$$y = \arg \min E_{\theta}(x, y)$$

where an individual reasoning step is just gradient descent:

$$
y^t = y^{t - 1} - \lambda \triangledown_y E_{\theta}(x, y^{t - 1})
$$

How do you train the thing?

You can sample data and candidate solutions from $p_d$ and a replay buffer, initialize the starting states, then take steps on the energy model and then take the loss between the final state $\tilde y^N_i$ and $y_i$.

Note: there's no contrastive divergence training here.

One problem can be that running a large number of iterative reasoning steps at test time can cause the underlying solution to degrade. To deal with this, you have a *replay buffer* of previously optimized samples $y^N_i$ and you initialize the $y^0_i$ from either $y^N_i$ or noise.

Note that learning $E(x, y)$ is sort of like learning a solution verifier (a classifier).

Then they have a bunch of experiments where they compare with:
 - Feedforward
 - RNN
 - PonderNet
 - Iterative Feedforward using iterative denoising (citing the diffusion paper)

Notes on the energy landscape: Figure 5: Predicted energy values for $y$ and the corresponding MSE distance of $y$ from the problem solution.