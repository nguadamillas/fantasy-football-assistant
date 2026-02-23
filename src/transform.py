from .models import Player


def clean_player_record(p: dict) -> dict:
    """
    Convert raw API player dict into a simplified dict.
    """
    return {
        "id": p["id"],
        "name": p["web_name"],
        "team_id": p["team"],
        "position_id": p["element_type"],
        "price": p["now_cost"] / 10,
        "total_points": p["total_points"],
        "form": float(p["form"]) if p.get("form") else 0.0,
        "minutes": p["minutes"],
        "points_per_game": float(p["points_per_game"]) if p.get("points_per_game") else 0.0,
        "selected_by_percent": float(p["selected_by_percent"]) if p.get("selected_by_percent") else 0.0,
        "status": p["status"],
    }


def build_player_objects(data: dict) -> list[Player]:
    """
    Build Player objects from FPL bootstrap-static response dict.
    """
    raw_players = data["elements"]
    cleaned = [clean_player_record(p) for p in raw_players]

    return [
        Player(
            id=p["id"],
            name=p["name"],
            team_id=p["team_id"],
            position_id=p["position_id"],
            price=p["price"],
            total_points=p["total_points"],
            form=p["form"],
            minutes=p["minutes"],
            points_per_game=p["points_per_game"],
            selected_by_percent=p["selected_by_percent"],
            status=p["status"],
        )
        for p in cleaned
    ]