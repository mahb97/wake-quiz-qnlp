# Wake Quiz QNLP Playground  
## Quantum Compositional Semantics and Style Control in *Finnegans Wake*

## Project Overview

This project investigates how quantum natural language processing (QNLP) and controllable language generation can be combined in order to model and imitate the stylistic and semantic behaviour of the quiz chapter of *Finnegans Wake* (Book I, Chapter 6). The chapter presents a sequence of question answer exchanges in a highly distinctive Wake register, which makes it a natural testbed for experiments that treat question answer pairs as structured semantic objects rather than as purely sequential text. The project develops a small but carefully annotated dataset from this chapter, trains a downstream language model that generates Wake like quiz answers from prompts, and then introduces a QNLP component that evaluates the compatibility of generated answers with the original Wake quiz structures. The final outcome is an interactive demo that allows users to type questions, select stylistic settings, and observe how the QNLP layer assesses the Wake likeness of the outputs.

## Aims and Contributions

- To construct a well documented corpus of question answer pairs from the quiz chapter of *Finnegans Wake*, including macro question answer alignments and finer grained intra question call response segments, with optional morpheme level annotations.
- To train a lightweight downstream generator on top of a pretrained language model that produces Wake like quiz answers conditioned on user questions and style control signals.
- To implement a QNLP model, using lambeq or a similar toolkit, that scores the compositional compatibility of question answer pairs, distinguishing authentic Wake pairs from mismatched or purely generative pairs.
- To integrate these components into an interactive web based interface that exposes style control, QNLP scoring, and simple diagnostic visualisations to the user.
- To provide a compact, reproducible research artefact that demonstrates how compositional quantum inspired models can be used not as full generators, but as evaluators and diagnostics layered on top of classical neural language models.

## Research Questions

1. To what extent can a small downstream fine tune on the quiz chapter of *Finnegans Wake* enable a pretrained language model to generate question answer pairs that are recognisably Wake like in terms of surface form, local coherence, and lexical innovation.
2. Can a QNLP model, trained on a limited set of carefully curated question answer pairs from the quiz chapter, learn to assign higher compatibility scores to authentic Wake quiz pairs than to mismatched or artificially generated pairs for the same questions.
3. How do style control mechanisms, such as soft prompts or lightweight adapters for different authors or registers, affect the distributional and morphological properties of generated answers, and how do these shifts correlate with QNLP compatibility scores.
4. What does the joint behaviour of the generator and the QNLP evaluator reveal about the limits of current language models when they attempt to approximate the syntactic, semantic, and morphological strangeness of *Finnegans Wake*.

## Data and Corpus Construction

The core dataset is derived from Book I, Chapter 6 of *Finnegans Wake*, commonly referred to as the quiz chapter. The chapter is segmented into:

- **Macro question answer pairs**  
  Each quiz item is aligned as a pair consisting of a question block and its corresponding answer block, preserving the original Wake text as faithfully as possible.

- **Micro call response segments**  
  Within individual questions and answers, shorter segments are identified where the text naturally divides into subclauses or list like sequences, which creates additional aligned instances for training and evaluation.

- **Morpheme level annotations (optional but recommended)**  
  Building on an existing morpheme dataset for the same chapter, each answer segment can be enriched with morpheme segmentations and basic morphological tags in order to support later quantitative analysis of Wake specific blending, compounding, and neologism patterns.

### Basic English as a partial baseline

The project uses Ogden’s Basic English as one operationalisation of a “plain” baseline, but it does not treat Basic English as a neutral or universal representation of simplicity. Basic English is a historically situated, male designed controlled vocabulary that encodes early twentieth century Anglophone social imaginaries, including a binary and asymmetrical treatment of gender. In Ogden’s lists, for example, “male” appears among the hundred “general” qualities, while “female” is relegated to a separate list of “opposites” alongside items such as “bad,” “bent,” “cruel,” “dead,” “dirty,” “false,” “feeble,” and “ill.” The vocabulary for people and relations similarly reflects a heteronormative, nuclear family model, with “married,” “husband,” “wife,” “father,” and “mother” foregrounded, and labour organised around roles such as “manager,” “secretary,” “servant,” and “worker.” Basic English therefore offers not an ideologically empty core but a constrained lexicon shaped by a particular white, male, British perspective on what counts as “basic.”

When this project computes Basic based diagnostics, such as the proportion of tokens in a generated answer that belong to the Basic English list or the distribution of tokens across clusters induced from that list, the resulting measures are not interpreted as direct proxies for simplicity, naturalness, or accessibility. Instead they are treated as indices of how far a given text conforms to Ogden’s constrained semantic grid. Moving toward the Basic end of the style slider is therefore read as moving toward a historically specific, male centred controlled language, rather than toward an abstract notion of linguistic clarity. Conversely, texts that fall away from the Basic vocabulary may be doing so in virtue of complexity, but they may also be refusing the constraints of that grid in ways that matter for gendered and embodied characterisation. Any use of Basic English as a baseline in this project is therefore accompanied by explicit acknowledgement of its bias and by qualitative readings that attend to where and how the Basic lexicon fails to accommodate subjectivities that do not sit comfortably within Ogden’s categories.

Additional comparative material can be introduced as optional extensions, such as more conventional prose passages by Joyce or other modernist authors, which can supply contrastive training data for style control mechanisms. However, the minimal viable dataset focuses on the quiz chapter itself and its internal variation.

## Methods

### Classical Language Model Component

A pretrained causal language model is used as the base generator. On top of this base model, a small downstream task is defined:

- **Input**  
  A prompt that encodes the target style and the user question, for example through a format such as  
  `<STYLE=FW_I6_QUIZ>\nQ: [question]\nA:`

- **Output**  
  A continuation that is trained to reproduce the corresponding Wake answer segment.

A small parameter efficient fine tune is applied, for instance through LoRA adapters or soft prompt tuning, which updates only a limited subset of parameters while keeping the base model frozen. The training data consists primarily of the macro question answer pairs from the quiz chapter, optionally augmented with synthetic or paraphrased questions and with a limited amount of non Wake question answer examples that are tagged with contrasting style labels. The objective is to obtain a generator that, given a new question and a suitable style tag, produces an answer in a recognisably Wake like quiz register.

Style control for the interactive demo can be implemented by learning separate style embeddings or adapters for different regimes, such as neutral prose, generic Joyce prose, and quiz chapter Wake, and then interpolating between these embeddings in order to realise a continuous style slider in the user interface.

## Stylometry and LLMs

*Just some thoughts, the essential: since literally no one else writes this well, I shall take a moment of silence. This was published on 11th of November, absolute gold.*

O’Sullivan, J. Stylometric comparisons of human versus AI-generated creative writing. *Humanit Soc Sci Commun* 12, 1708 (2025). https://doi.org/10.1057/s41599-025-05986-3. https://rdcu.be/eP7yl

O’Sullivan’s recent study takes Beguš’s experimental narrative corpus as a testbed and stages a tightly controlled stylometric investigation in which short stories written by Mechanical Turk workers and by GPT-3.5, GPT-4, and Llama 70b respond to two Pygmalion prompts in which humans fall in love with their own or someone else’s artificial creation, and in which Burrows’s Delta over the one hundred most frequent words, together with hierarchical clustering and multidimensional scaling, is used to map the resulting stylistic space. The visual outcome is blunt and intellectually awkward for anyone who wants to claim seamless human machine convergence, since the human stories spread across the dendrogram and the multidimensional scaling plane in a messy, heterogeneous cloud, while each model produces a tight and internally coherent cluster in its own region of that space, with GPT-4 in particular forming a compact stylistic bloc; occasional incursions by GPT-3.5 samples into the human zone are treated as interesting edge cases rather than as evidence that the structural separation between human and machine texts has dissolved.

What makes the article valuable is not a rush toward novel features but the precision with which an established method is deployed and the refusal to inflate the significance of neat plots. The analysis uses classic Delta on frequent words, foregrounds its own constraints, and releases scripts and data so that every dendrogram and scatter plot can be re run, re weighted, or contradicted by others. The corpus is explicitly described as contrived and limited, since it rests on predefined prompts, on crowdsourced writing that does not claim the status of canonical literature, and on a feature set that privileges function words over syntax, sentence structure, or punctuation; within those boundaries, however, Burrows’s Delta is defended as a robust, field standard tool for the precise question at stake, namely whether contemporary large language models are stylistically indistinguishable from humans when one works at corpus scale, and on the evidence presented they are not, because the models remain fluent, often highly rated, and stylistically uniform in a way that leaves clear signatures in the distribution of their most frequent words.

The sharpest move, and the one that matters most for the Wake Quiz QNLP Playground, is normative rather than technical, since O’Sullivan insists that stylometry belongs in corpus level interpretive work and historical attribution and that it becomes both methodologically brittle and ethically dangerous when it is repurposed as a forensic instrument for academic integrity policing. Student writing is presented as stylistically unstable, shaped by task, time, discipline, health, affect, language background, institutional support, and the often invisible labour of tools and collaborators, so the fantasy of a fixed personal fingerprint that can be monitored for deviations is statistically naive and harmful when it is tied to accusations of misconduct. Stylometry can, and in this article does, clarify how human and machine texts cluster in a particular experimental setting, yet it is declared wholly inadequate as a sole basis for deciding who really wrote a given assignment, and the Wake Quiz QNLP Playground takes that constraint as a design principle, using stylometric and related quantitative diagnostics to map style manifolds, to compare human and model clusters, and to understand how different generators occupy stylistic space, rather than to police individuals or to underwrite institutional surveillance.

## QNLP Component

The QNLP layer is implemented using lambeq or a similar compositional semantics toolkit. A subset of the question answer pairs is selected and processed as follows:

- The question and answer texts are parsed into syntactic structures suitable for a DisCoCat or related categorical model of meaning.
- The resulting diagrams are mapped to parameterised quantum circuits or tensor networks that compute sentence level representations and a scalar compatibility score for each question answer pair.
- The model is trained so that authentic quiz pairings from the corpus are assigned high scores, while mismatched pairs and control pairs receive lower scores.

This QNLP model is not used to generate text. Instead, it acts as an evaluator that takes a question and a candidate answer, whether authentic or generated, and returns a Wake quiz compatibility score. During interactive use, multiple candidate answers produced by the classical language model can be ranked or filtered according to these scores, and the score can be surfaced to the user as an indicator of how closely the generated answer aligns with the learned quiz structures.

### Diagnostic Metrics and Analysis

In addition to the QNLP compatibility scores, the project employs several diagnostic measures:

- Morpheme level statistics, such as type token distributions and the proportion of blended or compound forms, comparing generated answers to authentic quiz answers.
- Distributional measures derived from existing Wake embedding work, such as neighbourhood overlap or geometric drift between generated text embeddings and embeddings of the original quiz chapter.
- Simple surface metrics, including sentence length, punctuation patterns, and lexical overlap with the source corpus.

These diagnostics support both the qualitative interpretation of model behaviour and the evaluation of how style control affects the resemblance between generated and original Wake text.

## Interactive Demo

The project culminates in a small interactive web application, implemented for example with Gradio, that exposes the system to users as follows:

- A text input field for the user question.
- A style control slider that interpolates between at least three regimes, such as neutral prose, Joyce like prose, and quiz chapter Wake style.
- A toggle that enables or disables QNLP based reranking.
- An output panel that displays the selected generated answer, the associated QNLP compatibility score, and optionally one or two diagnostic indicators such as a simple Wake likeness gauge or basic morpheme statistics.

The demo is intended both as a research interface and as a communicative artefact that makes the interaction between classical language modelling and QNLP evaluation visible and inspectable.

## Planned Outputs and Repository Structure

The repository is expected to contain the following components:

- A data directory holding the quiz chapter corpus in a documented JSON or JSONL format, together with any derived segmentation or morpheme annotation files.
- Training scripts and notebooks for the downstream language model component, including configuration files for LoRA or soft prompt tuning.
- QNLP scripts and notebooks that build and train the lambeq based compatibility model, with clear instructions for reproducing the experiments on a classical backend.
- The source code for the interactive demo, designed so that it can be launched locally or in a hosted notebook environment.
- Documentation files, including this project overview, that describe the design rationale, methodological choices, and known limitations.

## Work Plan (don't talk to me about KPIs on the weekend pls)

1. Corpus construction and annotation for the quiz chapter, including macro question answer pairs, micro segments, and integration of existing morpheme data.
2. Implementation and evaluation of the downstream generator with style controlled prompts, using a small parameter efficient fine tuning strategy.
3. Construction and training of the QNLP compatibility model on a selected subset of question answer pairs.
4. Integration of the generator, QNLP evaluator, and diagnostics into a unified interactive demo, followed by small scale evaluation and documentation.

This work plan is intentionally modular in order to allow incremental progress, with each phase producing a usable intermediate artefact that can be inspected and tested independently.

