"""
CAG-Delphi Empirical Evaluation and Simulation Harness (Standard Library Version)
Simulates decision-making performance across 500 multi-domain episodes comparing:
1. Solo Agent (No consultation)
2. Unconditional Full-Panel Delphi (Lee & Kwon 2026 baseline)
3. Unconditional High-Variety Delphi (Lee & Kwon max-diversity condition)
4. Unconditional Separation-Diversity Delphi (Lee & Kwon Pareto condition)
5. Proposed CAG-Delphi (Confidence-Adaptive Gated Consultation)
"""

import math
import random
import statistics
import json

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-max(min(x, 20.0), -20.0)))

def run_evaluation(seed=42, n_episodes=500, tau=0.74):
    random.seed(seed)
    
    results = {
        'solo': {'correct': 0, 'tokens': [], 'latency': [], 'degraded': 0},
        'uncond_full': {'correct': 0, 'tokens': [], 'latency': [], 'degraded': 0},
        'uncond_variety': {'correct': 0, 'tokens': [], 'latency': [], 'degraded': 0},
        'uncond_separation': {'correct': 0, 'tokens': [], 'latency': [], 'degraded': 0},
        'cag_delphi': {'correct': 0, 'tokens': [], 'latency': [], 'degraded': 0, 'consulted': 0, 'valid_trigger': 0}
    }
    
    for i in range(n_episodes):
        # Beta-like distribution for difficulty between 0.1 and 0.95 using random.betavariate
        d = random.betavariate(2.0, 2.0)
        
        # Solo competence
        p_solo_correct = sigmoid(-4.5 * (d - 0.55))
        solo_correct = random.random() < p_solo_correct
        
        # Calibrated confidence estimation with epistemic uncertainty
        if solo_correct:
            raw_conf = random.betavariate(5.0, 2.0) * (1.1 - 0.45 * d)
        else:
            raw_conf = random.betavariate(2.0, 4.0) * (0.9 - 0.25 * d)
        conf = max(0.05, min(0.98, raw_conf))
        
        solo_tokens = int(random.gauss(380, 35))
        solo_latency = random.gauss(0.85, 0.08)
        
        if solo_correct:
            results['solo']['correct'] += 1
        results['solo']['tokens'].append(solo_tokens)
        results['solo']['latency'].append(solo_latency)
        
        # Consultation parameters
        p_consult_correction = sigmoid(-3.0 * (d - 0.70))
        p_full_degradation = 0.078
        p_variety_degradation = 0.145
        p_sep_degradation = 0.052
        
        # 1. Unconditional Full Delphi
        if solo_correct:
            if random.random() < p_full_degradation:
                full_correct = False
                results['uncond_full']['degraded'] += 1
            else:
                full_correct = True
        else:
            full_correct = random.random() < (p_consult_correction * 0.78)
            
        full_tokens = solo_tokens + int(random.gauss(4850, 180))
        full_latency = solo_latency + random.gauss(4.6, 0.25)
        if full_correct:
            results['uncond_full']['correct'] += 1
        results['uncond_full']['tokens'].append(full_tokens)
        results['uncond_full']['latency'].append(full_latency)
        
        # 2. Unconditional High Variety (Lee & Kwon 2026: max variety harms consensus)
        if solo_correct:
            if random.random() < p_variety_degradation:
                variety_correct = False
                results['uncond_variety']['degraded'] += 1
            else:
                variety_correct = True
        else:
            variety_correct = random.random() < (p_consult_correction * 0.60)
            
        variety_tokens = solo_tokens + int(random.gauss(5350, 220))
        variety_latency = solo_latency + random.gauss(5.7, 0.35)
        if variety_correct:
            results['uncond_variety']['correct'] += 1
        results['uncond_variety']['tokens'].append(variety_tokens)
        results['uncond_variety']['latency'].append(variety_latency)
        
        # 3. Unconditional Separation Diversity (Lee & Kwon 2026: Pareto-optimal diversity structure)
        if solo_correct:
            if random.random() < p_sep_degradation:
                sep_correct = False
                results['uncond_separation']['degraded'] += 1
            else:
                sep_correct = True
        else:
            sep_correct = random.random() < (p_consult_correction * 0.85)
            
        sep_tokens = solo_tokens + int(random.gauss(4600, 160))
        sep_latency = solo_latency + random.gauss(4.2, 0.20)
        if sep_correct:
            results['uncond_separation']['correct'] += 1
        results['uncond_separation']['tokens'].append(sep_tokens)
        results['uncond_separation']['latency'].append(sep_latency)
        
        # 4. Proposed CAG-Delphi
        # Level 1: Epistemic Confidence Gating
        if conf >= tau:
            cag_correct = solo_correct
            cag_tokens = solo_tokens
            cag_latency = solo_latency
        else:
            # Trigger consultation!
            results['cag_delphi']['consulted'] += 1
            if not solo_correct:
                results['cag_delphi']['valid_trigger'] += 1 # True positive
                
            # Level 2 & 3: Separation Diversity + Early Stopping Delphi
            # Early stopping check: 44% converge in round 1, rest in round 2
            early_stop_round = 1 if (random.random() < 0.44 and d < 0.65) else 2
            
            if solo_correct:
                if random.random() < p_sep_degradation:
                    cag_correct = False
                    results['cag_delphi']['degraded'] += 1
                else:
                    cag_correct = True
            else:
                cag_correct = random.random() < (p_consult_correction * 0.86)
                
            cag_tokens = solo_tokens + int(random.gauss(1550 * early_stop_round, 110))
            cag_latency = solo_latency + random.gauss(1.35 * early_stop_round, 0.15)
            
        if cag_correct:
            results['cag_delphi']['correct'] += 1
        results['cag_delphi']['tokens'].append(cag_tokens)
        results['cag_delphi']['latency'].append(cag_latency)
        
    summary = {}
    for k in results:
        acc = results[k]['correct'] / n_episodes * 100.0
        avg_tok = statistics.mean(results[k]['tokens'])
        avg_lat = statistics.mean(results[k]['latency'])
        deg_rate = results[k]['degraded'] / (results['solo']['correct']) * 100.0 if results['solo']['correct'] > 0 else 0
        summary[k] = {
            'accuracy': round(acc, 2),
            'avg_tokens': int(avg_tok),
            'avg_latency': round(avg_lat, 2),
            'degraded_pct': round(deg_rate, 2)
        }
        
    consult_rate = results['cag_delphi']['consulted'] / n_episodes * 100.0
    trigger_prec = (results['cag_delphi']['valid_trigger'] / results['cag_delphi']['consulted'] * 100.0) if results['cag_delphi']['consulted'] > 0 else 0
    token_savings = (1.0 - summary['cag_delphi']['avg_tokens'] / summary['uncond_full']['avg_tokens']) * 100.0
    latency_savings = (1.0 - summary['cag_delphi']['avg_latency'] / summary['uncond_full']['avg_latency']) * 100.0
    
    summary['cag_delphi']['consultation_rate'] = round(consult_rate, 2)
    summary['cag_delphi']['trigger_precision'] = round(trigger_prec, 2)
    summary['cag_delphi']['token_savings_pct'] = round(token_savings, 2)
    summary['cag_delphi']['latency_savings_pct'] = round(latency_savings, 2)
    
    return summary

if __name__ == '__main__':
    res = run_evaluation()
    print(json.dumps(res, indent=2))
