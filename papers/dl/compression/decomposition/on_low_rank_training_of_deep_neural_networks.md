---
title: "On Low-Rank Training of Deep Neural Networks"
---
Do SVD and a modified L2 regularization.
-   Eg, you have $W_{t + 1} = U_{t + 1}V_{t + 1}$
-   Gradient descent in the factorised setting does not align well with vanilla gradient descent
-   At inference time, the complexity goes from $O(mn)$ to $O(mr + rn)$, where $r = \min(m, n)$.
-   Initialization: Take the square root of the eigenvalues and multiply backk out. Spectral initialization
-   L2 regularization: Penalize frobenius norm of $||UV^T||$. Don’t penalize each weight matrix separately (note, kind of similar to what we did in our sparsity paper).