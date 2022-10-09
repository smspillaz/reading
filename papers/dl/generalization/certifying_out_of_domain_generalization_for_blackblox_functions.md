---
title: "Certifying Out-of-Domain Generalization for Blackbox Functions."
venue: "ICML"
pages: "23527-23548"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/WeberLWZ0022"
ee: "https://proceedings.mlr.press/v162/weber22a.html"
url: "https://dblp.org/rec/conf/icml/WeberLWZ0022"
authors: ["Maurice Weber", "Linyi Li", "Boxin Wang", "Zhikuan Zhao", "Bo Li", "Ce Zhang"]
sync_version: 3
cite_key: "conf/icml/WeberLWZ0022"
---
Being able to have some bounds on OOD generalization would be nice, but most of the existing techniques assume something about the model class or loss function.

In this paper, focus on certifying distributional robustness for blackbox models and bounded loss functions

We want to compute the distributional robustness, eg,:

$$
\mathcal{R}_{\theta}(\mathcal{U}_p) = \sup_{Q \in \mathcal{U}_p} E_{(X, Y) \sim Q}[\mathcal{l}(h^P_{\theta}(X), Y)]
$$

Eg, we want to know what is the highest possible expected loss for all $X, Y$ in all $\mathcal{U}_p$ distributions. So this measures the worst case risk of $\mathcal{h}_{\theta}$ when shifting from any distribution in $\mathcal{U}_p$ to any other distribution in $\mathcal{U}_p$.

Since the function is a black box, in this paper they look at *certification* which means that if $P$ is an in-domain distribution and $Q$ is a shifted distribution, then $\text{dist}(Q, P) < \rho \implies E_{(X, Y) \sim Q}[\mathcal{l}(h^P_{\theta}(X), Y)] \le C_t(\rho, P)$.

Hellinger Distance:

$$
H(P, Q) = \sqrt{\frac{1}{2} \int_{\mathcal{Z}} (\sqrt{p(z)} - \mathcal{q(z)})^2 d \mu(z)}
$$

$\mu(z)$ is a reference measure.

The idea behind the Hellinger distance is that it is bounded between 0 and 1 where $H(P, Q) = 0$ iff $P = Q$. $H(P, Q) = 1$ where the two distributions are disjoint