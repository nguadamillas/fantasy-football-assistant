from .models import Player


def player_score(player, w_points=1.0, w_form=8.0, w_ppg=6.0, w_minutes=0.002, w_value=10.0):
    """
    Compute a recommendation score for a player.
    Uses weighted components for ranking.
    """
    value = (player.total_points / player.price) if player.price > 0 else 0.0

    return (
        w_points * player.total_points +
        w_form * player.form +
        w_ppg * player.points_per_game +
        w_minutes * player.minutes +
        w_value * value
    )


POSITION_NAME_TO_ID = {
    "GK": 1,
    "DEF": 2,
    "MID": 3,
    "FWD": 4
}


def recommend_players(players, limit=10, **filters):
    """
    Yield top recommended players based on optional filters.
    Demonstrates generator + **kwargs usage.
    """

    filtered = players

    if "position" in filters:
        pos_id = POSITION_NAME_TO_ID[filters["position"]]
        filtered = [p for p in filtered if p.position_id == pos_id]

    if "max_price" in filters:
        filtered = [p for p in filtered if p.price <= filters["max_price"]]

    if "min_minutes" in filters:
        filtered = [p for p in filtered if p.minutes >= filters["min_minutes"]]

    if "team_id" in filters:
        filtered = [p for p in filtered if p.team_id == filters["team_id"]]

    scored = [(p, player_score(p)) for p in filtered]
    scored.sort(key=lambda x: x[1], reverse=True)

    for item in scored[:limit]:
        yield item