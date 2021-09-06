# Attention is not all you need: Pure attention loses rank doubly exponentially with depth

[[dong_attention_is_not_all_you_need.pdf]]

In this work, seek to better understand what makes self-attention effective.

Pure-self-attention networks have an inductive bias where all tokens become uniform and the rank effectively collapse. Skip connections play a role by mitigating rank collapse.

MLPs can slow down convergence by increasing their Lipschtiz constant.

## Path decomposition

Decompose attention model output into simpler path components.

Each path corresponds to a deep single-head self-attention network.

Convergence of path residuals.

Theorem: without skip connections or MLPs, pure self-attention converges to rank-1 doubly exponentially quickly wrt depth.

P-matrices are row-stochastic (after softmax normalization) - product of stochastic matrices generally converges to rank-1.

skip-connections and MLPs counteract this convergence by diversifying the path distributions in width-H and depth-L. There are many more paths of short enghts. With skip connections you have $\begin{pmatrix} L \\ l \end{pmatrix}$ of at least length $L$.

With MLP, nonlinearities can increase the rank of the inputs. But MLP with a high lipschitz constant lead to overfitting.

Self-attention networks behave like an ensemble of shallow-netowrks.

