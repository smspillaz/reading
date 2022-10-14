---
title: "The Value of Out-of-Distribution Data."
venue: "CoRR"
volume: "abs/2208.10967"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2208-10967"
doi: "10.48550/ARXIV.2208.10967"
ee: "https://doi.org/10.48550/arXiv.2208.10967"
url: "https://dblp.org/rec/journals/corr/abs-2208-10967"
authors: ["Ashwin De Silva", "Rahul Ramesh", "Carey E. Priebe", "Pratik Chaudhari", "Joshua T. Vogelstein"]
sync_version: 3
cite_key: "journals/corr/abs-2208-10967/Silva/2022"
---

Real datasets can contain OOD data. We would expect that every OOD sample we see helps us on this distribution, but this is not always true!

if the OOD samples are not known, there is no strategy that is guaranteed to be effective in eliminating the adverse impact of OOD data.

Why does this happen?

 - Geometric and semantic nuisanses (eg, small rotations decrease generalization, large rotations increase it - you have two modes of data).
 - OOD samples are drawn from a different task

Can this be exploited somehow?

- biased sampling procedure, where each mini-batch contains $\beta$ fraction samples of training data and the remainder $1 - \beta$ are OOD. If you set $\beta = \frac{n}{n + m}$ you get an unbiased estimate with respect to the unweighted total objective.