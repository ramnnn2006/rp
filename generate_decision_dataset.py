"""
Synthetic Decision Episode Dataset Generator
Follows Section 6 of Multi-Agent-Decision-Making-Research-Package.pdf.
Generates 500 structured decision episodes across 3 domains:
- Legal Judgment (Jiang & Yang, 2025)
- Urban Planning Arbitration (Kalyuzhnaya et al., 2025)
- Complex Strategic Reasoning (Lee & Kwon, 2026)

Fields:
task_id, domain, query, difficulty, primary_answer, primary_confidence,
consult_triggered, delphi_rounds, final_answer, ground_truth, consult_helped,
tokens_spent, latency_s, geval_score
"""

import json
import random
import math
import os

DOMAINS = [
    ("Legal_Judgment", "Evaluate criminal culpability and sentencing severity under statutory mitigating circumstances.", 0.65),
    ("Urban_Planning", "Arbitrate municipal resource allocation between transit infrastructure and residential zoning.", 0.50),
    ("Strategic_Reasoning", "Delphi panel evaluation of multi-stakeholder organizational talent acquisition strategy.", 0.45)
]

def generate_dataset(n_samples: int = 500, output_file: str = "data/decision_episodes.jsonl", seed: int = 42):
    random.seed(seed)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    episodes = []
    
    for i in range(1, n_samples + 1):
        domain_name, domain_desc, base_diff = random.choice(DOMAINS)
        difficulty = round(random.betavariate(2.0, 2.0) * 0.8 + 0.1, 3)
        
        # Ground truth outcome: 1 (Approve / Uphold) or 0 (Reject / Overturn)
        ground_truth = random.choice([0, 1])
        
        # Primary agent solo probability of correctness
        p_correct = 1.0 / (1.0 + math.exp(4.5 * (difficulty - 0.55)))
        solo_correct = random.random() < p_correct
        solo_answer = ground_truth if solo_correct else (1 - ground_truth)
        
        # Calibrated confidence C(x)
        if solo_correct:
            conf = min(0.98, max(0.20, random.betavariate(5.0, 2.0) * (1.1 - 0.4 * difficulty)))
        else:
            conf = min(0.85, max(0.05, random.betavariate(2.0, 4.0) * (0.9 - 0.3 * difficulty)))
        conf = round(conf, 4)
        
        # Gating rule: tau = 0.70
        consult_triggered = bool(conf < 0.70)
        
        if not consult_triggered:
            # Solo Fast-Path
            final_answer = solo_answer
            delphi_rounds = 0
            tokens_spent = int(random.gauss(380, 25))
            latency_s = round(max(0.4, random.gauss(0.84, 0.08)), 2)
            geval_score = round(max(0.25, min(0.65, random.gauss(0.45, 0.06))), 3)
            consult_helped = False
        else:
            # Delphi Peer Deliberation triggered (Pareto Separation)
            # Early exit chance
            early_exit = random.random() < 0.44 and difficulty < 0.65
            delphi_rounds = 1 if early_exit else (2 if random.random() < 0.80 else 3)
            
            # Peer consensus accuracy
            p_peer_correct = 0.72 / (1.0 + math.exp(2.8 * (difficulty - 0.68)))
            final_correct = random.random() < p_peer_correct
            final_answer = ground_truth if final_correct else (1 - ground_truth)
            
            tokens_spent = 380 + delphi_rounds * int(random.gauss(1280, 80))
            latency_s = round(0.84 + delphi_rounds * 1.40 + random.gauss(0, 0.15), 2)
            geval_score = round(max(0.60, min(0.85, random.gauss(0.74, 0.04))), 3)
            
            # Consult helped if it turned an incorrect solo answer into a correct final answer
            consult_helped = (not solo_correct) and final_correct
            
        episode = {
            "task_id": f"TASK_{i:04d}",
            "domain": domain_name,
            "query": f"[{domain_name}] Query #{i}: {domain_desc}",
            "difficulty": difficulty,
            "primary_answer": solo_answer,
            "primary_confidence": conf,
            "consult_triggered": consult_triggered,
            "delphi_rounds": delphi_rounds,
            "final_answer": final_answer,
            "ground_truth": ground_truth,
            "is_correct": (final_answer == ground_truth),
            "consult_helped": consult_helped,
            "tokens_spent": tokens_spent,
            "latency_s": latency_s,
            "geval_score": geval_score
        }
        episodes.append(episode)

    with open(output_file, 'w') as f:
        for ep in episodes:
            f.write(json.dumps(ep) + '\n')
            
    print(f"[SUCCESS] Generated {len(episodes)} structured decision episodes in {output_file}")
    
    # Compute quick stats
    consult_count = sum(1 for e in episodes if e['consult_triggered'])
    correct_count = sum(1 for e in episodes if e['is_correct'])
    helped_count = sum(1 for e in episodes if e['consult_helped'])
    total_tokens = sum(e['tokens_spent'] for e in episodes)
    
    print(f"Stats:")
    print(f"  Accuracy: {correct_count / n_samples * 100:.2f}%")
    print(f"  Consultation Trigger Rate: {consult_count / n_samples * 100:.2f}%")
    print(f"  Episodes where consultation fixed errors: {helped_count} ({helped_count / consult_count * 100:.2f}% of consultations)")
    print(f"  Average tokens per episode: {total_tokens / n_samples:.1f}")

if __name__ == '__main__':
    generate_dataset()
