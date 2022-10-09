---
title: "DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale."
venue: "ICML"
pages: "18332-18346"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/RajbhandariLYZA22"
ee: "https://proceedings.mlr.press/v162/rajbhandari22a.html"
url: "https://dblp.org/rec/conf/icml/RajbhandariLYZA22"
authors: ["Samyam Rajbhandari", "Conglong Li", "Zhewei Yao", "Minjia Zhang", "Reza Yazdani Aminabadi", "Ammar Ahmad Awan", "Jeff Rasley", "Yuxiong He"]
sync_version: 3
cite_key: "conf/icml/RajbhandariLYZA22"
---
Due to the very large model size of MoE and their unique architecture, providing fast MoE inference is challenging.

DeepSpeec MoE is an end-to-end trianing and inference solution, including a novel MoE architecture design and compression technique to reduce the model size up to 3.7x and hihgly optimized inference system that provides 7.3x better latency.

The main challenge is MoE's memory requirement and parameter count. MoE-based Switch-Base has 10x more parameters than T5-large. They have much lower "parameter efficiency". You need thousands to GPUs just to fit the model state for training. Memory bandwidth scaling is also an issue.

#### Improving Parameter Efficiency

The paper proposes the PR-MoE architecture, standing for "Pyramid Residual Mixture of Experts". Effecitvely in a Pyramid-Residual MoE, you start out with a small number of experts on the first few layers, then scale up the number of experts on later layers., with a residual MLP connection on each layer.

The intuition for this design comes from a "first-half MoE/second-half MoE" experiment shown in Figure 2, where it is shown that having the mixture of experts at the last layers still scales about as well as having them on all layers, but is better than having them only at the first layers.

The authors also experimented on just having the MLP connection and using the MoE as residual as opposed to the layer in and of itself. This does about as well as using two experts.

#### Desinging a training infrastructure for heterogeneous layer layouts

#### DeepSpeed MoE inference: serving MoE at scale and speed

The main issue is communication overhead. There is a need for all-to-all reduction. The idea is to increase the communication volume by doing local (GPU-only) reduction, then slicing the GPU chunks and moving them across GPUs within a single node and doing an intra-node reduction. Then we can slice across nodes and move across nodes to do an inter-node reduction.