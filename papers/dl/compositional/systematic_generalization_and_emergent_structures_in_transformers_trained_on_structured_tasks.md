---
title: "Systematic Generalization and Emergent Structures in Transformers Trained on Structured Tasks."
venue: "CoRR"
volume: "abs/2210.00400"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2210-00400"
doi: "10.48550/ARXIV.2210.00400"
ee: "https://doi.org/10.48550/arXiv.2210.00400"
url: "https://dblp.org/rec/journals/corr/abs-2210-00400"
authors: ["Yuxuan Li", "James L. McClelland"]
sync_version: 3
cite_key: "journals/corr/abs-2210-00400/Li/2022"
---
In this paper they explore how well a transformer can perform tasks like copying, sorting and hierarchical compositions.

Strong generalization happens to sequences longer than those used in training. You can get this by replacing the stardard positional encoding by labels arbitrarily paired with items in the sequence.

Contributions:
 - They highlight a simple label-based order encoding method in place of positional encoding, this can help to achieve strong length generalization
 - Two-layer causal transformers can learn multiple algorithmic operations. More attention heads at deeper layers has advantages for learning multi-level tasks
 - Systematic decomposition happens, there is also exploitation of shared structure.


## Dataset

![[systematic_generalization_transformers_structured_tasks_dataset.png]]

Item pool covering all combinations of 5 shapes, colors and textures. Sample 5-50 items at random and put them into a sequence

Basically you have an input sequence, then tasks that come from that output sequence. The tasks are:
 - Copy (just copy the sequence)
 - Reverse (reverse the sequence)
 - Group by shape (circles, squares, pentagons)
 - Group by color (red, purple, blue)
 - Sort(shape, color texture): similar to the SQL order by operation on multiple columns

## Label based order encoding

Instead of positional encodings, just use ascending random integer labels. Eg, every item gets a random positional encoding, but they're monotonic. Its sort of like a form of data augmentation.

# Results

![[systematic_generalization_and_emergent_structures_task_specific_item_encoding.png]]

1. Two-layer nodels with label encoding can learn the SORT task and generalize to longer sequences.
2. There seems to be two stages of processing. First layer tends to distribute attention to unsorted items that share the same shape (shape as in the data, not tensor shape) as the query item. This is for the SORT task.
3. Mutli-task learning: Two-layer single-head model can't learn all tasks. Two-layer multi-head models can get good training and genrealization performance.
4. There is also shared task processing and task decomposition across attention layers.
5. There is also task-specific item encoding. Eg for group-by-shape, all of the items with the same shape tend to get grouped together in latent space too. In "sort-by-shape,color,texture" we notice that we have sequences of orange/red/pink/purple/blue, then a group of squares on the left, group of triangles, group of crosses, group of pentagons, group of circles.