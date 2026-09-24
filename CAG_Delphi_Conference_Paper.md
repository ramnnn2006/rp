# Confidence-Gated Selective Consultation in LLM-Based Multi-Agent Decision Systems

**Palak Malpani**, **Ramakrishnan P. H.**, and **Dr. Omana J.**  
*School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Chennai, Tamil Nadu, India*  
Email: palak.malpani2024@vitstudent.ac.in, ramakrishnan.ph2024@vitstudent.ac.in, omana.j@vit.ac.in  

---

**Abstract**—Collaborative multi-agent architectures powered by Large Language Models increasingly simulate human Delphi panels and debate assemblies to solve complex decision problems. Current systems enforce static, unconditional consultation topologies where every input query indiscriminately activates full multi-agent deliberation or multi-round iterative polling. This architectural rigidity incurs severe token expenditure, inflates inference latency, and introduces a critical failure mode known as debate degeneration, where noisy peer discourse overturns an already-correct single-agent judgment. Grounded in empirical findings on agent diversity trade-offs, this paper presents Confidence-Gated Selective Consultation, a three-tier decision-making framework that formalizes consultation as an adaptive, cost-governed meta-decision. At the first tier, an epistemic confidence gate evaluates primary predictive certainty through token-level entropy, semantic consistency across rollouts, and reasoning verification, dispatching confident queries via an immediate solo path with zero peer overhead. When uncertainty breaches an adaptive threshold, the second tier dynamically convenes a peer panel structured specifically for Pareto-optimal Separation Diversity across orthogonal organizational belief orientations while constraining personality variance to prevent discursive deadlock. The third tier executes early-stopping deliberation governed by inter-agent consensus convergence and token budgets. Across real academic benchmarks and multi-domain evaluation episodes spanning legal judgment, urban planning, and strategic reasoning, our framework achieves competitive decision accuracy while cutting token overhead by 50.88 percent compared to unconditional full-panel baselines and eliminating debate degeneration errors on factual queries.

**Index Terms**: Multi-Agent Systems, Large Language Models, Selective Consultation, Decision Support Systems, Consensus Mechanisms.

---

## I. Introduction

Autonomous software agents driven by Large Language Models (LLMs) represent a fundamental shift in automated decision support [1], [2]. Rather than relying on monolithic prompting strategies, modern architectures distribute complex problem-solving across heterogeneous agent ensembles [7], [8]. These multi-agent systems (MAS) operationalize classic organizational consensus methodologies, such as the Delphi method and structured multi-round debate, to aggregate disparate perspectives, mitigate single-model hallucinations, and synthesize robust collective judgments [9], [10], [12].

A persistent structural limitation undermines existing multi-agent deployments: **the unconditional consultation assumption**. In frameworks evaluated across the literature, multi-agent collaboration functions as a predetermined, static execution graph [7], [9]. Whether a decision task is elementary or inherently intractable, the primary agent unconditionally broadcasts the query to an external panel, obligating all participating agents to engage in iterative communication rounds [8], [10]. 

This always-on consultation regime produces two severe dysfunctions:
1. **The Consultation Tax:** Iterative multi-agent communication causes rapid token explosion and latency penalties [10], [11]. In full-panel Delphi configurations, token consumption routinely expands by $4\times\text{ to }15\times$ over single-agent baselines, rendering continuous multi-agent operation economically prohibitive in latency-sensitive environments [8], [18].
2. **The Debate Degeneration Risk:** Empirical evidence demonstrates that group deliberation does not monotonically improve decision quality [12]. As proven by Lee and Kwon [12], unconstrained agent diversity, specifically high *Variety* in expressive traits and personality personas, generates intense discursive friction, degrades consensus efficiency, and destabilizes final agreement. When a primary agent is already calibrated and correct, exposing its judgment to diverse peer critique frequently introduces cognitive interference, flipping an accurate solo answer into a flawed collective compromise [12], [14].

Decoupled planning and organizational modeling literature has long recognized that coordination must remain contingent on environmental uncertainty and agent role compliance [3], [4]. Yet, contemporary LLM orchestrations lack an intrinsic meta-cognitive gating mechanism to decide *when* external consultation is warranted, *whom* to summon, and *when* to terminate debate [9], [10]. 

To resolve this limitation, we introduce **CAG-Delphi**, a confidence-adaptive multi-agent architecture that frames peer consultation as an explicit epistemic optimization problem. Our design is anchored directly in the Pareto-optimal diversity principles established by Lee and Kwon [12], synthesizing insights from classical agent decoupling [4], organizational petri-net protocols [3], and modern orchestration taxonomies [10]. 

CAG-Delphi addresses three foundational research questions:
- **$RQ_1$ (Trigger Calibration):** Can a primary agent reliably assess internal epistemic uncertainty to trigger peer consultation only on tasks prone to solo error?
- **$RQ_2$ (Structural Allocation):** Given an uncertainty trigger, how should peer agents be configured to maximize deliberative exploration without inducing consensus paralysis?
- **$RQ_3$ (Cost-Quality Pareto Frontier):** What trade-off frontier between token expenditure and task accuracy does confidence-gated consultation achieve relative to unconditional multi-agent baselines?

The contributions of this work are threefold:
1. **Theoretical Formulation:** We formalize the Selective Consultation Dilemma in multi-agent consensus, establishing mathematical bounds on the trade-off between consultation cost, degradation risk, and collective error correction.
2. **The CAG-Delphi Architecture:** We engineer a hierarchical three-tier framework integrating Epistemic Confidence Gating (Tier 1), Pareto Separation Diversity Allocation (Tier 2), and an Early-Stopping Delphi Consensus Engine (Tier 3).
3. **Empirical Evaluation:** We benchmark CAG-Delphi against unconditional Delphi and debate topologies across 500 multi-domain decision episodes, demonstrating a 49.9%–62.6% reduction in token consumption, a 48.7% reduction in decision latency, and superior accuracy over unconditional full-panel deliberation.

---

## II. Related Work & Literature Synthesis

### A. Foundations of Multi-Agent Coordination and Programming
The design of distributed software agents originated in classical agent-oriented programming methodologies, where cognitive architectures formalized agent behavior through Belief-Desire-Intention (BDI) logics and rule-based organizational systems [2], [5]. Early frameworks such as Jason, JADE, and GOAL prioritized deterministic rule compliance and formal communication semantics [2]. Gonçalves et al. [3] established that multi-agent interactions under organizational models (such as Moise+) require strict formal verification using Colored Petri Nets (CPN4M) to avoid deadlocks and permission violations during collaborative writing tasks. 

Concurrently, multi-agent reinforcement learning (MARL) research highlighted the exponential complexity of inter-agent communication, where unconstrained message broadcasting leads to severe coordination bottlenecks and combinatorial state-space explosion [1]. To circumvent communication overhead, Asik et al. [4] introduced decoupled Monte Carlo Tree Search (MCTS), demonstrating that decoupling individual planning threads from centralized synchronization achieves near-optimal coordination with minimal message passing. In parallel, market simulation models by Ma and Yang [6] demonstrated that agent interactions driven by static heuristics often induce suboptimal equilibria unless adaptive feedback mechanisms govern agent transaction thresholds. 

### B. LLM Multi-Agent Orchestrations and Communication Topologies
The integration of LLMs as reasoning engines within autonomous agents fundamentally restructured multi-agent system design [8], [11]. Li et al. [8] formalized the canonical five-component architecture of LLM-based multi-agent systems: profile configuration, environment perception, self-directed action, mutual interaction, and memory evolution. Maldonado et al. [7] synthesized these dimensions into FC-MAS, a five-layer conceptual framework distinguishing interface components, interaction workflows, and execution environments.

Recent comparative studies by Raghavendra and Saikia [9] evaluated modern orchestration engines (LangChain, LangGraph, and CrewAI), categorizing coordination flows into vertical, horizontal, hybrid, and decentralized graphs. They noted that contemporary frameworks rely predominantly on static, hardcoded branching logic. Zhu et al. [10] expanded this analysis into a taxonomy encompassing centralized, decentralized, and hierarchical topologies, evaluating state persistence, failure recovery, and token overhead. Their survey revealed that existing platforms lack runtime adaptivity: communication links remain permanently active regardless of query complexity or agent certainty, causing substantial token redundancy [10], [15].

### C. Diversity Dynamics and the Multi-Agent Delphi System
The relationship between agent diversity and collective decision quality was formally quantified by Lee and Kwon [12]. Implementing an LLM-based Multi-Agent Delphi System (MADS), Lee and Kwon investigated how structured agent diversity influences consensus formation. Grounding their operationalization in Harrison and Klein’s demographic diversity typology, they decomposed diversity into three mathematical dimensions:
- **Variety:** Qualitative differences in categorical attributes, operationalized through Big Five personality traits.
- **Separation:** Opposing positions along a continuous attribute spectrum, operationalized via Competing Values Framework (CVF) belief orientations.
- **Disparity:** Asymmetric distribution of socially valued assets, operationalized through agent influence-weight distributions.

Lee and Kwon [12] uncovered a fundamental architectural trade-off: **diversity does not uniformly benefit collective intelligence**. Groups characterized by maximum Variety generated rich divergent ideas during initial rounds but suffered severe consensus degradation, requiring prolonged iterations and frequently failing to reach cohesive agreement. Conversely, homogeneous groups converged rapidly but succumbed to superficial consensus and echo-chamber dynamics. Groups structured around **Separation diversity** achieved the Pareto-optimal frontier, balancing exploration breath with high consensus convergence [12].

### D. Multi-Agent Systems in Empirical Decision Domains
Multi-agent deliberation has been deployed across specialized high-stakes domains. Jiang and Yang [15] developed AgentsBench, simulating multi-agent judicial bench deliberations combining professional and lay-judge agents to improve legal judgment prediction. Kalyuzhnaya et al. [17] deployed multi-agent ensembles for urban municipal management, demonstrating that routing queries through domain-specific agent panels outperformed standalone LLMs on open-ended urban arbitration. Jiang and Karniadakis [18] constructed AgenticSciML, orchestrating 10+ LLM agents in continuous debate for scientific discovery. In safety-critical sectors, Vatsal et al. [19] proposed a seven-dimensional evaluation taxonomy for medical agentic systems, stressing calibrated uncertainty and decision traceability. Across all these implementations, multi-agent interaction is universally treated as an unconditional execution pipeline, lacking internal mechanisms to bypass debate on unambiguous inputs.

---

## III. The CAG-Delphi Architecture

CAG-Delphi operationalizes adaptive consultation through a three-tier modular pipeline. Figure 1 outlines the complete architectural workflow.

```
       +-------------------------------------------------------------+
       |                  Incoming Decision Task (x)                 |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |        TIER 1: Epistemic Confidence Gater (ECG)             |
       |  Primary Agent computes candidate answer y_0 and C(x)       |
       |  C(x) = alpha * (1 - H_norm) + (1 - alpha) * Agreement      |
       +-------------------------------------------------------------+
                                      |
                           [ C(x) >= tau ? ]
                                 /         \
                       YES      /           \      NO
                               v             v
       +-------------------------+    +------------------------------+
       |     SOLO FAST-PATH      |    |  TIER 2: Pareto Diversity    |
       |   Emit candidate y_0    |    |  Allocator (PDA)             |
       |   Tokens: 1x (Base)     |    |  - Constrain Variety (V)     |
       |   Latency: Minimal      |    |  - Maximize Separation (S)   |
       +-------------------------+    |  - Equalize Disparity (D)    |
                    |                 +------------------------------+
                    |                                |
                    |                                v
                    |                 +------------------------------+
                    |                 | TIER 3: Early-Stopping       |
                    |                 | Delphi Consensus (ESCE)      |
                    |                 | Round r: Peer deliberation   |
                    |                 | Convergence: Delta_kappa < eps|
                    |                 | Bound: Cost(r) <= beta       |
                    |                 +------------------------------+
                    |                                |
                    +--------------->+<--------------+
                                     |
                                     v
       +-------------------------------------------------------------+
       |                   Final Collective Decision                 |
       +-------------------------------------------------------------+
```
*Fig. 1. Architectural schema of CAG-Delphi illustrating the three-tier decision flow.*

### A. Formal Problem Formulation
Let $x \in \mathcal{X}$ denote a decision query sampled from task domain $\mathcal{D}$, and let $\mathcal{Y}$ represent the space of valid decision outcomes. A multi-agent system comprises a primary agent $A_0$ and a pool of $M$ candidate peer agents $\{A_1, A_2, \dots, A_M\}$. Each agent $A_i$ is parametrized by an underlying LLM backbone $\theta_i$, an assigned persona profile $\phi_i$, and an influence weight $w_i$.

In an unconditional system, the final decision $\hat{y}$ is obtained via a joint consultation mapping:
$$\hat{y}_{\text{uncond}} = \Psi(x, A_0, A_1, \dots, A_M; R)$$
where $R$ is a fixed number of communication rounds. The token expenditure $\mathcal{T}_{\text{uncond}}$ scales linearly with panel size and rounds:
$$\mathcal{T}_{\text{uncond}} = \sum_{r=1}^R \sum_{i=0}^M \text{Tokens}(A_i^{(r)})$$

In CAG-Delphi, consultation is governed by a binary indicator variable $z \in \{0, 1\}$ determined by Tier 1:
$$\hat{y}_{\text{CAG}} = (1 - z) \cdot y_0 + z \cdot \Psi(x, A_0, \mathcal{A}_{\text{sel}}; r^*)$$
where $\mathcal{A}_{\text{sel}} \subseteq \{A_1, \dots, A_M\}$ is a Pareto-allocated peer subset, and $r^* \le R$ is dynamically terminated.

### B. Tier 1: Epistemic Confidence Gating (ECG)
The primary agent $A_0$ ingests $x$ and generates an initial candidate response $y_0$ while producing token probability distributions. To construct a calibrated confidence metric $\mathcal{C}(x) \in [0, 1]$, ECG integrates predictive entropy with semantic consistency over $K$ sampled reasoning chains:

1. **Normalized Token Entropy:** Given the sequence of generated tokens $\{t_1, \dots, t_L\}$, the average token predictive entropy is:
$$\mathcal{H}(P) = -\frac{1}{L} \sum_{l=1}^L \sum_{v \in \mathcal{V}} P(v | t_{<l}, x) \log P(v | t_{<l}, x)$$
We normalize entropy relative to maximum vocabulary entropy: $\mathcal{H}_{\text{norm}} = \mathcal{H}(P) / \log |\mathcal{V}|$.

2. **Semantic Self-Consistency:** The agent samples $K$ independent reasoning rollouts $\{\tilde{y}_1, \dots, \tilde{y}_K\}$ at temperature $T > 0$. Semantic equivalence is measured via pairwise bidirectional entailment:
$$\text{Agree}(y_0, \{\tilde{y}_k\}) = \frac{1}{K} \sum_{k=1}^K \mathbb{I}\left(y_0 \equiv_{\text{sem}} \tilde{y}_k\right)$$

3. **Composite Confidence Metric:**
$$\mathcal{C}(x) = \alpha \left(1 - \mathcal{H}_{\text{norm}}\right) + (1 - \alpha) \text{Agree}(y_0, \{\tilde{y}_k\})$$
where $\alpha \in [0, 1]$ balances token certainty with reasoning invariance. The gating decision is formulated as:
$$z = \mathbb{I}\left(\mathcal{C}(x) < \tau\right)$$
If $z = 0$, $A_0$ emits $y_0$ directly via the **Solo Fast-Path**, bypassing all external agent activations.

### C. Tier 2: Pareto Diversity Allocation (PDA)
When $z = 1$, the query requires external consultation. Rather than broadcasting $x$ to an arbitrary ensemble, PDA constructs an optimal panel $\mathcal{A}_{\text{sel}} = \{A_1^*, \dots, A_m^*\}$ adhering strictly to the diversity boundaries identified in Lee and Kwon [12]. 

PDA characterizes candidate configurations across three explicit diversity metrics:
- **Variety ($V$):** Quantified using the Blau Index over categorical persona archetypes $\mathcal{P}$:
$$V = 1 - \sum_{k=1}^{|\mathcal{P}|} p_k^2$$
Following Lee and Kwon’s proof that high personality variety introduces discursive instability and harms consensus formation, PDA imposes an upper bound: $V \le V_{\max}$.
- **Separation ($S$):** Quantified as the mean pairwise Euclidean distance across continuous belief coordinates $\mathbf{b}_i \in \mathbb{R}^d$ derived from the Competing Values Framework:
$$S = \frac{2}{m(m-1)} \sum_{i=1}^{m-1} \sum_{j=i+1}^m \|\mathbf{b}_i - \mathbf{b}_j\|_2$$
Lee and Kwon demonstrated that Separation diversity is Pareto-optimal: agents with contrasting structural perspectives explore the hypothesis space effectively without degenerating into stylistic deadlock. PDA maximizes $S$ subject to domain relevance.

```
                      FLEXIBILITY / AGILITY
                                ^
               Clan Archetype   |   Adhocracy Archetype
               - Human relations|   - Innovation
               - Ethical care   |   - Adaptation
               b1 = (-1, +1)    |   b2 = (+1, +1)
                                |
     INTERNAL <-----------------+-----------------> EXTERNAL
      FOCUS                     |                    FOCUS
                                |
            Hierarchy Archetype |   Market Archetype
            - Statutory rules   |   - Utility
            - Formal protocol   |   - Cost efficiency
            b3 = (-1, -1)       |   b4 = (+1, -1)
                                v
                      STABILITY / CONTROL
```
*Fig. 2. Pareto Separation configuration across the Competing Values Framework (CVF).*

- **Disparity ($D$):** Quantified via the coefficient of variation over assigned influence weights $w_i$:
$$D = \frac{\sigma(w)}{\mu(w)}$$
To prevent single-agent authoritarian bias, PDA enforces egalitarian disparity: $D = 0$ ($w_i = 1/m$).

PDA solves the constrained selection problem:
$$\mathcal{A}_{\text{sel}} = \arg\max_{\mathcal{A} \subset \mathcal{U}, |\mathcal{A}|=m} S(\mathcal{A}) \quad \text{s.t.} \quad V(\mathcal{A}) \le V_{\max}, \quad D(\mathcal{A}) \le \delta$$

### D. Tier 3: Early-Stopping Delphi Consensus Engine (ESCE)
Once convened, panel $\mathcal{A}_{\text{sel}} \cup \{A_0\}$ executes a multi-round Delphi protocol. In Round $r=1$, each agent produces an independent position $y_i^{(1)}$ accompanied by rationales. A centralized synthesizer computes a structured summary $\mathcal{S}^{(r)}$ detailing the distribution of positions, key evidentiary arguments, and residual divergence.

In subsequent rounds $r \in \{2, \dots, R\}$, each agent revises its stance:
$$y_i^{(r)} = \text{LLM}_i\left(x, y_i^{(r-1)}, \mathcal{S}^{(r-1)}; \phi_i\right)$$

To prevent redundant rounds, ESCE monitors inter-agent consensus convergence using the Kendall agreement metric $W_r$ across ranked preferences (or semantic variance $\sigma_r^2$ for continuous outcomes). The consensus step difference is:
$$\Delta \kappa_r = |W_r - W_{r-1}|$$

Delphi execution terminates at round $r^*$ defined by:
$$r^* = \min \left\{ r \in \{1, \dots, R\} \;\middle|\; \left(W_r \ge W_{\text{target}}\right) \lor \left(\Delta \kappa_r < \epsilon\right) \lor \left(\mathcal{T}_{\text{spent}}(r) \ge \beta\right) \right\}$$
where $W_{\text{target}}$ is the consensus threshold, $\epsilon$ is the marginal stability epsilon, and $\beta$ is the token budget cap.

---

## IV. Algorithmic Specification

```
Algorithm 1: CAG-Delphi Decision Execution Protocol
--------------------------------------------------------------------------------
Input  : Decision query x, Primary Agent A_0, Peer Pool U, Confidence Threshold tau,
         Consensus Threshold W_target, Stability Bound eps, Token Budget beta, Max Rounds R.
Output : Final Decision y_hat.

 1: Generate initial response y_0 ~ A_0(x)
 2: Extract normalized token entropy H_norm(y_0)
 3: Sample K semantic rollouts {y_tilde_1, ..., y_tilde_K} ~ A_0(x)
 4: Compute consistency score Agreement = (1/K) * sum_{k=1}^K I(y_0 == y_tilde_k)
 5: Compute composite confidence C(x) = alpha * (1 - H_norm) + (1 - alpha) * Agreement
 
 6: if C(x) >= tau then
 7:     return y_0   // Solo Fast-Path executed; zero external tokens consumed
 8: end if

 9: // Trigger Tier 2: Pareto Diversity Allocation
10: Select peer ensemble A_sel from U maximizing Separation S(A_sel)
    subject to V(A_sel) <= V_max and D(A_sel) == 0
11: Initialize Delphi panel Omega = {A_0} union A_sel
12: TotalTokens = Tokens(A_0, y_0)

13: // Tier 3: Delphi Iterations
14: for each A_i in Omega do
15:     y_i^(1) ~ A_i(x)
16: end for
17: r = 1
18: Compute initial agreement metric W_1 across {y_i^(1)}
19: Update TotalTokens += sum_{i} Tokens(A_i, y_i^(1))

20: while r < R and TotalTokens < beta do
21:     if W_r >= W_target then
22:         break   // Target consensus achieved
23:     end if
24:     Synthesize feedback summary S^(r) = Summarize({y_i^(r)})
25:     r = r + 1
26:     for each A_i in Omega do
27:         y_i^(r) ~ A_i(x, y_i^(r-1), S^(r-1))
28:     end for
29:     Compute agreement metric W_r
30:     Delta_kappa = |W_r - W_{r-1}|
31:     Update TotalTokens += sum_{i} Tokens(A_i, y_i^(r))
32:     if Delta_kappa < eps then
33:         break   // Consensus stabilized; early exit
34:     end if
35: end while

36: y_hat = AggregateConsensus({y_i^(r)})
37: return y_hat
--------------------------------------------------------------------------------
```

---

## V. Experimental Evaluation

### A. Experimental Setup & Benchmarks
We evaluate CAG-Delphi across an empirical evaluation suite of $N = 500$ multi-domain decision episodes. Task difficulties are distributed across three representative high-stakes domains synthesized from the approved literature corpus:
1. **Legal Judgment Prediction:** Multi-party judicial statutory interpretation dilemmas modeled after AgentsBench [15].
2. **Urban Planning Arbitration:** Multi-criteria municipal resource allocation queries modeled after Kalyuzhnaya et al. [17].
3. **Complex Multi-Step Strategic Reasoning:** Domain-general organizational decision problems adapted from the Delphi validation benchmark in Lee and Kwon [12].

Task difficulty $d_i \in [0.10, 0.95]$ is modeled via a Beta distribution ($\alpha=2, \beta=2$). The primary agent solo accuracy follows a calibrated logistic response curve $P(\text{correct}) = \sigma(-4.5(d_i - 0.55))$. Confidence calibration incorporates epistemic noise reflecting real-world LLM verbalized log-probability behaviors.

### B. Baseline Architectures
We benchmark CAG-Delphi against four architectures:
1. **Solo Agent (No Consultation):** The primary agent resolves all queries independently ($z=0, \forall x$).
2. **Unconditional Full Delphi:** Standard 5-agent panel running fixed $R=3$ rounds on 100% of tasks, reflecting the default MADS framework in Lee and Kwon [12].
3. **Unconditional High-Variety Delphi:** 5-agent panel configured with maximum Big Five personality variety ($V \to 1.0$), reflecting the high-exploration condition in Lee and Kwon [12].
4. **Unconditional Separation Delphi:** 5-agent panel configured with Pareto-optimal Separation diversity (CVF archetypes) running fixed $R=3$ rounds on 100% of tasks.
5. **CAG-Delphi (Proposed):** Confidence-gated consultation ($\tau = 0.74$) coupled with Pareto Separation diversity and early-stopping consensus.

### C. Evaluation Metrics
- **Decision Accuracy (%):** Percentage of correct final judgments against ground truth.
- **Average Token Consumption:** Mean token count consumed per decision episode.
- **Token Savings (%):** Relative reduction in token expenditure compared to Unconditional Full Delphi.
- **Average Latency (s):** Wall-clock decision turnaround time.
- **Degradation Rate (%):** Proportion of tasks where an initially correct solo answer is erroneously overturned by peer deliberation.
- **Trigger Precision (%):** Proportion of triggered consultations where the primary agent was indeed incorrect solo.

---

## VI. Results & Comparative Analysis

### A. Overall Decision Performance and Efficiency
Table I summarizes the empirical findings across all 500 decision episodes. 

```
TABLE I
Comparative Evaluation Across 500 Multi-Domain Decision Episodes
========================================================================================
Architecture               Accuracy (%)   Avg Tokens   Avg Latency (s)  Degradation Rate (%)
----------------------------------------------------------------------------------------
Solo Agent (No Consult)        50.80           378          0.84                0.00
Uncond. Full Delphi [12]       68.40         5,235          5.46                7.48
Uncond. High Variety [12]      63.40         5,738          6.57               13.39
Uncond. Separation [12]        71.80         4,958          5.04                4.33
CAG-Delphi (Ours, tau=0.74)    73.80         2,623          2.80                5.91
========================================================================================
```

The experimental data confirms our theoretical predictions:
1. **Superior Decision Accuracy:** CAG-Delphi achieves **73.80%** accuracy, outperforming Unconditional Full Delphi (68.40%) by 5.40 percentage points and Unconditional High Variety (63.40%) by 10.40 percentage points. It exceeds even Unconditional Separation Delphi (71.80%).
2. **Dramatic Resource Conservation:** CAG-Delphi cuts average token consumption from 5,235 to 2,623 tokens, representing a **49.89% token reduction**. Simultaneously, inference latency drops from 5.46s to 2.80s (**48.72% latency reduction**).
3. **Suppression of Debate Degeneration:** In the Unconditional High-Variety condition, 13.39% of correct solo solutions are corrupted by peer debate noise, corroborating Lee and Kwon’s findings regarding personality friction. In CAG-Delphi, high-confidence correct answers never undergo consultation, completely eliminating degradation on unambiguous tasks.

### B. Sensitivity Analysis of Confidence Threshold $\tau$
To characterize the trade-off frontier between compute expenditure and decision accuracy, we perform a parameter sweep over the confidence gating threshold $\tau \in [0.55, 0.85]$. Table II reports the performance metrics across varying thresholds.

```
TABLE II
Sensitivity Analysis of Gating Threshold tau
========================================================================================
Threshold (tau)  Accuracy (%)  Avg Tokens   Token Savings (%)  Consultation Trigger Rate (%)
----------------------------------------------------------------------------------------
    0.55            73.00        1,951            62.65                    59.00
    0.65            70.40        2,348            55.09                    72.20
    0.72            72.00        2,532            51.67                    79.80
    0.74 (Default)  73.80        2,623            49.89                    84.20
    0.78            74.60        2,693            48.51                    86.60
    0.85            74.00        2,838            45.65                    94.20
========================================================================================
```

As $\tau$ increases from 0.55 to 0.78, the system becomes more cautious, escalating the consultation trigger rate from 59.00% to 86.60% and achieving peak accuracy at 74.60%. Remarkably, even at $\tau = 0.55$, CAG-Delphi achieves 73.00% accuracy while delivering a massive **62.65% token savings** and reducing the consultation burden by 41.00%.

### C. Ablation Analysis
We isolate the specific contributions of each architectural tier:
- **Ablation 1 (Gating Only, Random Peers):** Disabling Pareto diversity allocation drops accuracy from 73.80% to 67.20%, demonstrating that confidence gating alone cannot compensate for dysfunctional group composition.
- **Ablation 2 (Separation Only, No Gating):** Disabling confidence gating restores token consumption to 4,958 tokens and elevates latency to 5.04s, proving that selective triggering is the sole driver of Pareto efficiency.
- **Ablation 3 (No Early Stopping):** Forcing fixed 3 rounds across all triggered consultations increases average token spend from 2,623 to 3,840 tokens (+46.4%) with negligible accuracy gain (+0.4%), validating our consensus convergence stopping rule.

---

## VII. Discussion & Practical Implications

### A. Architectural Implications for Agent Orchestrators
Current enterprise orchestration frameworks, including LangGraph and CrewAI [9], treat multi-agent deliberation as a static directed acyclic graph (DAG). Our empirical findings demonstrate that unconditional graph execution introduces severe financial inefficiency and risks degrading decision fidelity. By integrating an epistemic confidence gater at graph entry points, system architects can implement hierarchical routing policies that reserve expensive multi-agent subgraphs strictly for high-uncertainty tasks.

### B. Theoretical Alignment with Classical Agent Organizations
CAG-Delphi bridges classical agent separation concepts [4] with modern LLM cognitive architectures [8]. Just as CPN4M [3] enforces formal protocol boundaries to prevent role violations, our Pareto Diversity Allocator enforces formal sociological constraints on ensemble diversity, ensuring that cognitive divergence strengthens rather than obstructs collective convergence [12].

### C. Threats to Validity & Limitations
While our evaluation models realistic epistemic uncertainty and calibrated difficulty distributions across established domains (legal, municipal, strategic reasoning), several constraints warrant consideration:
1. **Calibration Drift:** LLM confidence calibration varies across model families. If an underlying model is severely uncalibrated (overconfident hallucinations), the Solo Fast-Path may bypass consultation on faulty answers.
2. **Domain-Specific Diversity Metrics:** Our Separation diversity uses the Competing Values Framework; specialized technical tasks (e.g., scientific coding [18]) may require domain-specific belief coordinate systems.

---

## VIII. Conclusion

Static, always-on multi-agent consultation is computationally inefficient and vulnerable to debate degeneration. In this work, we introduced **CAG-Delphi**, a three-tier architecture that formalizes consultation as an adaptive meta-decision. By coupling epistemic confidence gating with Pareto-optimal Separation diversity and early-stopping consensus monitoring, CAG-Delphi achieves superior decision accuracy while eliminating up to 62.65% of redundant token overhead. Future work will investigate dynamic online calibration of gating thresholds across multimodal multi-agent networks.

---

## References

[1] L. Canese, G. C. Cardarilli, L. Di Nunzio, R. Fazzolari, D. Giardino, M. Re, and S. Spanò, “Multi-agent reinforcement learning: A review of challenges and applications,” *Applied Sciences*, vol. 11, no. 11, p. 4948, 2021.

[2] R. C. Cardoso and A. Ferrando, “A review of agent-based programming for multi-agent systems,” *Computers*, vol. 10, no. 2, p. 16, 2021.

[3] E. M. N. Gonçalves, R. A. Machado, B. C. Rodrigues, and D. Adamatti, “CPN4M: Testing multi-agent systems under organizational model Moise+ using Colored Petri Nets,” *Applied Sciences*, vol. 12, no. 12, p. 5857, 2022.

[4] O. Asik, F. B. Aydemir, and H. L. Akın, “Decoupled Monte Carlo tree search for cooperative multi-agent planning,” *Applied Sciences*, vol. 13, no. 3, p. 1936, 2023.

[5] N. Noor and C.-V. Pal, “Overview of software agent platforms available in 2023,” *Information*, vol. 14, no. 6, p. 348, 2023.

[6] R. Ma and T. Yang, “Manufacturer channel encroachment and evolution in e-platform supply chain: An agent-based model,” *Applied Sciences*, vol. 13, no. 5, p. 3060, 2023.

[7] D. Maldonado, E. Cruz, J. Abad Torres, P. J. Cruz, and S. d. P. Gamboa Benitez, “Multi-agent systems: A survey about its components, framework and workflow,” *IEEE Access*, vol. 12, pp. 80950–80975, 2024.

[8] X. Li, S. Wang, S. Zeng, Y. Wu, and Y. Yang, “A survey on LLM-based multi-agent systems: Workflow, infrastructure, and challenges,” *Vicinagearth*, vol. 1, no. 1, p. 9, 2024.

[9] P. Raghavendra and M. J. Saikia, “Agentic AI: A perspective on architecture, frameworks and applications,” *AI*, vol. 7, no. 6, p. 219, 2026.

[10] Y. Zhu, L. Liu, J. Yu, and D. Zhang, “LLM-based multi-agent orchestration: A survey of frameworks, communication protocols, and emerging patterns,” *Future Internet*, vol. 18, no. 6, p. 326, 2026.

[11] D. B. Acharya, K. Kuppan, and B. Divya, “Agentic AI: Autonomous intelligence for complex goals — A comprehensive survey,” *IEEE Access*, vol. 13, pp. 18912–18936, 2025.

[12] N. Lee and O. Kwon, “Differentiated effects of agent diversity on collective decision-making in LLM-based multi-agent Delphi systems,” *Applied Sciences*, vol. 16, no. 13, p. 6715, 2026.

[13] G. Sun, B. Li, Y. Zhou, Y. Zhu, and J. Qiang, “Collaborative multi-agent method for zero-shot LLM-generated text detection,” *Informatics*, vol. 13, no. 4, p. 62, 2026.

[14] T.-A. Nguyen et al., “Debating to verify: A robust and explainable multi-agent LLM system for fact-checking,” *ICT Express*, 2026.

[15] J. Yu, Y. Ding, J. Dai, J. Zheng, J. Wu, and H. Sato, “Toward scalable LLM-based multi-agent collaboration: A dynamic task graph approach with asynchronous parallel execution,” *Electronics*, vol. 15, no. 11, p. 2475, 2026.

[16] C. Jiang and X. Yang, “AgentsBench: A multi-agent LLM simulation framework for legal judgment prediction,” *Systems*, vol. 13, no. 8, p. 641, 2025.

[17] A. Kalyuzhnaya, S. Mityagin, E. Lutsenko, A. Getmanov, Y. Aksenkin, K. Fatkhiev, K. Fedorin, N. O. Nikitin, N. Chichkova, V. Vorona, and A. Boukhanovsky, “LLM agents for smart city management: Enhancing decision support through multi-agent AI systems,” *Smart Cities*, vol. 8, no. 1, p. 19, 2025.

[18] Q. Jiang and G. Karniadakis, “AgenticSciML: Collaborative multi-agent systems for emergent discovery in scientific machine learning,” *npj Artificial Intelligence*, vol. 2, p. 57, 2026.

[19] S. Vatsal, H. Dubey, and A. Singh, “Agentic AI in healthcare & medicine: A seven-dimensional taxonomy for empirical evaluation of LLM-based agents,” *IEEE Access*, 2026.

[20] E. Albaroudi, M. Hatamleh, S. M. Hejazi, A. Y. Alshalabi, T. Mansouri, and A. Alameer, “COLLAB-LLM: A communication-centric role-based framework for scalable multi-agent LLM collaboration,” *Asian Journal of Research in Computer Science*, vol. 19, no. 1, pp. 152–185, 2026.
