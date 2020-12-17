# From Ground Truth to Grounded Truth

Computer struggle with deductions about coreference resolution.

 - Not straightforward for non-literal sentences
 - Maybe algorithms need more commonsense, eg, that wine glasses shatter,
   not wooden tables.

Can you understand language understanding just by reading?

 - Minimal semantic assumptions on data/model structure
 - Assumes lots of data.
 - Text-to-text-transfer transformer

Jack of all trades, master of none. Lacking core capabilities crucial for deeper
understanding.

## Generalization

Productivity:

 - Generalize to inputs beyond length seen in training


Compositionality:

 - Recombine parts that you know in new and novel ways
 - You've never seen the objects but you've done all the pieces around it.

## Grounding

 - Understanding text in terms of what you already know
 - Learning a world model and how to refer to it in natural language


Textual data is all we have access to. So if it is working why not.

Lots of work in cognitive sciences argues that much linguistic meaning is
not even in the words. Think of it like an iceberg. Lots of stuff going on
under the surface.

Embodiment: Humans learn language through how we interact with the world - rich world model.

Executable semantic parsing: Text-to-program:

 - Some ideas to map natural language to executable programs
 - Text-to-SQL
 - Text-to-action (navigation, instruction following).

 - Hard to apply this to new language or new situations.

What might an executor for general language look like?

 - Situations
   - Affordances
   - Results

 - Text-based games - grounded language learning environment.

Why text based games?

 - Flexible, easy to code diverse lightweight embodied environments
 - subtract abstract situation understanding 
   - don't want to go to lower-level (muscle movements etc)
 - parsing is easier when natural language is aligned with action language

POC Procedural Text Understanding:

 - Material Science literature - lots of paragraphs about how to make materials
 - Unstructured
 - Complex long technical, assumes expect common sense knowledge
 - Extracting structure is a hard challenge
 - complex coreference issues
 - litte action-graph data


 - Goal is to turn text into action graphs - text operation is, unit is X, etc etc

Grounded Procedure Understanding:

 - Those procedures are like recipes
 - Interpret procedural text as instruuctions for quest
   - Completed by executing procedure correctly.


TextWorld:

 - RL sandbox for custom text cames
 - convenient platform for providing interactive training environment
   - much richer than static text
   - curriculum, state tracking, common-sense knowledge, action constraints
 - supervision shown to be effective in similar problem settings
