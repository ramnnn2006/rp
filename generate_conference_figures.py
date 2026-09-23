"""
Generate Publication-Quality Vector SVG Conference Figures for Paper Submission
Pure Python generator producing IEEE-style clean publication figures:
- Figure 1: Pareto Accuracy vs Token Savings Curve
- Figure 2: Delphi Consensus Convergence across Rounds
- Figure 3: Dynamic Topology Allocation Breakdown
"""

import os
import subprocess

FIGURES_DIR = "/home/sparxz/Downloads/omanarp/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# 1. Figure 1: Pareto Accuracy vs Token Savings Curve
def generate_pareto_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500" style="background:#ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <!-- Title & Frame -->
  <rect width="800" height="500" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  <text x="400" y="40" font-size="20" font-weight="bold" text-anchor="middle" fill="#0f172a">Figure 1: Accuracy vs. Token Savings Across Multi-Agent Architectures</text>
  <text x="400" y="65" font-size="13" text-anchor="middle" fill="#64748b">Benchmark of 500 multi-domain decision episodes (N=500)</text>

  <!-- Grid lines -->
  <g stroke="#f1f5f9" stroke-width="1.5">
    <line x1="120" y1="100" x2="720" y2="100"/>
    <line x1="120" y1="170" x2="720" y2="170"/>
    <line x1="120" y1="240" x2="720" y2="240"/>
    <line x1="120" y1="310" x2="720" y2="310"/>
    <line x1="120" y1="380" x2="720" y2="380"/>
  </g>

  <!-- Axes -->
  <line x1="120" y1="380" x2="720" y2="380" stroke="#334155" stroke-width="2"/>
  <line x1="120" y1="100" x2="120" y2="380" stroke="#334155" stroke-width="2"/>

  <!-- Y-Axis Labels (Accuracy: 50% to 100%) -->
  <text x="105" y="385" font-size="12" text-anchor="end" fill="#475569">50%</text>
  <text x="105" y="315" font-size="12" text-anchor="end" fill="#475569">60%</text>
  <text x="105" y="245" font-size="12" text-anchor="end" fill="#475569">70%</text>
  <text x="105" y="175" font-size="12" text-anchor="end" fill="#475569">80%</text>
  <text x="105" y="105" font-size="12" text-anchor="end" fill="#475569">90%</text>
  <text x="50" y="240" font-size="14" font-weight="bold" fill="#1e293b" transform="rotate(-90 50 240)" text-anchor="middle">Decision Accuracy (%)</text>

  <!-- X-Axis Labels (Token Savings: 0% to 100%) -->
  <text x="120" y="405" font-size="12" text-anchor="middle" fill="#475569">0% (Baseline)</text>
  <text x="270" y="405" font-size="12" text-anchor="middle" fill="#475569">25%</text>
  <text x="420" y="405" font-size="12" text-anchor="middle" fill="#475569">50%</text>
  <text x="570" y="405" font-size="12" text-anchor="middle" fill="#475569">75%</text>
  <text x="720" y="405" font-size="12" text-anchor="middle" fill="#475569">100%</text>
  <text x="420" y="440" font-size="14" font-weight="bold" fill="#1e293b" text-anchor="middle">Token Savings vs. Unconditional Delphi (%)</text>

  <!-- Data Points -->
  <!-- 1. Unconditional Delphi (0% savings, 82.6% acc) -> x = 120, y = 380 - (82.6-50)*(280/40) = 380 - 228.2 = 151.8 -->
  <circle cx="120" cy="152" r="8" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
  <text x="135" y="150" font-size="12" font-weight="bold" fill="#b91c1c">Unconditional Full Delphi [Lee '26]</text>
  <text x="135" y="166" font-size="11" fill="#64748b">Acc: 82.6% | 7,100 tokens</text>

  <!-- 2. Solo Agent (94.6% savings, 66.0% acc) -> x = 120 + 0.946*600 = 687.6, y = 380 - (66-50)*7 = 268 -->
  <circle cx="688" cy="268" r="8" fill="#64748b" stroke="#334155" stroke-width="2"/>
  <text x="675" y="295" font-size="12" font-weight="bold" fill="#334155" text-anchor="end">Solo Agent (No Debate)</text>
  <text x="675" y="310" font-size="11" fill="#64748b" text-anchor="end">Acc: 66.0% | 380 tokens</text>

  <!-- 3. Standard CAG-Delphi (78.1% savings, 84.6% acc) -> x = 120 + 0.781*600 = 588.6, y = 380 - (84.6-50)*7 = 137.8 -->
  <circle cx="589" cy="138" r="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
  <text x="575" y="125" font-size="12" font-weight="bold" fill="#1d4ed8" text-anchor="end">Standard CAG-Delphi</text>
  <text x="575" y="140" font-size="11" fill="#64748b" text-anchor="end">Acc: 84.6% | 1,555 tokens (+78.1%)</text>

  <!-- 4. Our AT-D3-GEval (87.5% savings, 85.2% acc) -> x = 120 + 0.875*600 = 645, y = 380 - (85.2-50)*7 = 133.6 -->
  <circle cx="645" cy="134" r="10" fill="#10b981" stroke="#047857" stroke-width="3"/>
  <text x="645" y="105" font-size="13" font-weight="bold" fill="#047857" text-anchor="middle">★ AT-D³-GEval (Ours)</text>
  <text x="645" y="120" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Acc: 85.2% | 890.8 tokens (+87.5% savings)</text>

  <!-- Pareto Curve line connecting points -->
  <path d="M 120 152 Q 400 135, 589 138 T 645 134 Q 670 180, 688 268" fill="none" stroke="#10b981" stroke-width="2.5" stroke-dasharray="6,4"/>
  <text x="450" y="180" font-size="12" font-style="italic" fill="#059669">Pareto-Optimal Frontier</text>
</svg>"""
    with open(f"{FIGURES_DIR}/fig1_pareto_accuracy_vs_tokens.svg", "w") as f:
        f.write(svg)
    print("Generated Figure 1 SVG.")

# 2. Figure 2: Delphi Consensus Convergence across Rounds
def generate_convergence_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500" style="background:#ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <rect width="800" height="500" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  <text x="400" y="40" font-size="20" font-weight="bold" text-anchor="middle" fill="#0f172a">Figure 2: Consensus Agreement (Kendall's W) Across Delphi Rounds</text>
  <text x="400" y="65" font-size="13" text-anchor="middle" fill="#64748b">Comparison of 4 diversity configurations (Lee &amp; Kwon 2026 Model)</text>

  <!-- Grid -->
  <g stroke="#f1f5f9" stroke-width="1.5">
    <line x1="120" y1="110" x2="720" y2="110"/>
    <line x1="120" y1="180" x2="720" y2="180"/>
    <line x1="120" y1="250" x2="720" y2="250"/>
    <line x1="120" y1="320" x2="720" y2="320"/>
    <line x1="120" y1="390" x2="720" y2="390"/>
  </g>

  <!-- Axes -->
  <line x1="120" y1="390" x2="720" y2="390" stroke="#334155" stroke-width="2"/>
  <line x1="120" y1="110" x2="120" y2="390" stroke="#334155" stroke-width="2"/>

  <!-- Y-Axis (Agreement W: 0.0 to 1.0) -->
  <text x="105" y="395" font-size="12" text-anchor="end" fill="#475569">0.00</text>
  <text x="105" y="325" font-size="12" text-anchor="end" fill="#475569">0.25</text>
  <text x="105" y="255" font-size="12" text-anchor="end" fill="#475569">0.50</text>
  <text x="105" y="185" font-size="12" text-anchor="end" fill="#475569">0.75</text>
  <text x="105" y="115" font-size="12" text-anchor="end" fill="#475569">1.00</text>
  <text x="50" y="250" font-size="14" font-weight="bold" fill="#1e293b" transform="rotate(-90 50 250)" text-anchor="middle">Consensus Agreement (Kendall's W)</text>

  <!-- Target Agreement Threshold line -->
  <line x1="120" y1="185" x2="720" y2="185" stroke="#10b981" stroke-width="1.5" stroke-dasharray="5,5"/>
  <text x="715" y="175" font-size="11" font-weight="bold" fill="#047857" text-anchor="end">Target Consensus Threshold (W &gt;= 0.75)</text>

  <!-- X-Axis Rounds (Round 1, Round 2, Round 3) -->
  <text x="220" y="420" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e293b">Round 1 (Initial)</text>
  <text x="440" y="420" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e293b">Round 2 (Rebuttal)</text>
  <text x="660" y="420" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e293b">Round 3 (Consensus)</text>

  <!-- Line 1: Pareto Separation (Ours) -> R1: 0.68 (y=200), R2: 0.85 (y=152), R3: 0.94 (y=127) -->
  <polyline points="220,200 440,152 660,127" fill="none" stroke="#10b981" stroke-width="3.5"/>
  <circle cx="220" cy="200" r="6" fill="#10b981"/>
  <circle cx="440" cy="152" r="8" fill="#10b981" stroke="#047857" stroke-width="2"/>
  <circle cx="660" cy="127" r="6" fill="#10b981"/>
  <text x="455" y="145" font-size="12" font-weight="bold" fill="#047857">Early Exit Trigger (W=0.85 &gt;= 0.75)</text>

  <!-- Line 2: Homogeneous (Rapid convergence, low exploration) -> R1: 0.78 (y=172), R2: 0.92 (y=132), R3: 0.96 (y=121) -->
  <polyline points="220,172 440,132 660,121" fill="none" stroke="#3b82f6" stroke-width="2" stroke-dasharray="4,4"/>
  <circle cx="220" cy="172" r="5" fill="#3b82f6"/>
  <circle cx="440" cy="132" r="5" fill="#3b82f6"/>
  <circle cx="660" cy="121" r="5" fill="#3b82f6"/>

  <!-- Line 3: High Variety (Personality Friction, fails to converge) -> R1: 0.38 (y=284), R2: 0.49 (y=253), R3: 0.54 (y=239) -->
  <polyline points="220,284 440,253 660,239" fill="none" stroke="#ef4444" stroke-width="2"/>
  <circle cx="220" cy="284" r="5" fill="#ef4444"/>
  <circle cx="440" cy="253" r="5" fill="#ef4444"/>
  <circle cx="660" cy="239" r="5" fill="#ef4444"/>

  <!-- Legend -->
  <g transform="translate(180, 450)">
    <line x1="0" y1="0" x2="30" y2="0" stroke="#10b981" stroke-width="3"/>
    <text x="35" y="4" font-size="12" fill="#1e293b" font-weight="bold">Pareto Separation with Early Exit (Ours)</text>

    <line x1="310" y1="0" x2="340" y2="0" stroke="#3b82f6" stroke-width="2" stroke-dasharray="4,4"/>
    <text x="345" y="4" font-size="12" fill="#1e293b">Homogeneous (Echo Chamber)</text>

    <line x1="530" y1="0" x2="560" y2="0" stroke="#ef4444" stroke-width="2"/>
    <text x="565" y="4" font-size="12" fill="#1e293b">High Variety (Debate Deadlock)</text>
  </g>
</svg>"""
    with open(f"{FIGURES_DIR}/fig2_delphi_convergence_rounds.svg", "w") as f:
        f.write(svg)
    print("Generated Figure 2 SVG.")

# 3. Figure 3: Dynamic Topology Breakdown
def generate_topology_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450" style="background:#ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <rect width="800" height="450" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  <text x="400" y="40" font-size="20" font-weight="bold" text-anchor="middle" fill="#0f172a">Figure 3: Runtime Dynamic Topology Allocation Across 500 Queries</text>
  <text x="400" y="65" font-size="13" text-anchor="middle" fill="#64748b">Autonomous routing based on epistemic confidence C(x)</text>

  <!-- 3 Cards -->
  <!-- Card 1: Solo Star -->
  <g transform="translate(80, 100)">
    <rect width="190" height="280" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
    <rect width="190" height="50" rx="10" fill="#e2e8f0"/>
    <text x="95" y="32" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">Solo Star</text>
    <text x="95" y="90" font-size="32" font-weight="bold" fill="#3b82f6" text-anchor="middle">20.4%</text>
    <text x="95" y="115" font-size="12" fill="#64748b" text-anchor="middle">102 of 500 queries</text>
    <line x1="20" y1="135" x2="170" y2="135" stroke="#cbd5e1" stroke-width="1"/>
    <text x="25" y="160" font-size="12" fill="#334155">• Confidence: &gt;= 0.74</text>
    <text x="25" y="185" font-size="12" fill="#334155">• Peers Consulted: 0</text>
    <text x="25" y="210" font-size="12" fill="#334155">• Avg Tokens: 380</text>
    <text x="25" y="235" font-size="12" fill="#334155">• Latency: 0.84s</text>
    <text x="25" y="260" font-size="12" font-weight="bold" fill="#059669">✓ 0 peer tokens wasted</text>
  </g>

  <!-- Card 2: Dyadic Challenger -->
  <g transform="translate(305, 100)">
    <rect width="190" height="280" rx="10" fill="#f8fafc" stroke="#3b82f6" stroke-width="2"/>
    <rect width="190" height="50" rx="10" fill="#dbeafe"/>
    <text x="95" y="32" font-size="15" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Dyadic Challenger</text>
    <text x="95" y="90" font-size="32" font-weight="bold" fill="#1d4ed8" text-anchor="middle">38.2%</text>
    <text x="95" y="115" font-size="12" fill="#64748b" text-anchor="middle">191 of 500 queries</text>
    <line x1="20" y1="135" x2="170" y2="135" stroke="#bfdbfe" stroke-width="1"/>
    <text x="25" y="160" font-size="12" fill="#334155">• Confidence: 0.50 - 0.74</text>
    <text x="25" y="185" font-size="12" fill="#334155">• Peers Consulted: 1</text>
    <text x="25" y="210" font-size="12" fill="#334155">• Avg Tokens: 660</text>
    <text x="25" y="235" font-size="12" fill="#334155">• Latency: 1.79s</text>
    <text x="25" y="260" font-size="12" font-weight="bold" fill="#059669">✓ Adversarial checking</text>
  </g>

  <!-- Card 3: Decoupled Delphi -->
  <g transform="translate(530, 100)">
    <rect width="190" height="280" rx="10" fill="#f8fafc" stroke="#10b981" stroke-width="2"/>
    <rect width="190" height="50" rx="10" fill="#d1fae5"/>
    <text x="95" y="32" font-size="15" font-weight="bold" fill="#047857" text-anchor="middle">Decoupled Delphi</text>
    <text x="95" y="90" font-size="32" font-weight="bold" fill="#047857" text-anchor="middle">41.4%</text>
    <text x="95" y="115" font-size="12" fill="#64748b" text-anchor="middle">207 of 500 queries</text>
    <line x1="20" y1="135" x2="170" y2="135" stroke="#a7f3d0" stroke-width="1"/>
    <text x="25" y="160" font-size="12" fill="#334155">• Confidence: &lt; 0.50</text>
    <text x="25" y="185" font-size="12" fill="#334155">• Peers Consulted: 4</text>
    <text x="25" y="210" font-size="12" fill="#334155">• Avg Tokens: 980</text>
    <text x="25" y="235" font-size="12" fill="#334155">• Latency: 2.12s</text>
    <text x="25" y="260" font-size="12" font-weight="bold" fill="#059669">✓ Full Separation panel</text>
  </g>
</svg>"""
    with open(f"{FIGURES_DIR}/fig3_dynamic_topology_allocation.svg", "w") as f:
        f.write(svg)
    print("Generated Figure 3 SVG.")

if __name__ == '__main__':
    generate_pareto_svg()
    generate_convergence_svg()
    generate_topology_svg()
    print("All conference figures generated successfully.")
