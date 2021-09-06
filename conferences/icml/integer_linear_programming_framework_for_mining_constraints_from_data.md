# An Integer Linear Programming Framework for Mining Constraints from Data

Structured output prediction problems (e.g., sequential tagging, hierarchical multi-class classification) often involve constraints over the output space. These constraints interact with the learned models to filter infeasible solutions and facilitate in building an accountable system. However, despite constraints are useful, they are often based on hand-crafted rules. This raises a question -- can we mine constraints and rules from data based on a learning algorithm?

In this paper, we present a general framework for mining constraints from data. In particular, we consider the inference in structured output prediction as an integer linear programming (ILP) problem. Then, given the coefficients of the objective function and the corresponding solution, we mine the underlying constraints by estimating the outer and inner polytopes of the feasible set. We verify the proposed constraint mining algorithm in various synthetic and real-world applications and demonstrate that the proposed approach successfully identifies the feasible set at scale. 
In particular, we show that our approach can learn to solve 9x9 Sudoku puzzles and minimal spanning tree problems from examples without providing the rules.

