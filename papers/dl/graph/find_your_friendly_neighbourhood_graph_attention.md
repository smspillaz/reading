# How to find your friendly neighbourhood: Graph Attention Design with Self-Supervision

Attention over edges: learns relationship importance between nodes

Contributions:
 - Self-supervised attention using edge information
 
 
## Self-supervised attention using edge information.

![[find_your_friengly_neighbourhood_gat_probability.png]]

$e_{ij}$: unnormalized attention before softmax

$P_{ij}$: probability of edge between node $i$ and $j$.

![[super_gat.png]]

Original GAT:
 - GO: $e_{ij}, GO$
 - DP: $e_{ij}, DP$
 - MX: Mixed GO & DP
 - SD: Scaled DP (scaled by number of features)

The probability can be defined by the sigmoid of each unnormalized edge.

Jointly train with cross-entropy

Link-prediction with attention, can be optimized with binary cross entropy on edge labels.

## Analyze GAT's original GO and DP attention.

 - GO attention learns label-agreement better than DP atttention
 - Label-agreement: ideal attention where weights only given to nodes with same label
 - DP predicts edge presence better than GO attention.
 - Which graph attention design: Not proper for encoding self-supervision, need more advanced versions


## Propose recipes to design graph attention concerning homophily and average degree

Quality of edge labels and average degree (quantity). Best performed attention depends on homophily and average degree. Synethic graph results can be generalized to real-world graphs.