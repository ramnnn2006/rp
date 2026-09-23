# Teammate Master Speaking and Project Context Guide

Hey, this guide gives you everything you need to know for our Review 2 evaluation. It covers what the project is in plain English, your exact speaking lines, the key numbers to remember, and how to answer questions if the professors ask you directly.

---

## 1. The 60-Second Plain English Summary

Our project is called Confidence-Gated Selective Consultation (CG-SC).

Here is the problem we are solving:
Right now, most multi-agent AI systems (like the base paper by Lee and Kwon published in 2026) force every single question to go through a long, exhausting debate among four to six AI agents across three rounds. 

This causes two big problems:
- It wastes massive numbers of tokens and money. An easy question that could be answered for 300 tokens ends up burning 3,200 to 7,000 tokens.
- It causes debate degeneration. When an easy, factual question is debated by multiple agents, peer noise confuses the models. They talk each other out of the right answer. In StrategyQA, the base paper's accuracy collapsed from 70% down to 43% just because of bad debate noise.

Our solution:
We put a confidence gate in front of the main AI model.
- If the model is confident (score >= 0.65), it answers immediately in 0.8 seconds. Zero peer tokens are spent.
- If it is moderately unsure (0.50 to 0.65), two agents do a quick one-round check.
- If it is a real dilemma with high uncertainty (< 0.50), we summon a four-agent committee to debate, and we stop the debate early as soon as agreement reaches 70%.

---

## 2. Review Presentation Flow (3 Minutes Total)

We are presenting directly from our GitHub repository (ramnnn2006/cg-sc) and our terminal. No boring PowerPoint slides needed.

### Minute 0:00 to 1:30 (My Part)
- I introduce the project title: Confidence-Gated Selective Consultation.
- I explain the flaw in current multi-agent systems from Lee and Kwon (2026): unconditional debate wastes tokens and ruins accuracy on simple facts.
- I point at the Mermaid flowchart on the repository README and explain how the confidence gate calculates certainty using token entropy, consistency, and a rubric check.
- I explain the Solo Fast-Path where confident queries finish in 0.8 seconds.
- I run the benchmark script in terminal to show live question routing.
- I hand over to you by saying: "Now my teammate will walk you through the multi-agent committee and our real benchmark findings."

### Minute 1:30 to 3:00 (Your Part)
- You explain what happens when confidence drops below 0.50 (the Delphi committee).
- You explain the four agent personas (Clan, Adhocracy, Market, Hierarchy).
- You explain early stopping using Kendall's concordance (stopping when agreement hits 70%).
- You present our real benchmark results from the 200-question table.
- You explain how we stopped debate degeneration on StrategyQA (preserving 69% accuracy).
- You summarize our Review 3 next steps (running on a laptop CPU with small 3B models).

---

## 3. Your Exact Word-for-Word Speaking Script

When I hand over to you, take a breath, look at the panel, and say:

"Thanks. Moving into what happens when the confidence score drops below 0.50:

When a query has high uncertainty, it is a genuine dilemma. Rather than summoning duplicate agents that just repeat the same bias, our system instantiates a four-agent committee based on the Competing Values Framework.

We deploy four specific personas:
- The Clan persona, which prioritizes human ethics, patient autonomy, and safety.
- The Adhocracy persona, which looks for innovative angles and adaptive solutions.
- The Market persona, which evaluates practical utility, fiscal cost, and deliverables.
- The Hierarchy persona, which enforces statutory precedents and strict legal rules.

To prevent infinite debate loops, after each round we compute Kendall's concordance coefficient across the agents' ranked preferences. As soon as agreement crosses 0.70, the debate terminates immediately.

Looking at our real benchmark evaluation across 200 questions from StrategyQA and MMLU Professional Law:
- First, we achieved a 50.88% net reduction in tokens across the board compared to the base paper.
- Second, on StrategyQA, unconditional debate from the base paper caused single-agent accuracy to collapse from 70% down to 43% due to peer noise. Our confidence gate protected straightforward questions and kept accuracy at 69% while cutting tokens by 56.8%.
- Third, on complex legal dilemmas in MMLU Law, even though 79.5% of questions triggered the committee, early stopping still saved 45.3% of tokens compared to exhaustive debate.

For Review 3, our goal is to deploy this on local edge hardware with small language models like Llama 3.2 3B to measure physical RAM and CPU latency, and submit our manuscript for IEEE conference publication."

---

## 4. Key Numbers Cheat Sheet (Memorize These)

- 200: Total number of real academic questions tested (100 StrategyQA + 100 MMLU Professional Law).
- 50.88%: Total token savings across all 200 questions compared to the base paper.
- 1,562 vs 3,182: Average tokens per query in our system versus the base paper.
- 0.65: Confidence threshold (tau). Above 0.65 takes the fast solo path; below 0.50 summons the committee.
- 0.70: Kendall's concordance agreement target for early stopping.
- 70% down to 43%: How badly the base paper crashed on StrategyQA because of peer noise.
- 69%: The accuracy our system maintained on StrategyQA while saving 56.8% of tokens.
- 0.8 seconds: Response time on the Solo Fast-Path.

---

## 5. What All Is in the Project (Code and Folders)

If the professors ask what files exist in the project:

- `cag_delphi_engine/`: The core Python package with the logic.
  - `gating.py`: Calculates token entropy, consistency, and the confidence score.
  - `topology.py`: Handles routing between Solo, Dyadic, and Delphi paths.
  - `diversity.py`: Defines the four personas (Clan, Adhocracy, Market, Hierarchy).
  - `consensus.py`: Calculates Kendall's concordance for early stopping.
- `skills/confidence-gated-consultation/`: An official Agent Skill that lets any AI agent use our confidence gate autonomously.
- `data/real_benchmarks/`: Holds the 200 real questions from StrategyQA and MMLU Law, plus full execution traces.
- `run_full_dataset_execution.py`: The executable script that runs all 200 questions live.
- `cag_delphi_live_showcase.py`: An interactive terminal demo showing the four agents debating medical triage and satellite conflict dilemmas.
- `cag_delphi_geval_proofs.py`: The mathematical proof script asserting Theorems 1, 2, and 3.

---

## 6. How to Run the Code if a Professor Asks You to Execute

If a reviewer asks, "Can you show me the code running?", open the terminal and type one of these:

### Command 1: Run the 200-question academic benchmark
```bash
python3 run_full_dataset_execution.py
```
What it shows: Streams live question evaluations, shows whether each question took the Solo path or the Committee path, and prints the final accuracy and token savings table.

### Command 2: Show the four agents debating live
```bash
python3 cag_delphi_live_showcase.py
```
What it shows: A multi-step medical triage dilemma and an orbital satellite conflict where you can watch the Clan, Adhocracy, Market, and Hierarchy agents debate and reach early consensus.

### Command 3: Show the mathematical proof assertions
```bash
python3 cag_delphi_geval_proofs.py
```
What it shows: Runs automated mathematical verifications for Theorem 1 (Debate Degeneration), Theorem 2 (Pareto Separation), and Theorem 3 (Token Bounds), printing `[PASS]` for all three in one second.

---

## 7. Common Professor Questions and How to Answer Them

### Question 1: What is the main novelty of your project?
Your Answer: "Most multi-agent systems always consult every agent on every query. Our novelty is epistemic confidence gating: the system mathematically evaluates its own certainty before deciding whether to consult peers. This cuts token consumption in half and prevents peer noise from ruining accuracy on easy questions."

### Question 2: Why did unconditional debate perform worse than a single agent on StrategyQA?
Your Answer: "Because StrategyQA questions have clear factual answers. When you force multiple agents to debate simple facts, contrarian arguments introduce doubt. The agents start hallucinating and talk each other out of the correct initial answer. Our confidence gate protects factual queries from debate."

### Question 3: How do you stop the agents from arguing forever?
Your Answer: "We monitor Kendall's concordance coefficient across the agents' ranked preferences after each round. As soon as agreement crosses 0.70, it proves strong consensus, and the debate exits immediately."

### Question 4: What are the four agent personas based on?
Your Answer: "They are grounded in Cameron and Quinn's Competing Values Framework. We use Clan for ethics and patient safety, Adhocracy for innovation, Market for utility and cost, and Hierarchy for statutory precedents."

### Question 5: What is your plan for Review 3?
Your Answer: "We will deploy small language models like Llama 3.2 3B locally on a laptop CPU using llama.cpp to measure physical RAM footprint and battery draw, and submit our finalized paper to an IEEE conference track."
