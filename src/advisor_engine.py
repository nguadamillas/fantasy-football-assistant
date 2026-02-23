from .advisor import player_score, recommend_players
from .rules import RuleViolation


class Advisor:
    """
    Fantasy Football Advisor.
    Demonstrates composition: an Advisor has a list of rules
    and uses scoring to recommend players.
    """

    def __init__(self, rules=None):
        self.rules = rules or []

    def validate_squad(self, squad) -> list[str]:
        """
        Validate a squad against all rules.
        Returns a list of violation messages (empty if OK).
        """
        errors = []
        for rule in self.rules:
            try:
                rule.validate(squad)
            except RuleViolation as e:
                errors.append(str(e))
        return errors

    def top_recommendations(self, players, limit=10, **filters):
        """
        Return a list of (Player, score) recommendations using **kwargs filters.
        """
        return list(recommend_players(players, limit=limit, **filters))

    def score(self, player):
        """Expose score function for UI."""
        return player_score(player)