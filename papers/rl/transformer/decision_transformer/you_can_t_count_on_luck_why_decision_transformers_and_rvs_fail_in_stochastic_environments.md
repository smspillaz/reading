---
title: "You can't count on luck: Why Decision Transformers and RvS fail in Stochastic Environments"
---
# Discussion with the Author


Rather than use trajectoru return, learn function of trajectory that is independent of stochasticity.

ESPER
- adversarial clustering
- estimate average returns
- train rvs


Optimize cluster assignments so that it is easier to predict actions given the cluster but hard to predict the states. Then label using average returns and use that to train the decision transformer.


The problem is that when you condition on return = 5, you assume that the state where you get a return of 5 happens when you take action 0.