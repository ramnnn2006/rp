"""
Early-Stopping Delphi Consensus Engine (ESCE)
Tracks consensus stability (Delta_kappa), G-Eval quality, and budget ceilings.
"""

import math
import random
from typing import List, Dict, Any, Tuple
from .diversity import AgentPersona
from .gating import GEvalEvaluator

class EarlyStoppingDelphiEngine:
    """
    Tier 3: Early-Stopping Delphi Consensus Engine (ESCE)
    Replaces static 3-round polling with adaptive convergence termination.
    """
    def __init__(self, 
                 max_rounds: int = 3, 
                 w_target: float = 0.75, 
                 epsilon_stability: float = 0.05, 
                 token_budget: int = 4500,
                 tokens_per_peer_round: int = 320):
        self.max_rounds = max_rounds
        self.w_target = w_target
        self.eps = epsilon_stability
        self.budget = token_budget
        self.tokens_per_peer_round = tokens_per_peer_round
        self.geval = GEvalEvaluator(target_score=0.74)

    def execute_delphi(self, 
                       query: str, 
                       difficulty: float, 
                       primary_is_correct: bool, 
                       panel: List[AgentPersona]) -> Dict[str, Any]:
        """
        Executes multi-round Delphi deliberation with early exit.
        """
        m = len(panel) + 1 # Include primary agent
        tokens_spent = 380 # Initial primary agent tokens
        
        # Peer correction parameters calibrated to Lee & Kwon (2026) Separation condition
        p_correct_round1 = 0.65 - 0.20 * (difficulty - 0.5)
        p_correct_round2 = 0.82 - 0.15 * (difficulty - 0.5)
        
        rounds_executed = 0
        w_history: List[float] = []
        geval_history: List[float] = []
        is_correct = primary_is_correct
        
        for r in range(1, self.max_rounds + 1):
            rounds_executed = r
            tokens_spent += (m - 1) * self.tokens_per_peer_round
            
            # Simulate round-level consensus accuracy
            if r == 1:
                is_correct = bool(random.random() < p_correct_round1)
                w_current = min(0.95, random.gauss(0.68, 0.06))
            else:
                is_correct = bool(random.random() < p_correct_round2)
                w_current = min(0.98, w_history[-1] + random.uniform(0.08, 0.18))
                
            w_history.append(round(w_current, 4))
            
            # G-Eval assessment at round r
            geval_res = self.geval.evaluate(query, f"consensus_output_round_{r}", is_consensus=True, difficulty=difficulty)
            geval_score = geval_res['geval_score']
            geval_history.append(geval_score)
            
            # Stopping check 1: Target consensus reached
            if w_current >= self.w_target and geval_score >= 0.74:
                break
                
            # Stopping check 2: Marginal stability epsilon reached
            if r > 1:
                delta_kappa = abs(w_history[-1] - w_history[-2])
                if delta_kappa < self.eps:
                    break
                    
            # Stopping check 3: Token budget ceiling
            if tokens_spent >= self.budget:
                break
                
        return {
            'final_decision_correct': is_correct,
            'rounds_executed': rounds_executed,
            'tokens_spent': tokens_spent,
            'final_kendall_w': w_history[-1],
            'final_geval_score': geval_history[-1],
            'early_exit_fired': bool(rounds_executed < self.max_rounds),
            'w_history': w_history,
            'geval_history': geval_history
        }
