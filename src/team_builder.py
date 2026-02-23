from .models import Squad
from .models import Squad
from .rules import FormationRule
from .advisor_engine import Advisor


def build_starting_xi(players, advisor: Advisor, formation="4-4-2", budget=100.0):
    """
    Build a starting XI using advisor scores under formation + budget influence.

    Strategy (simple and defendable):
    - Create a per-position price cap derived from total budget.
    - Only choose candidates under that cap.
    - Pick highest scored players per position within the cap.
    """
    rule = FormationRule(formation)
    def_count, mid_count, fwd_count = [int(x) for x in formation.split("-")]
    total_players = 11

    # Simple budget allocation percentages (can tweak later)
    # GK 10%, DEF 35%, MID 35%, FWD 20%
    caps = {
        1: (budget * 0.10) / 1,          # GK
        2: (budget * 0.35) / def_count,  # DEF
        3: (budget * 0.35) / mid_count,  # MID
        4: (budget * 0.20) / fwd_count,  # FWD
    }

    xi = Squad(budget=budget)

    def top_scored(position_id, n):
        cap = caps[position_id]
        candidates = [
            p for p in players
            if p.position_id == position_id
            and p.status == "a"
            and p.price <= cap
        ]
        scored = [(p, advisor.score(p)) for p in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [p for p, _ in scored[:n]]

    # Pick players under caps
    for p in top_scored(1, 1):
        xi.add_player(p)

    for p in top_scored(2, def_count):
        xi.add_player(p)

    for p in top_scored(3, mid_count):
        xi.add_player(p)

    for p in top_scored(4, fwd_count):
        xi.add_player(p)

    rule.validate(xi)
    return xi