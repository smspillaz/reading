---
title: "Deep Reinforcement Learning at the Edge of the Statistical Precipice."
venue: "CoRR"
volume: "abs/2108.13264"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2108-13264"
ee: "https://arxiv.org/abs/2108.13264"
url: "https://dblp.org/rec/journals/corr/abs-2108-13264"
authors: ["Rishabh Agarwal", "Max Schwarzer", "Pablo Samuel Castro", "Aaron C. Courville", "Marc G. Bellemare"]
sync_version: 3
cite_key: "journals/corr/abs-2108-13264/Agarwal/2021"
tags: ["DeepMind"]
---

# Deep Reinforcement Learning at the Edge of the Statistical Precipice

Using point estimates is bad.

## Case study: Atari 100k

Prior work:
 - Median Human Normalized Scores (3-5 runs per game)
 - $\text{median}(\frac{1}{N} \sum x_{1, n}, \frac{1}{N} \sum x_{2, n}, ...)$

Experimental setup:
 - Evaluate 100 independent runs for DER, OTA, DrQ, CURL, SPR
 - 26x100 games and scores . Subsample with replacement to 3-100 runs
 - We want to investigate the statistical variations.

Sample medians exhibit substantial variability. Reported estimates do not provide variability and severly overestimate or underestimate the median.

Medians are biased!

How many runs for negligible uncertainty? 30-50 is required, FAR TOO MANY for many modern projects.

Changes in evaluation protocols invalidates comparisons to prior work?

## How to reliably evaluate performance?

- Fixing random seeds? Not a solution. Often cannot fix randomness in practice.
- Evaluating more runs? Not feasible
- Statistical significant testing? Not really. Dichotomous, widely misinterpreted, often hide effect sizes


## How to reliably evaluate performance with a *handful of runs*


### Interval estimates

Stratified bootstrap confidence intervals

 - Resample runs with replacement independently for each task
 - If we repeat the experiment with differnt runs, what aggregate scores will you be expected to get?
 - Statistical bootstrapping works well in the scenario where you have M * N tasks.


### Aggregate metrics hide variability

Tables with per-task scores, overwhelming beyond a few tasks. Standard deviations frequently omitted. Mean scores present incomplete picture.

A better approach:
 - Performance profiles with CIs
 - $p(\tau) = \frac{1}{NM} \sum \sum 1[X_{n, m} > \tau]$
 - Typically used for comparing solve times of different optimization methods
 - Robust to outlier runs/tasks
 - Robust to small changes in performance across all tasks.


Allows you to do birds-eye views of performance profiels.

The place where the curves intetrsect y = 0.5 is the median. The area under the curve is the mean. One curve over another means stochastic domiannce.

Plot fraction of runs with score above $\tau$.

What if one algorithm doesn't dominate the other? Need to aggregate metric for reporting quantitative performance.

Mean prone to outliers, median has highly variable and not robust.

Median: IQM: Averages middle 50% of scores across all runes and tasks.

Mean: Optimality gap: How far are you from optimal performance. Areas under the performance profiles.

IQM more robust to outliers. Requires fewer runes.

## Am I better than the baseline?

Probability of improvement of algorithm X over Y

$$
P(X > Y) = \frac{1}{M} \sum^M P(X_m > Y_m)
$$