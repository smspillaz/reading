---
title: Conservative Q-Learning for Offline Reinforcement Learning.
venue: NeurIPS
year: 2020
type: Conference and Workshop Papers
access: open
key: conf/nips/KumarZTL20
ee: https://proceedings.neurips.cc/paper/2020/hash/0d2b2061826a5df3221116a5085a6052-Abstract.html
url: https://dblp.org/rec/conf/nips/KumarZTL20
authors: ["Aviral Kumar", "Aurick Zhou", "George Tucker", "Sergey Levine"]
sync_version: 3
cite_key: conf/nips/KumarZTL20
---
"Conservative off-policy evaluation" is given by:

$$
\hat Q^{k + 1} = \arg \min_Q aE_{s \sim D, a \sim \mu(a|s)}[Q(s, a)] + \frac{1}{2} E_{s, a \sim D}[(Q(s, a) - \hat B^{\pi} \hat Q^{k}(s, a))^2]
$$

In essence, we try to find a Q that is minimal under the unseen actions and has a small difference from the previous Q function under the seen states and actions.

To improve the bound, maximize the Q function under actions sampled from the behaviour policy (if you know it):

$$
\hat Q^{k + 1} = \arg \min_Q a(E_{s \sim D, a \sim \mu(a|s)}[Q(s, a)] - E_{s \sim D, a \sim \hat \pi_{B}(a|s)}[Q(s, a)]) + \frac{1}{2} E_{s, a \sim D}[(Q(s, a) - \hat B^{\pi} \hat Q^{k}(s, a))^2]
$$

What this does is penalize everything that isn't selected by the behaviour policy.

"Conservative Q learning" provids a method to do this that doesn't require knowing what $\mu(a|s)$ is, but instead *adversarially* solves for it as part of an innner loop:

$$
\hat Q^{k + 1} = \arg \min_Q \max_{\mu} a(E_{s \sim D, a \sim \mu(a|s)}[Q(s, a)] - E_{s \sim D, a \sim \hat \pi_{B}(a|s)}[Q(s, a)]) + \frac{1}{2} E_{s, a \sim D}[(Q(s, a) - \hat B^{\pi} \hat Q^{k}(s, a))^2]
$$

In that sense we find a policy that tries to *exploit* the Q function and *penalize* what the Q function says about those actions.