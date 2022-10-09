---
title: "Why do tree-based models still outperform deep learning on tabular data?"
venue: "CoRR"
volume: "abs/2207.08815"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2207-08815"
doi: "10.48550/ARXIV.2207.08815"
ee: "https://doi.org/10.48550/arXiv.2207.08815"
url: "https://dblp.org/rec/journals/corr/abs-2207-08815"
authors: ["L\u00e9o Grinsztajn", "Edouard Oyallon", "Ga\u00ebl Varoquaux"]
sync_version: 3
cite_key: "journals/corr/abs-2207-08815/Grinsztajn/2022"
---

In this paper they collect 45 datasets from varied domains. They have a consistent methodology for fitting tree-based models and deep learning models and tuning their hyperparameters.

Main finding is that for small-to-medium sized data, tree based models still remain state-of-the-art.

Then they look into how you could make the NN models more robust to uninformative features, preserving data orientation and learning irregular functions.

Why do we even care? Tree-based models are not differentiable, so you can't easily compose them with other models

# Related Work

Lots of attempts to try and make this work. See the review by [[deep_neural_networks_and_tabular_data_a_survey|Borisov et al]].  But you can basically classify into the following approaches:

 - Data encoding techniques (Hancock and Khoshgoftaar)
 - Hybrid methods (Lay et al)
 - Factorization MAchines (Guo et al)
 - [[tab_transformer_tabular_data_modeling]] (Somepalli et al, Kossen, Arik and Pfister)
 - Regularization techniques

In this paper they focus on transformer and MLP.

# The benchmark

They compiled 45 tabular datasets from different domains, selected via the following criteria:

 - Heterogeneous columns
 - Not high dimensional
 - Documented
 - Validation set should be ID and data itself should be IID
 - Data should be from the real world and not artificial or algorithmically generated.
 - Data should have at least 4 features and 3000 samples.
 - Should not be so easy that logistic regression can solve it.
 - Should not be non-deterministic

## Postprocessing

Then in post-processing, they do:
 - Truncation to 10,000 samples each
 - Impute missing data or remove columns with many entries that are missing
 - Rebalance the dataset
 - Remove categorical features with > 20 items
 - Remove numerical features with < 10 unique values

To preprocess, they:
 - Normalize features
 - Log-transform targets when heavy-tailed
 - One-hot encode categoricals

## Hyperparameter Selection on models

Use Hyperopt with a random search of 400 iterations per dataset.

# Models

Tree-based:
1. Random Forest
2. Gradient Boosted Trees
3. XGBoost

Deep learning
1. MLP
2. ResNet
3. Transformer [[revisiting_deep_learning_models_for_tabular_data]]
4. "SAINT" - inter-sample attention mechanism [[saint_improved_neural_networks_for_tabular_data_via_row_attention_and_contrastive_pretraining]]

Basically, the tree-based models still kick the pants off the deep learning models, but of the deep learning models, SAINT is doing the best. Note that R2 score goes from 0 to 1, where 1 is the best. Deep learning can improve a fair bit with the right hyperparameters, as can XGBoost. However they still can't beat the tree-based models.

Categorical variables are also not the main source of weakness in NNs.

# OK but why does this happen?

1. The best methods are ensemble methods which have a tree-structure.
2. NNs are biased to overly smooth solutions. Eg in figure 3 they have model performance as a function of a smoothing parameter. If you smooth the target, performance of decision trees goes down, performance of NNs remains the same. NN's don't like high frequency functions
3. Uninformative features affect neural nets that are more like MLPs. Removing the uninformative features actually reduces the performance gap and adding them widens the gap. MLP doesn't just learn to ignore them.
4. NNs are rotationally invariant, and this is a *bad* thing. It means that feature clipping can happen in the rotated basis, so you're no longer making decisions based on individual features, but rather on mixes of features.