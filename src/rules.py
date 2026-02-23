from collections import Counter
from .validators import validate_formation


class RuleViolation(Exception):
    """Raised when a squad rule is violated."""
    pass


class BaseRule:
    """
    Base class for squad validation rules.
    Child classes must implement validate(squad).
    """
    def validate(self, squad):
        raise NotImplementedError("Subclasses must implement validate().")


class BudgetRule(BaseRule):
    """Ensures squad cost does not exceed the budget."""
    def validate(self, squad):
        if squad.total_cost() > squad.budget:
            raise RuleViolation(f"Budget exceeded: {squad.total_cost():.1f} > {squad.budget:.1f}")


class FormationRule(BaseRule):
    """
    Ensures the squad matches a formation like 3-5-2.
    Format: DEF-MID-FWD (GK is always 1 in normal fantasy rules).
    """
    def __init__(self, formation: str):
        if not validate_formation(formation):
            raise ValueError("Invalid formation format. Use '3-5-2' etc.")
        self.formation = formation

    def validate(self, squad):
        def_count, mid_count, fwd_count = [int(x) for x in self.formation.split("-")]

        # Count positions in squad
        pos_counts = Counter([p.position_id for p in squad])

        gk = pos_counts.get(1, 0)
        de = pos_counts.get(2, 0)
        mi = pos_counts.get(3, 0)
        fw = pos_counts.get(4, 0)

        # Simple rule: enforce exact match + 1 GK
        if gk != 1 or de != def_count or mi != mid_count or fw != fwd_count:
            raise RuleViolation(
                f"Formation mismatch. Expected GK=1 DEF={def_count} MID={mid_count} FWD={fwd_count} "
                f"but got GK={gk} DEF={de} MID={mi} FWD={fw}"
            )


class MaxFromTeamRule(BaseRule):
    """Ensures no more than max_per_team players are selected from the same team."""
    def __init__(self, max_per_team=3):
        self.max_per_team = max_per_team

    def validate(self, squad):
        team_counts = Counter([p.team_id for p in squad])
        for team_id, count in team_counts.items():
            if count > self.max_per_team:
                raise RuleViolation(f"Too many players from team {team_id}: {count} > {self.max_per_team}")