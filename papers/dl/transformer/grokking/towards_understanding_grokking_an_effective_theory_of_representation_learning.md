---
title: "Towards Understanding Grokking: An Effective Theory of Representation Learning."
venue: "CoRR"
volume: "abs/2205.10343"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-10343"
doi: "10.48550/ARXIV.2205.10343"
ee: "https://doi.org/10.48550/arXiv.2205.10343"
url: "https://dblp.org/rec/journals/corr/abs-2205-10343"
authors: ["Ziming Liu", "Ouail Kitouni", "Niklas Nolte", "Eric J. Michaud", "Max Tegmark", "Mike Williams"]
sync_version: 3
cite_key: "journals/corr/abs-2205-10343/Liu/2022"
---

Representations are key to grokking. You get much more structured representations at grokking.

Assume that you have 4 embeddings and you want to generalize addition. If you want to do this, they have to lie on a parallelogram. The nn tries to change the embeddings so that the task is as simple as possible. Eg, vector addition. So 1 + 2 = 3 (in embedding space)

There is a critical training set size below which the model is unable to generalize. Hessian of the loss function determines this. If you take the eigenvalues of the Hessian, the smallest one's inverse tells you the grokking time. If it is zero, you cannot generalize.


Whether or not you're in a grokking space depends on the combination of weight decay and learning rate. Training set size also matters.

You dont need every single combination to know that the embeddings should be on a line

If you do hyperparameter search you should do it along weight decay and learning rate

Or maybe if at least theoretically generalization is possible, throw out any non-generalizimg hyperparameter combination early on