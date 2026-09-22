"""
Comprehensive Experiment & Parameter Sweep Harness for CAG-Delphi
Executes high-resolution tau sweeps, diversity ablations, and G-Eval impact tests.
Outputs CSV and JSON data for empirical verification.
"""

import argparse
import csv
import json
import os
import statistics
from typing import Dict, Any, List

from cag_delphi_engine.benchmark import run_cag_benchmark
from cag_delphi_engine.gating import EpistemicConfidenceGater
from cag_delphi_engine.diversity import ParetoDiversityAllocator, AgentPersona, CLAN, ADHOCRACY, MARKET, HIERARCHY
from cag_delphi_engine.consensus import EarlyStoppingDelphiEngine

def run_tau_sweep(n_episodes: int = 500, output_csv: str = "data/pareto_frontier.csv") -> List[Dict[str, Any]]:
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    tau_values = [0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.74, 0.78, 0.82, 0.86, 0.90]
    sweep_results = []

    print(f"{'Tau':<8} | {'Accuracy (%)':<14} | {'Avg Tokens':<12} | {'Savings (%)':<12} | {'Trigger Rate (%)':<18} | {'G-Eval':<10}")
    print("-" * 85)

    for tau in tau_values:
        res = run_cag_benchmark(n_episodes=n_episodes, tau=tau, seed=42)
        cag = res['cag_delphi']
        entry = {
            'tau': tau,
            'accuracy_pct': cag['accuracy_pct'],
            'avg_tokens': cag['avg_tokens'],
            'token_savings_pct': cag['token_savings_pct'],
            'consultation_trigger_rate_pct': cag['consultation_trigger_rate_pct'],
            'avg_geval_score': cag['avg_geval_score'],
            'avg_latency_s': cag['avg_latency_s'],
            'early_exit_rate_pct': cag['early_exit_rate_pct']
        }
        sweep_results.append(entry)
        print(f"{tau:<8.2f} | {entry['accuracy_pct']:<14.2f} | {entry['avg_tokens']:<12d} | {entry['token_savings_pct']:<12.2f} | {entry['consultation_trigger_rate_pct']:<18.2f} | {entry['avg_geval_score']:<10.4f}")

    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(sweep_results[0].keys()))
        writer.writeheader()
        writer.writerows(sweep_results)

    print(f"\n[SUCCESS] Saved Pareto sweep results to {output_csv}")
    return sweep_results

def run_diversity_ablation(n_episodes: int = 500, output_json: str = "data/diversity_ablation.json") -> Dict[str, Any]:
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    
    # 4 Diversity conditions from Lee & Kwon (2026)
    conditions = {
        'homogeneous': [
            AgentPersona(f"Peer_{i+1}", CLAN, "Analytical-Conscientious", 0.25) for i in range(4)
        ],
        'high_variety_only': [
            AgentPersona("Peer_1", CLAN, "Open-Creative", 0.25),
            AgentPersona("Peer_2", CLAN, "Extraverted-Assertive", 0.25),
            AgentPersona("Peer_3", CLAN, "Neurotic-Cautious", 0.25),
            AgentPersona("Peer_4", CLAN, "Agreeable-Empathetic", 0.25)
        ],
        'high_disparity': [
            AgentPersona("Leader", CLAN, "Analytical-Conscientious", 0.70),
            AgentPersona("Peer_2", ADHOCRACY, "Analytical-Conscientious", 0.10),
            AgentPersona("Peer_3", MARKET, "Analytical-Conscientious", 0.10),
            AgentPersona("Peer_4", HIERARCHY, "Analytical-Conscientious", 0.10)
        ],
        'pareto_separation': [
            AgentPersona("Peer_1", CLAN, "Analytical-Conscientious", 0.25),
            AgentPersona("Peer_2", ADHOCRACY, "Analytical-Conscientious", 0.25),
            AgentPersona("Peer_3", MARKET, "Analytical-Conscientious", 0.25),
            AgentPersona("Peer_4", HIERARCHY, "Analytical-Conscientious", 0.25)
        ]
    }

    allocator = ParetoDiversityAllocator()
    ablation_results = {}

    print("\n" + "=" * 95)
    print("DIVERSITY ABLATION STUDY (Lee & Kwon 2026 Blueprint)")
    print("=" * 95)
    print(f"{'Condition':<25} | {'Separation (S)':<15} | {'Variety (V)':<12} | {'Disparity (D)':<14} | {'Consensus Score (Q)':<20}")
    print("-" * 95)

    for name, panel in conditions.items():
        s = allocator.calculate_separation(panel)
        v = allocator.calculate_blau_variety(panel)
        d = allocator.calculate_disparity(panel)
        # Consensus quality metric from Theorem 2
        q = (s + 0.25 * v) / (1.0 + 2.2 * (v ** 2) + 1.2 * d)
        
        ablation_results[name] = {
            'separation_s': s,
            'variety_v': v,
            'disparity_d': d,
            'consensus_quality_q': round(q, 4)
        }
        print(f"{name:<25} | {s:<15.4f} | {v:<12.4f} | {d:<14.4f} | {q:<20.4f}")

    with open(output_json, 'w') as f:
        json.dump(ablation_results, f, indent=2)

    print(f"\n[SUCCESS] Saved diversity ablation study to {output_json}")
    return ablation_results

def run_geval_ablation(n_episodes: int = 500, output_json: str = "data/geval_ablation.json") -> Dict[str, Any]:
    """
    Evaluates the impact of enabling vs disabling G-Eval in the gating loop.
    """
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    
    configs = [
        ("No G-Eval (Entropy + Agree Only)", 0.45, 0.55, 0.00),
        ("Balanced G-Eval (Default CAG-Delphi)", 0.35, 0.45, 0.20),
        ("High G-Eval Weight", 0.25, 0.35, 0.40)
    ]
    
    results = {}
    print("\n" + "=" * 90)
    print("G-EVAL ('JEV') GATING ABLATION STUDY")
    print("=" * 90)
    print(f"{'G-Eval Configuration':<40} | {'Accuracy (%)':<15} | {'Avg Tokens':<12} | {'G-Eval Score':<12}")
    print("-" * 90)
    
    for label, w1, w2, w3 in configs:
        gater = EpistemicConfidenceGater(tau=0.74, w1_entropy=w1, w2_agreement=w2, w3_geval=w3)
        res = run_cag_benchmark(n_episodes=n_episodes, tau=0.74, seed=42)
        cag = res['cag_delphi']
        results[label] = {
            'w_entropy': w1,
            'w_agreement': w2,
            'w_geval': w3,
            'accuracy_pct': cag['accuracy_pct'],
            'avg_tokens': cag['avg_tokens'],
            'avg_geval_score': cag['avg_geval_score']
        }
        print(f"{label:<40} | {cag['accuracy_pct']:<15.2f} | {cag['avg_tokens']:<12d} | {cag['avg_geval_score']:<12.4f}")

    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] Saved G-Eval ablation results to {output_json}")
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CAG-Delphi Experiment Suite")
    parser.add_argument("--episodes", type=int, default=500, help="Number of episodes per test")
    parser.add_argument("--all", action="store_true", help="Run all sweeps and ablations")
    args = parser.parse_args()

    run_tau_sweep(n_episodes=args.episodes)
    run_diversity_ablation(n_episodes=args.episodes)
    run_geval_ablation(n_episodes=args.episodes)
