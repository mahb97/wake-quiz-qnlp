# Wake Quiz QNLP Playground

Quantum natural language processing (QNLP) and controllable language generation for the quiz chapter of *Finnegans Wake* (Book I, Chapter 6).

This repository accompanies `project.md`, which contains a detailed overview of the aims, corpus design, and methodology. 

---

## 1. Objectives

1. To construct a documented corpus of question answer pairs from the quiz chapter of *Finnegans Wake*, including macro level pairs and micro level segments, with optional morpheme annotations.
2. To train a small downstream generator on top of a pretrained language model that produces quiz style answers conditioned on user questions and style control inputs.
3. To implement a QNLP compatibility model, using lambeq or a related toolkit, that assigns higher compatibility scores to authentic quiz question answer pairs than to mismatched or purely generative pairs.
4. To integrate the generator and the QNLP layer into an interactive demo that exposes style control, compatibility scores, and simple diagnostics to the user.

For a full statement of research questions and diagnostic metrics, see `project.md`.

---

## 2. Repository Structure

The intended structure is as follows.

```text
wake-quiz-qnlp/
  README.md
  project.md

  data/
    raw/
      fw_i6_original.txt
    interim/
      fw_i6_qa_core.jsonl
      fw_i6_segments.jsonl
    processed/
      fw_i6_morphemes.jsonl
      lm_qa_pairs.jsonl
      qnlp_pairs.jsonl
      styles.json

  notebooks/
    01_corpus_fw_i6.ipynb
    02_lm_finetune.ipynb
    03_qnlp_lambeq.ipynb
    04_demo_dev.ipynb

  src/
    wakequiz/
      __init__.py
      data_types.py
      data_utils.py
      lm_training.py
      qnlp_model.py
      demo_app.py

  configs/
    lm_config.yaml
    qnlp_config.yaml

  requirements.txt
  .gitignore
