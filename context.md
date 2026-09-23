# Project Context and AI System Prompt

This document provides the complete technical and operational context for our project. If you are an AI assistant helping my teammate, use this text as your system prompt. Do not hallucinate external libraries or unrelated frameworks. Follow only the system architecture, equations, and benchmark data defined here.

If you are my teammate, read this for a complete walkthrough of what our project does, why it exists, and how the entire system works.

---

## High Level Summary

Our project is titled Confidence-Gated Selective Consultation (CG-SC).

It belongs to the field of Large Language Model Multi-Agent Systems. The main goal is to eliminate the severe compute waste and accuracy drops caused by unconditional multi-agent debate. Instead of forcing every user query into an expensive multi-agent discussion, our system evaluates the initial agent's confidence mathematically. Straightforward queries get answered instantly by a single model, while only genuine dilemmas activate peer debate.

---

## The Two Repositories Explained

We maintain two GitHub repositories:

### 1. Public Code and Implementation Repository
URL: https://github.com/ramnnn2006/cg-sc

This is the public-facing repository intended for reviewers and external viewers. It contains only clean, tested code and benchmark datasets:
- Core Python package under cag_delphi_engine.
- Ingested benchmark dataset with 200 real questions from StrategyQA and MMLU Professional Law.
- Clean execution logs and audit reports.
- Live executable scripts for terminal demonstrations.
- Native slate monochrome Mermaid flowchart in the README.
- Clean git history with a single initial commit dated yesterday and zero badge clutter.

### 2. Comprehensive Research and Academic Repository
URL: https://github.com/ramnnn2006/rp

This is the full research repository containing all background material, raw literature, and formal academic drafts:
- 16 full research paper PDFs in the papers directory.
- Complete IEEE conference paper draft in LaTeX format.
- Forensic critiques of 15 multi-agent literature papers.
- Formal mathematical proofs for confidence bounds and consensus stability.
- Comprehensive review reports and evaluation tables.

---

## The Core Research Problem

Our work builds on and addresses a fatal limitation in current multi-agent systems, particularly the base paper by Lee and Kwon (2026), published in Applied Sciences.

Lee and Kwon introduced a Delphi consensus model using diverse agent personas. However, their system relies on unconditional consultation:
- Every query, no matter how simple or factual, unconditionally activates a full committee of 4 to 6 agents across 3 debate rounds.
- This creates massive token inflation, consuming 3,200 to 7,000 tokens per prompt compared to roughly 300 tokens for a single model.
- More seriously, it causes debate degeneration. When simple factual questions enter an adversarial debate, peer noise and conflicting viewpoints confuse the agents. They frequently discard the correct answer in favor of a consensus hallucination.

In our empirical evaluation on StrategyQA, unconditional debate caused single-agent accuracy to drop from 70% down to 43%.

---

## How Confidence-Gated Selective Consultation Works

We solve this using a three-tier architecture:

### 1. Epistemic Confidence Gate
When a query enters the system, the primary agent generates an initial response alongside its next-token probability distribution. We evaluate three distinct signals to compute an epistemic confidence score C(x) between 0.0 and 1.0:

- Normalized Shannon Token Entropy:
Measures the sharpness of the probability distribution over generated tokens. High entropy indicates uncertainty, while low entropy indicates certainty.
- Semantic Consistency:
Samples multiple outputs at low temperature to verify whether the agent reaches identical conclusions consistently.
- Fast Reasoning Rubric:
Evaluates whether the chain-of-thought steps logically support the conclusion.

The composite confidence formula is:
C(x) = 0.50 * (1 - Normalized Entropy) + 0.30 * Agreement + 0.20 * Rubric

### 2. Dynamic Routing Topologies
Based on the confidence score C(x), the query is routed through one of three pathways:

- Solo Fast-Path (Confidence >= 0.65):
Straightforward query with high certainty. The initial agent's answer is returned immediately in about 0.8 seconds. Zero peer tokens are spent.
- Dyadic Challenger (Confidence between 0.50 and 0.65):
Moderate ambiguity. Two agents (proposer and adversarial critic) run a single fast verification round to catch potential hallucinations.
- Delphi Committee (Confidence < 0.50):
Genuine dilemma with low certainty. Activates the full multi-agent committee.

### 3. Competing Values Framework Personas
When the committee is summoned, we avoid duplicate or echo-chamber agents. Grounded in Cameron and Quinn's Competing Values Framework, we deploy four orthogonal personas:
- Clan Persona: Emphasizes internal ethics, human safety, and harm reduction.
- Adhocracy Persona: Emphasizes flexibility, innovative thinking, and adaptive strategies.
- Market Persona: Emphasizes utility, fiscal cost efficiency, and measurable deliverables.
- Hierarchy Persona: Emphasizes statutory rules, procedural compliance, and evidentiary standards.

### 4. Early Stopping via Kendall Concordance
Traditional Delphi systems run for a predetermined number of rounds. Our engine computes Kendall's concordance coefficient (Kendall's W) over the agents' ranked preferences after each round. As soon as Kendall's W reaches 0.70 or higher, consensus is reached and the debate exits immediately, saving substantial tokens.

---

## Real Benchmark Results Across 200 Academic Questions

We evaluated the architecture on 200 real academic questions: 100 questions from StrategyQA (strategic commonsense reasoning) and 100 questions from MMLU Professional Law (US Bar Examination legal scenarios).

### Summary Table
- Solo Agent (Single Model): 58.50% accuracy, 291.2 tokens per query.
- Unconditional Delphi (Base Paper): 44.50% accuracy, 3182.0 tokens per query.
- CG-SC (Our Framework): 57.00% accuracy, 1562.9 tokens per query.

### Key Empirical Findings
- Net Token Reduction: Saved 50.88% of tokens across all 200 questions compared to the base paper (1,562 tokens vs 3,182 tokens).
- Eliminating Debate Degeneration on StrategyQA: Single-agent accuracy was 70.0%. Unconditional debate caused accuracy to collapse to 43.0% due to peer noise. Our confidence gating shielded straightforward questions and kept accuracy at 69.0% while saving 56.8% of tokens.
- Handling Complex Dilemmas on MMLU Law: Professional law questions were genuinely ambiguous, activating the committee on 79.5% of queries. Even under frequent committee activation, early stopping via Kendall's W saved 45.3% of tokens compared to exhaustive debate.

---

## Project Codebase and Key Files

- cag_delphi_engine/gating.py: Epistemic confidence estimation, token entropy, and routing threshold logic.
- cag_delphi_engine/topology.py: Topology switching (Solo, Dyadic, Delphi) and belief sharing.
- cag_delphi_engine/consensus.py: Kendall's concordance coefficient calculation and early-exit stopping.
- cag_delphi_engine/diversity.py: Competing Values Framework persona definitions and instructions.
- run_full_dataset_execution.py: Ingests all 200 real questions, executes the three baseline pipelines, and generates full audit logs.
- cag_delphi_live_showcase.py: Real-time terminal demo illustrating step-by-step deliberation on medical and legal dilemmas.
- simulation_testbench.py: Monte Carlo evaluation calculating 95% confidence intervals across hundreds of runs.
- data/real_benchmarks/real_decision_benchmarks.jsonl: Ingested academic benchmark dataset.
- data/real_benchmarks/FULL_EXECUTION_AUDIT_REPORT.md: Detailed per-question execution and routing log.

---

## Frequently Asked Questions and Answers

Question: What is the main innovation over previous work?
Answer: Previous systems consult all agents unconditionally, which wastes compute and degrades accuracy on easy questions. We introduce epistemic confidence gating to selectively consult peer agents only when the primary agent is genuinely uncertain.

Question: Why did unconditional debate perform worse than a single agent on StrategyQA?
Answer: Factual commonsense questions have clear, objective answers. Forcing agents to debate simple facts introduces noise and contrarian reasoning, confusing the models and causing them to abandon correct initial answers.

Question: How does early stopping work?
Answer: After each Delphi round, we compute Kendall's concordance coefficient across the agents' ranked preferences. If Kendall's W reaches 0.70, it proves strong consensus, allowing the debate to terminate early and save tokens.
