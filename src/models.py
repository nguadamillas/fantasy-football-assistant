class Player:
    """
    Represents a Fantasy Premier League player.
    Wraps cleaned API data into a structured object.
    """

    POSITION_MAP = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }

    def __init__(self, id, name, team_id, position_id, price,
                 total_points, form, minutes, points_per_game,
                 selected_by_percent, status):

        self.id = id
        self.name = name
        self.team_id = team_id
        self.position_id = position_id
        self.price = price
        self.total_points = total_points
        self.form = form
        self.minutes = minutes
        self.points_per_game = points_per_game
        self.selected_by_percent = selected_by_percent
        self.status = status

    @property
    def position(self):
        """Return human-readable position name."""
        return self.POSITION_MAP.get(self.position_id, "Unknown")

    def __str__(self):
        return f"{self.name} ({self.position}) - £{self.price}m"

    def __repr__(self):
        return f"Player(id={self.id}, name={self.name})"

    def __eq__(self, other):
        return isinstance(other, Player) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        """Allows sorting players by total points."""
        return self.total_points < other.total_points


class Squad:
    """
    Represents a fantasy squad made of Player objects.
    Demonstrates composition: Squad contains Players.
    """

    def __init__(self, budget=100.0):
        self.budget = budget
        self.players = []   # mutable attribute

    def add_player(self, player):
        """Add a Player to the squad if budget allows."""
        if self.total_cost() + player.price > self.budget:
            raise ValueError("Budget exceeded!")
        self.players.append(player)

    def remove_player(self, player_id):
        """Remove a player by id."""
        self.players = [p for p in self.players if p.id != player_id]

    def total_cost(self):
        """Return total cost of the squad."""
        return sum(p.price for p in self.players)

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        return iter(self.players)

    def __str__(self):
        return f"Squad(players={len(self.players)}, cost={self.total_cost():.1f}/{self.budget})"