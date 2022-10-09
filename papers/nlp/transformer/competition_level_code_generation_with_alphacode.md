---
title: "Competition-Level Code Generation with AlphaCode."
venue: "CoRR"
volume: "abs/2203.07814"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2203-07814"
doi: "10.48550/ARXIV.2203.07814"
ee: "https://doi.org/10.48550/arXiv.2203.07814"
url: "https://dblp.org/rec/journals/corr/abs-2203-07814"
authors: ["Yujia Li", "David H. Choi", "Junyoung Chung", "Nate Kushman", "Julian Schrittwieser", "R\u00e9mi Leblond", "Tom Eccles", "James Keeling", "Felix Gimeno", "Agustin Dal Lago", "Thomas Hubert", "Peter Choy", "Cyprien de Masson d&apos;Autume", "Igor Babuschkin", "Xinyun Chen", "Po-Sen Huang", "Johannes Welbl", "Sven Gowal", "Alexey Cherepanov", "James Molloy", "Daniel J. Mankowitz", "Esme Sutherland Robson", "Pushmeet Kohli", "Nando de Freitas", "Koray Kavukcuoglu", "Oriol Vinyals"]
sync_version: 3
cite_key: "journals/corr/abs-2203-07814/Li/2022"
---

[[competition_level_code_generation_with_alphacode.pdf]]

Empirical project. What is required to get good and relaible performance on code-generation for these sorts of code-competition tasks?

1. Extensive and clean dataset
2. Large and efficient-to-sample transformer architectures
3. Large scale model sampling to explore the search sapce, followed by filtering based on program behaviour to a small set of submissions


# Challenges
1. Generating code that solves a specific task requires searching in a huge structured space of possible programs with a very sparse reward signal.
	1. Example: Single character edits can completely change the behaviour. Its not like the state space is one where close-in-edit-distance implies close-in-value.
	2. Upshot: Search-based solutions do not work so well
2. Snippits vs entire code: Snippits can be self-contained and side-effect free. Entire programs require reasoning about what the entire inputs and outputs are and what the expected behaviour should be.
3. Competitive Programming:
	1. "Complex natural language descriptions"
	2. "Reasoning about previously unseen problems"
	3. "Mastering a wide range of algorithms and data structures"
	4. "Precisely implementing solutions that can span hundreds of lines"
	5. Hidden test cases
	6. Penalties if you submit a wrong solution to a problem.
	7. You have to solve the problem efficiently (space requirement, time requirement).



## Evaluation Methodology

A methodological challenge: Ensuring that evaluation problems are truly unseen druing training. Difficult problems should not be solveable by copying from the training set.

### Dataset

CodeContests dataset: "split temporallly so that all training data predates all evalaution problems and adds additional generated tests to ensure correctness"

Methodology for validating the temporal split. Use baselines:

 - "evaluating one solution from each training problem" (eg, the copy-paste baseline): 4.1% random split, 0% temporal split
 - 1B parameter model trained on github: 0.8% random split, 0% temporal split

"The models must go beyond simply remembering the training set".

### Metrics

Live programming competitions are the gold standard, but not a stable benchmark.

New metric: "percentage of problems solved using $n$ submissions from $k$ samples per probelm", $n@k$ . So basically, $k$ proposals, and choose to submit $n$ of them. Successful if any one of the $n$ passes all hidden tests.

The filtering method is up to the system itself, but it should be based on information available to the competitors, eg, the example tests that are part of the problem description, not the hidden tests.

# Pretraining

Include all public code from C++, C#, Go, Java, JavaScript, Lua, Python, PHP, Ruby, Rust, Scala, TypeScript.

You end up with 715.1GB of code as a result.

# Fine-tuning

Code on GitHub doesn't solve competitive programming problems.

Scrape codeforces, Description2Code, CodeNet. Don't include the difficulty rating or tags in the test data.

The dataset contains correct and incorrect human submissions. Majority of solutions are actually incorrect, for example, 27% of C++ solutions in the training set are not correct.

# Test cases

False Positive: An incorrect solution that happens to be correct on all the provided test cases, but actually has bugs.

"Slow positives": Correct solution, algorithmically inefficient.

How do you know if something is a false positive? Randomly sample 50 problems solved by a 1B parameter model, which could generate 10,000 samples per problem. Manually examine one solution to check for a false positive or slow solution.

How to reduce false positives? Generate additional test cases by mutating existing test inputs. Eg, bit flips on binary inputs, randomly incrementing/decrementing integers, swapping and changing characters in strings.


# Approach

1. Pre-train a transformer model on GitHub with language modelling objective
2. Fine-tune the model on competitive programming data using GOLD with tempering as the training objective. GOLD is a kind of RL-based text generation objective.
3. Generate very large numbers of samples for each problem
4. Flter the samples to obtain a small set of candidate submissions, using the example tests and clustering to pick different samples.

## Transformer Model

Its a sequence-to-sequence translation task. Given problem description $X$, produce code solution $Y$

Asymmetric architecture with 1536 tokens for the encoder but only 768 tokens for the decoder (the rationale being problem descriptions are on average twice as long as their corresponding human solutions). Not sure what they mean by having "1536 tokens for the encoder". Perhaps this is the maximum sequence length in each batch.

Use multi-query attention: A full-set of query heads but shared key and value heads per attention block.

## Pretraining

Use next-token prediction loss for decoder and MLM loss for the encoder.

## Fine-tuning

Fine-tune on CodeContests. Standard next-token prediction and MLM losses. Also with additional conditioning and modifications that improve the overall solve rate, tempering, value conditioning and prediction as well a GOLD and metadata conditioning.

**Tempering**: [[softmax_tempering_for_training_neural_machine_translation_models]] - sharpen the token probability distribution by dividing the logits by $T$ before softmax. They actually use it in the opposite way to what was suggested in the first paper - divide by 0.2 to make the training distribution sharper and consequently "the inference distribution smoother". So the effect of this is that you have an artificial confidence boost during training, but that goes away during test time? But then they divide by $T'$ at inference time which was 0.12, so even more sparse.

**Value Conditioning**: Discriminate between correct and incorrect probelm submissions. Condition on whether or not a solution was correct. Then at inference time, assume that you are sampling a correct solution.

**GOLD**: Each unique problem admits any distinct solutions. Many more solutions than descriptions, so standard maximum likelihood tries to put weight on each solution in the training set. This metric is different: it measures whether the model can find a single correct solution within some budget.

$$
\triangledown \mathcal{L}_{\text{GOLD}}(\theta) = - \sum_{s \in \text{solutions}} P_{\theta}(s) \triangledown \log P_{\theta}(s)
$$

Basically: learn from tokens that you've assigned a high-likelihood to and ignore tokens that are not in distribution. This enables concentration on precision rather than recall.

## Large scale sampling

How to get diversity in samples?

 * Prompt for different languages (python, C++)
 * Randomize problem tags and ratings in the NL prompt
 * Use a high sampling temperature


How to generate different tags?
 - Pick random tags from the most popular 50
 - Sampled ratings uniformly from 800 to 250

Optimal sampling temperature ? Depends on total number of samples, but it doesn't seem to make much of a difference, so just keep it at 0.25 in all experiments that use tempering and 0.12 in all experiments that use GOLD.


## Filtering

Filter samples to only those that pass the example tests. Apparently this throws out a large marority, since on 10% of problems you don't even solve the sample tests.

## Clustering

Many semantically equivalent programs remain.

One possible solution: use more test cases to group solutions together based on outputs to testcases.

Train a separate test input generation model using the same architecture. It should predict test inputs from the same github pretrained checkpoint. Predict test inputs from problem descriptions using example, hidden(??) and generated test inputs as training data.

Test inputs not guaranteed to be valid, invalid test inputs can still be useful for grouping outputs.

# Evaluation

## On codeforces
![[alphacode_codeforces_evaluation.png]]

Evaluate on competitions from 2021/12/01 to 2021/12/28

## On CodeContests
![[alphacode_codecontests_evaluation.png]]

# Abalation Study

## What if you have unlimited attempts per problem?
![[alphacode_ablation_unlimited_attempts.png]]
This is on CodeContests.

More parameters and more samples generated are better (you will eventually find the monkey at the typewriter which produces shakespeare), though samples scales better than parameter count.

## Scaling
Take-aways:

 * Solve-rates scale log-linearly with more samples
 * Better models have higher slopes in the scaling curve
 * Solve rates scale log-linearly with more compute


## Improving Sampling speed - architecture changes
![[alphacode_architecture_ablations.png]]

Asymmetric encoder and decoder structures and multi-query attention setup decrease solve rate somewhat, but they improve sampling speed meaning that you can sample more possible options in limited time.

### Model Ablations and Solve Rate
![[alphacode_model_ablations.png]]

Clustering helps a lot when you have many samples to choosen from.

Value preconditioning also helps (only generate "good" solutions).

# Limitations

## Does it just copy the training data?

Longest-common-substring between correct validation problem solutions generated by the model and the entire training set (similar to the observations made in [[retro_improving_language_models_by_retrieving_from_trillions_of_tokens#Quantifying Dataset Leakage]]).

Now we know that copying full solutions is not sufficient to solve any problems in the unseen validation set. But you might be able to get away with duplicating parts of previous solutions.

Findings: Humans and models copy from the training set, but the model copies a bit more. Usually boilerplate.

## Is it hard to get syntax right?

Easier to get python syntax right than C++.

## What about solve rates by tag?

"Our models are better at problems that deal with bitmasks, sorting, maths and greedy algorithms, but notably *worse at dynamic programming*"

## How long solutions do you generate?
![[alphacode_correlation_between_human_length_and_alphacode_length.png]]


## Sensitivity to problem descriptions
![[alphacode_sensitivity_to_problem_descriptions.png]]
When given a simplified description of the problem, the model solves it at a much higher rate.

Solve rate goes down when given related but different problems.

Model unaffected by changes that do not seem significant (like replacing words with synonyms or removing some type details) but responds to larger changes that would make the problem ill-posed.

## Sensitivity to provided metadata

Providing different tags changes what algorithms the model generates.

## Loss is a poor proxy for solve rate

Validation loss might increase but solve rate continues to improve past the point where validation loss is increasing.

# Impact

## Applications

1. Productivity improvements (a-la codex)
2. Efficiency improvements
3. Code-to-documentation
4. Malware
5. Technical interviews

## Risks / Benefits

1. Interpretability: Easier to prove a generated sorting algorithm is correct than proving that an NN will sort the numbers correctly.
2. Generalization
3. Bias, fairness, representation: Low quality code that perpetuates bugs or uses outdated APIs.
4. Security: Memorize weaknesses, training set could be flooded with security bugs
5. Environmental impact: Training large scale models is expensive
6. Intellectual Property
7. Automation: No more jobs for programmers
8. Advanced AI risks: Skynet