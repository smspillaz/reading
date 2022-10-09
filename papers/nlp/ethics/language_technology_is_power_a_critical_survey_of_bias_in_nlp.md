---
title: "Language (Technology) is Power - A Critical Survey of &quot;Bias&quot; in NLP."
venue: "ACL"
pages: "5454-5476"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/acl/BlodgettBDW20"
doi: "10.18653/V1/2020.ACL-MAIN.485"
ee: "https://doi.org/10.18653/v1/2020.acl-main.485"
url: "https://dblp.org/rec/conf/acl/BlodgettBDW20"
authors: ["Su Lin Blodgett", "Solon Barocas", "Hal Daum\u00e9 III", "Hanna M. Wallach"]
sync_version: 3
cite_key: "conf/acl/BlodgettBDW20"
---

Survey 146 papers about "bias" and find that:
1. They are often vague, inconsistent and lacking normative reasoning
2. Proposed quantitative techniques are poorly matched to their motivations

Use a previously developed taxonomy of bias harms:

 - Allocational: Automated system allocates resources (eg, credit or opportunities) in an unfair way to different groups
 - Representational: When a system represents a group in a less favorable light than others, demeans them or fails to recognize their existence.

Categorize papers descriptions of "bias" as follows :

- Allocational: When an automated system allocates resources unfairly to different social groups.
- Representational
	- Stereotyping: Negatve generalizations
	- Differences in system performance for different social groups
	- language that misrepresents the distribution of different groups in a population or
	- language that is denigrating towards a particular group
- Questionable correlations: Between system behaviour and features of language associated with social groups
- Vague descriptions of bias or gender: Don't properly describe


Many papers focus on stereotyping or other representational harms as opposed to allocational harms =.

# Findings

## What motivations exist?

- All six categories above

Papers usually don't include normative reasoning and instead are concerned about system performance (eg, the system works less well on group X than it does on group Y) and claiming that this is bias.

Papers that do state motivations are unclear on which biases actually harm people and in what way.

Motivations conflate allocational and representational harms.

## Paper techniques

Techniques are usually not well grounded on relevant literature outside of NLP. What could you rely on?
 - Double bind facing women
 - "angry black women" stereotype
 - Implicit association test

## Problem / solution mismatch

Even though 21% of papers include allocational harms, only four actually propose a technique to mitigate this.

## Narrow range of sources of bias

Nearly all papers focus on system predictions as the potential source of bias with also many focusing on bias in datasets.

Almost nobody looks at he normative decisions made during the development and deployment lifecycle. Eg, task definitions used to make a system or dataset, annotation guidelines, evaluation metrics.


# Recommendations

1. Ground work analyzing bias in NLP systems in terms of relevant literature, examining relationship between language and social hierarchices
	1. Treat representational harms as harmful in their own way
2. Describe why system behaviours that are described as bias are harmful
3. Examine language use in practice by engaging with lived experiences. Engage with the actual community

"How are ideologies coproduced"

## Language / Social Hierarchies

1. Without relevant studies outside of NLP, researchers usually measure what is more convenient to measure rather than normative concerns
2. Mitigation of bias should be focused on:
	1. How racial hierarchies and ideologies that maintain them are re-created by technology
	2. How social hierarhcies and language ideologies influence decisiosn made during development and deployment lifecycle
		1. General Assumptions: Which language practices are standard / ordinary or correct
		2. Task definition: Who is the und user
		3. Datasets
		4. Evaluation: How is the system evaluated? What are the implications?
	3. How do NLP systems reproduce or transform "language ideologies". What practices are considered "bad" or "good". Some dialects are seen as "noisy text" and normalize .

## Language Use in Practice

1. How do communities become aware of NLP systems? Are they resisted?
2. What additional costs are carried? For example if there is discrimination, might be focused to change their dialect.
3. Do NLP systems shift power towards oppressive institutions or away from them?
4. Who is involved in the development and deployment of NLP systems? Is there reversibility or amenability?

# Example

Tweet scoring system:

 - If tweets containing features associated with AAE are scored as more offensive than tweets without those features, then this might
	 - Yield negative perceptions of AEE
	 - Result in disproportionate removal of tweets
	 - Cause AAE speakers to incur additional costs if they have to change their language practices to avoid automated removal.


# Discussion

Would you be less hurt if you were discriminated by an NLP system than by a human

 * Katja: It would suck to be overlooked
 * Sam: Hard to ascribe intentionality to an NLP system, from the engineering perspective I just feel bad for the authors because they didn't intend for their system to behave like that.
 * Wei: Predictions of the system are not controlled by the engineers, it would be crucial to introudce the anti-discrimination laws


Should anti-discrimination laws apply to NLP systems?

 * Katja: I'm a bit afraid of laws :-)

* Allocational harms: This is already true. Look at the decisionmaking process. See also EU directives on high risk systems. Needs to affect some fundamental rights.  For representational harms, harder because you have to ascribe intent.