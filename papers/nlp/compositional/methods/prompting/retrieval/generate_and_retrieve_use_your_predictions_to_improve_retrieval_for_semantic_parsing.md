---
title: "Generate-and-Retrieve: use your predictions to improve retrieval for semantic parsing."
venue: "CoRR"
volume: "abs/2209.14899"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2209-14899"
doi: "10.48550/ARXIV.2209.14899"
ee: "https://doi.org/10.48550/arXiv.2209.14899"
url: "https://dblp.org/rec/journals/corr/abs-2209-14899"
authors: ["Yury Zemlyanskiy", "Michiel de Jong", "Joshua Ainslie", "Panupong Pasupat", "Peter Shaw", "Linlu Qiu", "Sumit Sanghai", "Fei Sha"]
sync_version: 3
cite_key: "journals/corr/abs-2209-14899/Zemlyanskiy/2022"
---

GandR, a retrieval procedure that retrieves exemplars with outputs similar to the preliminar prediction used to generate a final prediction.

It first generates some preliminary prediction, then retrieves exemplars with outputs similar to the preliminary prediction used to generate the final prediction.

Existing work asks "what is the output for similar inputs". In this work we explore whether there is complimentary information in exemplars that answer the inverse: "what is the input for similar outputs?".

The true output of a sample is in general unknown, so you have to proceed in two steps. First, you make a preliminary prediction using *retrievals with a similar input only.* Then a new set of exemplars is retrieved based on a  relevance measue that balances similar of inputs and *similarity of preliminary prediction and exemplar output*.

![[gandr.png]]

They do relevance scoring by TF-IDF, ie:

$$
R_{ij} = (1 - \alpha)\text{TF-IDF}(x_i, x_j) + \alpha \text{TF-IDF}(\hat y_i, y_j)
$$

where $\hat y_i$ si the preliminary prediction, $x_i$ and $x_j$ are queries and $y_i$ and $y_j$ are targets for those queries. TF-IDF similarity is basically just cosine similarity between TF-IDF bectors.