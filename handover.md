# Teammate Handover

Here is our plan for tomorrow's Review 2 evaluation. All the heavy engineering, benchmarking, and theoretical proofs are done. To make sure you have solid ownership and can speak confidently during the review, here is your exact share of the work and presentation.

---

## What Is Already Finished

Everything on the technical side is complete and verified:
- We surveyed 16 research papers, focusing on the base paper by Lee and Kwon (2026).
- Mathematical proofs and formulations for our confidence gate are fully written.
- The Python decision engine is built and tested.
- We evaluated the system across 200 real academic questions (100 from StrategyQA and 100 from MMLU Professional Law).
- Real benchmark runs proved a 50.88% token reduction and fixed debate degeneration (where the base paper dropped to 43% accuracy on StrategyQA).
- Live terminal demo scripts are ready to execute.
- The public repository at ramnnn2006/cg-sc is clean, pushed, and contains only code and benchmark data.
- The full research repository at ramnnn2006/rp contains all 16 paper PDFs, LaTeX drafts, review reports, and execution logs.

---

## What You Need to Do Tonight

Here are the specific tasks for you:

### 1. Build the 5-Slide Presentation Deck
Use Google Slides, PowerPoint, or Canva. Keep it clean and readable. Use this slide order:

- Slide 1: Title and Research Gap
  Introduce the project title: Confidence-Gated Selective Consultation. Mention the core problem in Lee and Kwon (2026): unconditional multi-agent debate burns too many tokens and confuses models on simple facts.
- Slide 2: Core Architecture Flowchart
  Use the clean Mermaid flowchart from the README of the cg-sc repository. Walk through the confidence gate and the three paths: Solo Fast-Path, Dyadic Challenger, and Delphi Committee.
- Slide 3: The Four Agent Personas
  Explain the Competing Values Framework personas: Clan (ethics and safety), Adhocracy (innovation), Market (cost efficiency), and Hierarchy (rules and compliance). Mention early exit using Kendall's concordance.
- Slide 4: Real Benchmark Results
  Show our 200-question table. Highlight two key numbers: 50.88% token savings overall, and maintaining 69% accuracy on StrategyQA where unconditional debate collapsed to 43%.
- Slide 5: Review 3 Roadmap
  List upcoming work: testing on local laptop CPU with a 3B model, measuring physical RAM and latency, and submitting the camera-ready paper to an IEEE conference track.

### 2. Practice Your 90-Second Speaking Part
Review your section of the presentation script below so you can speak naturally without reading off notes.

### 3. Test Running the Scripts on Your Machine
Make sure Python is installed and test run the live demo:
```bash
git clone https://github.com/ramnnn2006/cg-sc.git
cd cg-sc
python3 run_full_dataset_execution.py
python3 cag_delphi_live_showcase.py
```

---

## 3-Minute Presentation Split

We have about 3 minutes total. We split the speaking time evenly down the middle.

### First 90 Seconds: My Part
- I will introduce the project and explain the limitation of Lee and Kwon (2026): unconditional multi-agent consultation wastes tokens and ruins accuracy on factual queries.
- I will explain the confidence gate formula: Shannon token entropy, semantic consistency, and rubric checks.
- I will explain the Solo Fast-Path where confident queries finish in 0.8 seconds using zero peer tokens.
- I will run the real benchmark script in terminal to demonstrate live question routing.
- I will hand over to you.

### Second 90 Seconds: Your Part
Here is your exact speaking lines:

"Thanks. Moving into what happens when confidence drops below 0.50: rather than summoning identical agents that echo each other, our system instantiates a four-agent committee based on the Competing Values Framework.

We have the Clan persona prioritizing human ethics, the Adhocracy persona exploring innovative angles, the Market persona focusing on practical utility and cost, and the Hierarchy persona enforcing statutory rules and precedents.

To prevent infinite debate loops, we calculate Kendall's concordance coefficient across peer rankings after each round. As soon as agreement crosses 0.70, the committee exits immediately.

Looking at our real benchmark evaluation across 200 questions from StrategyQA and MMLU Professional Law, this approach cut total token consumption by 50.88%.

More importantly, on StrategyQA, unconditional debate from the base paper caused single-agent accuracy to crash from 70% down to 43% due to peer noise. Our confidence-gated approach maintained 69% accuracy by shielding factual questions from unnecessary debate.

For Review 3, we plan to deploy this on local edge hardware with quantized 3B models and submit the finalized manuscript for conference publication."

---

## Tasks Left for Review 3 (After Tomorrow)

- Run local hardware profiling on a laptop CPU using small language models like Llama 3.2 3B or Phi 3.5.
- Record physical RAM consumption, CPU latency, and battery drain.
- Add code generation and math benchmarks (HumanEval and GSM8K).
- Finalize the camera-ready IEEE manuscript in the rp repository.

---

## Tomorrow Morning Checklist

- Have the 5 slides open in full screen.
- Have a terminal open ready to run the showcase script.
- Keep the cg-sc GitHub repository open in a browser tab showing the architecture flowchart.
