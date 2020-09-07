# Meta-Learning for Few-Shot NLP: A survey

https://arxiv.org/abs/2007.09604

Meta-Learning: Train a model on a variety of tasks with rich annotations, so that you can solve a new task quickly.
Train the model's initial parameters such that the model has maximal performance on a new task after the parameter
have been updated through a few gradient update steps.

In the meta-learning framework, treat *tasks as examples*. To solve a new task collect lots of tasks and fit
a model to adapt to all training tasks.

Eg, text classification: We assume that training sentences and test sentences are from the same distribution.
In task learning: tasks come from the same distribution. During meta-training, you sample a task and then test
on the test set -> the test error is your training signal.

Each new task has only K labeled examples and a large set of unlabeled test instances. Meta-learning progressively
learns to solve many tasks, and the idea is that if you learn to learn, then you become better at solving new tasks
even if you have few examples.

## Meta-Learning vs Transfer Learning

Transfer Learning leverages past experience to improve the target by pre-training. In TL
you have weights from some other related tas and this new knowledge helps you with your current task.

In meta-learning you instead learn-to-learn.

Meta-learning assumes that the training tasks are in the same distribution as the target tasks - eg, same
problem, different domains. Transfer learning does not have tis assumption.

## Meta-Learning vs Multi-Task Learning

Meta-Learning is a kind of multi-task learning. Main differences:
 (1) Conventional goal of multi-task learning is to learn a pre-trained model that generalizes well. In
     contrast, meta-learning tries to learn an efficient learning procedure
 (2) Multi-task learning favors tasks with larger amounts of dat 
 (3) Meta-learning treats tasks as training examples, but multi-task learning may run into problems if
     you have too many tasks.
