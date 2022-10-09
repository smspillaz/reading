---
title: "UNITER - UNiversal Image-TExt Representation Learning."
venue: "ECCV"
pages: "104-120"
year: 2020
type: "Conference and Workshop Papers"
access: "closed"
key: "conf/eccv/ChenLYK0G0020"
doi: "10.1007/978-3-030-58577-8_7"
ee: "https://doi.org/10.1007/978-3-030-58577-8_7"
url: "https://dblp.org/rec/conf/eccv/ChenLYK0G0020"
authors: ["Yen-Chun Chen", "Linjie Li", "Licheng Yu", "Ahmed El Kholy", "Faisal Ahmed", "Zhe Gan", "Yu Cheng", "Jingjing Liu"]
sync_version: 3
cite_key: "conf/eccv/ChenLYK0G0020"
---

UNITER model, learned by large-scale pretrinaing over four image text datasets (COCO, Visual Genome, Conceptual Captions, SBU Captions). Four pretrainig tasks: MLM, Masked Region Modelling, Image Text Matching and Word-Region Alignment. Use conditional masking on the pre-training tasks. Also proposes word-region alignment via the use of optimal transport to explicitly encourage fine-grained alignment between word and imave regions during pretraining.

# Architecture
![[uniter_model_architecture.png]]


Adopt transformer as the core of the model.

Enocde imave regions and textual words into a common embedding space with Image Embedder and Text Embedder.

The thing goes into one big transformer encoder. There is no encoder/decoder split - self-attention is cross-attention in this case.

Main Contributons:
 - conditional masking on MLM and MRM (mask only one modality and keep the oher untainted)
 - novel word-region alignment pre-training task via the use of optimal transport.

Image Embeddings:
 - Faster R-CNN + Location Embedding (pooled ROI features)

Word Embeddings:
 - WordPiece + Word Embeddings


## Pretraining tasks

 - Masked Language Modelling (conditioned on image regions). Likelihood based loss.
 - Masked Region Modelling (conditioned on language). Reconstruction/classification/KL-divergence loss.
 - Image-Text Matching. Sample both positive and negative image sentence pairs and learn a matching score. Basically a contrastive learning task - predict 1 if the sentence matches the image, 0 otherwise. We know which sentences match which images in the data.
 - Word-Region Alignment: Calculate the minimum cost of transporting the contextualized image embeddings to the word embeddings.
	 - Why is [[optimal_transport|optimal transport]] interesting in this case?
		 - Self-normalization: all elements of the plan $T \in \mathbb{R}^{T \times K}$ sum to 1
		 - Sparsity: when solved exactly, you get a sparse solution containing (2r - 1) non-zero elements.
		 - Efficiency: Iterative procedures that require only matrix-vector products.
	 - How does it work?
		 - $w$ (the word sequence) and $v$ the image sequence. Consider them as two discrete distribution $\mu = \sum^Ta_i \delta_{w_i}$ $\nu = \sum^T b_i \delta_{v_i}$
		 - The weight vectors $a \in \triangle_T$ and $b \in \triangle_K$ belong to $T$ and $K$ dimensional simplexes, eg, they sum to 1.
		 - Then the optimal transport distance is:
			 - $$\mathcal{L}_{\text{WRA}} = \mathcal{D}_{\text{ot}}(\mu, \nu) = \min_{T \in \Pi(a, b)} \sum^T \sum^K T_{ij} c(w_i, v_j)$$
			 - in this case $\Pi(a, b) = \{T \in R^{T \times K}|T1_m = a, T^T1_n = b\}$ where $1_n$ is an n-dimension one-vector and $c$ is a cost function, for example cosine distance.
			 - Use the IPOT algorithm to approximate the optimal transport distance. This is differentiable and can be used to optimize the parameters of the encoder networks.

## Experimental Results

![[uniter_qualitative_results.png]]

# Ablation Study

Significnat perofrmance improve comes from adding WRA (optimal transport) especially on VQA and RefCOCO+.