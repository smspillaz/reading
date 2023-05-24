---
title: "You Can&apos;t Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments."
venue: "NeurIPS"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/PasterMB22"
ee: "http://papers.nips.cc/paper_files/paper/2022/hash/fe90657b12193c7b52a3418bdc351807-Abstract-Conference.html"
url: "https://dblp.org/rec/conf/nips/PasterMB22"
authors: ["Keiran Paster", "Sheila A. McIlraith", "Jimmy Ba"]
sync_version: 3
cite_key: "conf/nips/PasterMB22"
---
# Discussion with the Author


Rather than use trajectoru return, learn function of trajectory that is independent of stochasticity.

ESPER
- adversarial clustering
- estimate average returns
- train rvs


Optimize cluster assignments so that it is easier to predict actions given the cluster but hard to predict the states. Then label using average returns and use that to train the decision transformer.


The problem is that when you condition on return = 5, you assume that the state where you get a return of 5 happens when you take action 0.