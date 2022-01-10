# Interpreting Knowledge Graph Relation Representation from Word Embeddings

=> Building on recent theoretical understanding of word embeddings, we categorise knowledge graph relations into three types and for each derive explicit requirements of their representation


KGs store known facts - binary relations between entities.

We require representations, entities represented as vector embeddings, relations represented as transformations from subject entity to object entity.

Many models developed with gradually increasing success, but not much theoretic rational as to why and how they work.

Consider word embeddings: word2vec . The semantic relations between words manifest as geometric relationships between embeddings. Similar words have close embeddings.

From analogies to relations:

 -> Analogies contain certain common binary word relations similar to KGs
 -> For certain analogies the associated vector offset gives a transformation representing the relation.
 
 
 Identify other semantic relation types:
  -> Relatedness
  -> Specialization
  -> Context shift
  
  Determine this by pairwise difference/similarity between vector.
  
  Categorise the relations into semantic relation types. We can come up with functions which cature this.
  
  S- Relatedness:
   - Both entity embeddings share a common subspace (S) component
   - Project $V_S$ by $P_r$ and compare:
	   - Dot produict: $(P_r e_s)^T(P_r e_o) = e_s^T M_r e_o$
	   - Euclidean Distance: $||P_r e_s - P_r e_o||^2 = ||P_r e_s||^2 - 2e_s^T M_r e_0 + ||P_r e_o||^2$
  
  Specialization / Context Shift:
   - Requires S-Relatedness and relation-specific components $v_r^s, v_r^o$
   - Project on to subspace corresponding to $S$, $v_r^s$ and $v_r^o$
   - Add relation-specific $r = v_r^o - v_r^s$ to transformed embeddings
   - Dot product: $(P_r e_s + r)^T P_r e_o$
   - Euclidean Distance: $||P_r e_s + r - P_r e_o||^2$


Theoretically derived geometric components of relation representations from word-co-occurrence statistics.

Interpretability: associates geometric model components with semantic aspects of relations.