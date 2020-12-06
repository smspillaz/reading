# CausalLens

The real world is nonstationary. The past is almost never representative of the present
adn the future.

Learnign the past perfectly doesn't help you all that much when the future doesn't look like the past.

Correlation is not Causation. You learn patterns in the data.

Trading using automated AI platforms loses money.

Biases exist within predictive hiring.

"Teaching Deep Larning Causal Effects Improves Predictive Performance"

All current causal discovery methods are limited. Restrictive assumptions in top research:

 - No time ordering
 - No hidden confounders: assume that the datasets are complete
 - No regime shifts: assume that the world remains pretty much the same.
 - No feedback loops: 


Prominent techniques are sensitive to assumption vioplations.

 - Pre-filtering oftern required
 - Nonlinear methods are expensive

Suggested future research:

 - Methods that work in broader scenarios
 - Methods that are less dependent on choice of hyperparmeters
 - Meta-models that can automatically choose the optimal method based on the data

"Data Generating Process to Evaluate Causal Discovery Techniques for Time Series Data"

 - It is very easy to overfit on the current methods
 - They don't scale so well with the number of features
 - They are oversensitive to hyperparameters


Example:

 - If I place a $1m buy order on stock X, what happens?
 - Let the machine imagine what would have happened.


Searching for Valuable Data:
 - Too many false positives or false negatives
 - Need to filter spurious correlations


What if you have sparse observations with not so much data?


Suggested reading:
 - Causal Discovery and Forecasting in Nonstationary Evnrionments with State Space Models
