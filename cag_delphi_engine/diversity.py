"""
Pareto Diversity Allocation (PDA) Module
Implements CVF continuous Separation and Blau Variety constraints from Lee & Kwon (2026).
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class CVFArchetype:
    name: str
    focus: float      # -1.0 (Internal) to +1.0 (External)
    structure: float  # -1.0 (Stability) to +1.0 (Flexibility)

    @property
    def vector(self) -> Tuple[float, float]:
        return (self.focus, self.structure)

CLAN = CVFArchetype("Clan (Collaborative / Human)", focus=-1.0, structure=1.0)
ADHOCRACY = CVFArchetype("Adhocracy (Innovative / Agility)", focus=1.0, structure=1.0)
MARKET = CVFArchetype("Market (Competitive / Results)", focus=1.0, structure=-1.0)
HIERARCHY = CVFArchetype("Hierarchy (Control / Precision)", focus=-1.0, structure=-1.0)

@dataclass
class AgentPersona:
    agent_id: str
    archetype: CVFArchetype
    personality_style: str = "Analytical-Conscientious"  # Standardized to eliminate Variety friction
    influence_weight: float = 0.20

class ParetoDiversityAllocator:
    """
    Tier 2: Pareto Diversity Allocation (PDA)
    Selects peer agents maximizing Separation S while bounding Variety V and Disparity D.
    """
    def __init__(self, v_max: float = 0.20, delta_d: float = 0.05):
        self.v_max = v_max
        self.delta_d = delta_d

    @staticmethod
    def calculate_separation(agents: List[AgentPersona]) -> float:
        """
        Normalized pairwise Euclidean distance across CVF coordinates in [0.0, 1.0].
        Max possible distance in [-1, 1]^2 is sqrt(4 + 4) = sqrt(8) ~ 2.8284.
        """
        m = len(agents)
        if m < 2:
            return 0.0
        
        total_dist = 0.0
        pairs = 0
        for i in range(m - 1):
            for j in range(i + 1, m):
                v1 = agents[i].archetype.vector
                v2 = agents[j].archetype.vector
                dist = math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
                total_dist += dist
                pairs += 1
                
        avg_dist = total_dist / pairs
        norm_separation = avg_dist / math.sqrt(8.0)
        return round(norm_separation, 4)

    @staticmethod
    def calculate_blau_variety(agents: List[AgentPersona]) -> float:
        """
        Blau Index of Variety over categorical personality styles:
        V = 1 - sum(p_k^2)
        """
        m = len(agents)
        if m < 2:
            return 0.0
        counts: Dict[str, int] = {}
        for a in agents:
            counts[a.personality_style] = counts.get(a.personality_style, 0) + 1
            
        sum_sq = sum((c / m) ** 2 for c in counts.values())
        return round(1.0 - sum_sq, 4)

    @staticmethod
    def calculate_disparity(agents: List[AgentPersona]) -> float:
        """
        Coefficient of variation across influence weights:
        D = sigma(w) / mu(w)
        """
        m = len(agents)
        if m < 2:
            return 0.0
        weights = [a.influence_weight for a in agents]
        mu = sum(weights) / m
        var = sum((w - mu) ** 2 for w in weights) / m
        sigma = math.sqrt(var)
        return round(sigma / mu if mu > 0 else 0.0, 4)

    def allocate_pareto_panel(self, panel_size: int = 4) -> List[AgentPersona]:
        """
        Constructs the Pareto-optimal panel maximizing CVF Separation
        while enforcing low Variety (V <= V_max) and uniform Disparity (D = 0).
        """
        # Select balanced opposing archetypes
        archetypes = [CLAN, ADHOCRACY, MARKET, HIERARCHY]
        selected_archetypes = archetypes[:panel_size]
        
        equal_weight = 1.0 / panel_size
        panel = [
            AgentPersona(
                agent_id=f"Peer_{i+1}",
                archetype=selected_archetypes[i],
                personality_style="Analytical-Conscientious", # Zero variety friction
                influence_weight=equal_weight
            )
            for i in range(panel_size)
        ]
        return panel
