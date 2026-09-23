# Project Context and Technical Blueprint

This document contains the complete technical architecture, empirical data, and development roadmap for our project. 

If you are an AI assistant helping my teammate, treat this file as your master system prompt. Do not invent external frameworks or assume generic multi-agent libraries. Ground all explanations and advice directly in the equations, routing logic, benchmark numbers, and pending technical tasks documented below.

If you are my teammate, use this as your comprehensive reference guide to understand every part of the system, what is already working, and what actual engineering work remains to be done.

---

## High Level Summary

Our project is called Confidence-Gated Selective Consultation (CG-SC).

It addresses a major efficiency and accuracy bottleneck in Large Language Model Multi-Agent Systems. Most current frameworks treat multi-agent collaboration as a static, always-on process where every query triggers an exhaustive debate among multiple agents. This creates massive token waste and introduces peer noise that confuses models on simple factual questions.

Our system introduces an epistemic confidence gate. It mathematically scores how certain a primary model is about its answer. Straightforward queries are resolved immediately on a fast solo path using zero peer tokens. When a query is genuinely ambiguous or presents a complex tradeoff, the gate routes it to specialized agent personas that deliberate and exit early as soon as mathematical consensus is reached.

---

## The Two Repositories and Their Roles

We maintain two distinct GitHub repositories to separate clean public artifacts from internal research materials:

### 1. The Public Code Repository
URL: https://github.com/ramnnn2006/cg-sc

This repository is public facing and holds only clean, production-grade code and verified benchmark data:
- The core Python decision package under cag_delphi_engine.
- The 200-question academic benchmark dataset from StrategyQA and MMLU Professional Law.
- Execution traces, token audit reports, and testbench runners.
- Live CLI demonstration scripts.
- A clean README with a slate monochrome Mermaid architecture diagram.
- A clean git history with a single initial commit and zero badges.

### 2. The Internal Research Repository
URL: https://github.com/ramnnn2006/rp

This repository contains our comprehensive research archive and academic writing:
- 16 full research paper PDFs in the papers folder.
- Our base paper: Lee and Kwon (2026), published in Applied Sciences.
- Detailed technical critiques of 15 supporting papers.
- Mathematical formulations and convergence proofs.
- The complete IEEE two-column conference paper draft in LaTeX.
- Internal handover documents, master study guides, and review evaluation reports.

---

## The Core Problem in Existing Systems

Our research builds directly upon and resolves a fatal flaw in the base paper by Lee and Kwon (2026, Applied Sciences), titled "Differentiated Effects of Agent Diversity on Collective Decision-Making in LLM-Based Multi-Agent Delphi Systems".

Lee and Kwon showed that using diverse agent personas improves consensus quality on complex problems. However, their architecture forces unconditional consultation:
- Every query, regardless of complexity or certainty, triggers a full committee of 4 to 6 agents across 3 fixed rounds of debate.
- This creates severe token inflation, burning between 3,200 and 7,000 tokens for queries that a single model can answer accurately in 300 tokens.
- It causes debate degeneration. On factual commonsense questions, introducing conflicting viewpoints and contrarian arguments causes agents to doubt correct facts. They frequently talk each other out of the right answer.

In our empirical evaluation on StrategyQA, unconditional debate caused accuracy to drop from 70% down to 43% simply due to peer noise.

---

## The Confidence-Gated Architecture

We solve these problems through a three-tier architecture that dynamically adapts based on epistemic certainty.

### 1. Epistemic Confidence Estimation
When a user submits a query, a primary agent produces an initial candidate answer along with its next-token probability distribution. We calculate a composite confidence score C(x) between 0.0 and 1.0 using three complementary signals:

- Normalized Shannon Token Entropy:
We calculate the entropy across the probability distribution of generated tokens. A sharp distribution indicates high model confidence, while a flat distribution indicates uncertainty. We invert and normalize this to a certainty score between 0 and 1.
- Semantic Consistency:
We sample candidate completions at low temperature and measure whether the agent reaches identical conclusions consistently. High consistency signals factual stability.
- Fast Reasoning Rubric:
A lightweight evaluation check that verifies whether the reasoning chain logically supports the final conclusion without self-contradiction.

The composite confidence formula is:
C(x) = 0.50 * (1 - Normalized Entropy) + 0.30 * Agreement + 0.20 * Rubric Score

### 2. Dynamic Routing Pathways
The confidence score determines which execution pathway handles the query:

- Solo Fast-Path (Confidence >= 0.65):
The query is straightforward. The primary agent's initial answer is returned immediately. Response latency is roughly 0.8 seconds and zero peer tokens are consumed.
- Dyadic Challenger (Confidence between 0.50 and 0.65):
The query contains moderate ambiguity. We summon a single adversarial critic agent. The proposer and critic complete one focused verification round to catch hallucinations without spinning up a full committee.
- Delphi Committee (Confidence < 0.50):
The query presents a genuine dilemma with high uncertainty. We summon a four-agent committee to deliberate.

### 3. Competing Values Framework Personas
When the Delphi committee is summoned, we do not use identical agents. Drawing on Cameron and Quinn's Competing Values Framework, we deploy four orthogonal personas:
- Clan Persona: Prioritizes internal ethics, human safety, patient autonomy, and harm reduction.
- Adhocracy Persona: Prioritizes flexibility, innovation, systemic adaptation, and unconventional solutions.
- Market Persona: Prioritizes external utility, fiscal efficiency, and measurable deliverables.
- Hierarchy Persona: Prioritizes statutory rules, legal precedents, and procedural compliance.

### 4. Early Stopping via Kendall Concordance
Rather than running a fixed number of rounds, our engine computes Kendall's concordance coefficient (Kendall's W) over the agents' ranked preferences after each round. As soon as Kendall's W crosses 0.70, strong consensus is proven and the debate exits immediately, saving substantial tokens.

---

## Real Benchmark Results Across 200 Academic Questions

We evaluated our architecture across 200 real academic questions: 100 questions from StrategyQA (strategic commonsense reasoning) and 100 questions from MMLU Professional Law (US Bar Examination legal scenarios).

### Verified Performance Summary
- Solo Agent (Single Model): 58.50% accuracy, 291.2 tokens per query.
- Unconditional Delphi (Base Paper): 44.50% accuracy, 3182.0 tokens per query.
- CG-SC (Our Framework): 57.00% accuracy, 1562.9 tokens per query.

### Key Empirical Findings
- Token Savings: Slashed average token consumption by 50.88% across all 200 questions compared to the base paper (1,562 tokens vs 3,182 tokens).
- Debate Degeneration Eliminated: On StrategyQA, single-agent accuracy was 70.0%. Unconditional debate in the base paper collapsed accuracy to 43.0% due to peer noise. Our confidence gating shielded straightforward questions, maintaining 69.0% accuracy with 56.8% token savings.
- Handling Complex Law Queries: On MMLU Professional Law, questions were genuinely difficult and triggered the committee 79.5% of the time. Even under heavy committee usage, early stopping via Kendall's W saved 45.3% of tokens compared to exhaustive debate.

---

## Actual Technical Work Left to Do (Project Engineering Roadmap)

This section lists the real technical engineering, mathematical research, and system implementation tasks remaining on the project beyond review presentations.

### 1. Local Edge Hardware Deployment and Profiling
Currently, our benchmark runs use cloud API calls and simulated logit distributions for calibration. We need to deploy small open-weight language models locally on physical edge hardware:
- Models to evaluate: Llama 3.2 (1B and 3B parameters), Phi 3.5 mini (3.8B), and Mistral 7B quantized using 4-bit AWQ or GGUF.
- Runtime engines: Implement inference pipelines using llama.cpp and Ollama.
- Hardware profiling: Measure physical RAM and VRAM footprint, CPU temperature, power consumption in watts, and token generation speed on a standard laptop CPU and a mini PC.
- Goal: Demonstrate that our confidence gate enables multi-agent decision systems to run efficiently on resource-constrained consumer hardware without thermal throttling or memory exhaustion.

### 2. Empirical Logit and Entropy Calibration for Closed APIs
Commercial closed-source APIs (like OpenAI and Anthropic) often restrict or omit raw next-token logit distributions:
- Problem: The normalized Shannon entropy component in our formula assumes access to full vocabulary logits.
- Work to do: Build an empirical calibration bridge that calculates surrogate entropy using top-5 logprobs where available, or calibrated verbalized uncertainty scoring when logprobs are absent.
- Validation: Compare closed-API surrogate entropy against full-vocabulary PyTorch logit distributions using an open model (like Llama 3.1 8B) on the same 200 questions to quantify calibration error.

### 3. Systematic Hyperparameter Optimization for Confidence Weights
Our confidence formula currently uses static heuristic weights: w1 = 0.50 (entropy), w2 = 0.30 (consistency), w3 = 0.20 (rubric).
- Work to do: Implement a Bayesian optimization sweep using Optuna or grid search across a dedicated validation split.
- Domain-specific tuning: Investigate whether optimal weights shift across domains. For example, determine if legal compliance tasks benefit from a higher rubric weight, while arithmetic reasoning benefits from a higher consistency weight.
- Threshold sensitivity analysis: Map the exact Pareto frontier of accuracy versus token cost across gating thresholds from tau = 0.30 to tau = 0.85 in increments of 0.05.

### 4. Expansion to Quantitative and Coding Benchmarks
Our current evaluation covers strategic commonsense reasoning (StrategyQA) and legal judgment (MMLU Professional Law). We need to test how the confidence gate performs on deterministic, ground-truth verifiable domains:
- Mathematical reasoning: Evaluate on 100 questions from GSM8K or MATH.
- Code generation: Evaluate on HumanEval or MBPP, measuring whether unit test execution can replace or augment the rubric evaluation signal.
- Hypothesis: Test whether deterministic tasks exhibit even sharper entropy drops on correct answers, potentially yielding higher token savings on code and math tasks.

### 5. Dynamic Budget-Constrained Threshold Shifting
Currently, the routing threshold tau is constant (tau = 0.65).
- Work to do: Design an adaptive threshold controller that adjusts tau dynamically based on a remaining token budget or latency deadline.
- Behavior: If an application has an emergency latency deadline of 1.0 second or a remaining token budget under 500 tokens, the controller automatically increases tau, forcing queries onto the solo or dyadic path to guarantee budget compliance.

### 6. Multi-Turn Dialogue Memory and State Persistence in Delphi Rounds
Currently, during Delphi rounds, agents evaluate responses based on the immediate prior round summary.
- Work to do: Implement a structured memory buffer that tracks the evolution of each agent's belief coordinates and arguments across rounds.
- Preventing argument recycling: Ensure agents detect and discard previously refuted counterarguments rather than repeating them in later rounds.
- Memory compression: Test whether vector summarization of round transcripts prevents token bloat when extended deliberation is required.

### 7. Human-in-the-Loop Fallback for Persistent Deadlock
In rare cases where a dilemma fails to reach Kendall's W = 0.70 after maximum Delphi rounds, the system must not hang or guess blindly.
- Work to do: Build a human-in-the-loop escalation pipeline.
- Output generation: Generate an automated differential report summarizing the core conflict (for example, Clan safety concerns versus Market cost constraints) and queue it for human administrator review.

### 8. Final IEEE Camera-Ready Paper Submission
Complete the academic publication package in the rp repository:
- Convert high-resolution Matplotlib evaluation plots into vector PDF figures.
- Incorporate empirical edge hardware profiling numbers and hyperparameter ablation tables into Section V of the LaTeX manuscript.
- Run citation cross-checking and formatting compliance checks against the target IEEE conference track template.

---

## Codebase File Map

- cag_delphi_engine/gating.py: Epistemic confidence estimator, token entropy calculations, and routing threshold logic.
- cag_delphi_engine/topology.py: Topology switching (Solo, Dyadic, Delphi) and inter-agent message passing.
- cag_delphi_engine/consensus.py: Kendall's concordance coefficient calculation and early-exit stopping logic.
- cag_delphi_engine/diversity.py: Competing Values Framework persona definitions and prompt engineering.
- run_full_dataset_execution.py: Executes the full 200-question academic benchmark and logs per-query metrics.
- cag_delphi_live_showcase.py: Real-time terminal demo illustrating step-by-step deliberation on medical and legal dilemmas.
- simulation_testbench.py: Monte Carlo testbench calculating 95% confidence intervals across hundreds of runs.
- data/real_benchmarks/real_decision_benchmarks.jsonl: Academic benchmark dataset containing 200 questions.
- data/real_benchmarks/FULL_EXECUTION_AUDIT_REPORT.md: Full question-by-question audit log with token counts and routing decisions.

---

## Frequently Asked Questions for Technical Discussions

Question: What is the primary theoretical contribution of this work?
Answer: Previous multi-agent frameworks operate on static graphs where every query unconditionally triggers multi-agent debate. Our contribution is showing that unconditional debate is actively harmful on factual queries due to debate degeneration, and introducing epistemic confidence gating to dynamically route queries between single-agent and multi-agent pathways based on predictive certainty.

Question: Why did unconditional debate achieve lower accuracy than a single model on StrategyQA?
Answer: StrategyQA questions are multi-step commonsense problems with factual ground truths. When multiple agents debate simple facts, contrarian viewpoints and adversarial noise introduce doubt, causing the models to abandon correct initial reasoning in favor of a consensus hallucination. Confidence gating shields these queries from unnecessary debate.

Question: How does Kendall's concordance coefficient decide early stopping?
Answer: After each Delphi round, agents rank candidate decisions. We compute Kendall's W across their rankings. A value of W >= 0.70 indicates strong agreement across orthogonal personas, proving that further debate rounds will yield diminishing returns and allowing the engine to stop immediately.
