---
title: "Diffusion-LM Improves Controllable Text Generation."
venue: "CoRR"
volume: "abs/2205.14217"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-14217"
doi: "10.48550/ARXIV.2205.14217"
ee: "https://doi.org/10.48550/arXiv.2205.14217"
url: "https://dblp.org/rec/journals/corr/abs-2205-14217"
authors: ["Xiang Lisa Li", "John Thickstun", "Ishaan Gulrajani", "Percy Liang", "Tatsunori B. Hashimoto"]
sync_version: 3
cite_key: "journals/corr/abs-2205-14217/Li/2022"
---

# Discussion with the Author

Rounding step: L2 distance

Embedding step: embedding + noise. Why do they have this?

Which model to use for doing the reverse steps? Transformer. Use tricks like ddim to reduce inferemce time.

How many diffusion steps? 2000

How to learn meaningful embeddings? We want x_T to be a standard normal. So penalise if not

We try to predict x0 directly as opposed to x_(t-1). You predict x0 and then do the forward diffusion to x_(t - 1). Clamping happens on the x0.