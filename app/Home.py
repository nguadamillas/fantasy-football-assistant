import sys
from pathlib import Path
import streamlit as st

# ----------------------------
# Make src imports work
# ----------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.data_api import fetch_bootstrap_static
from src.transform import build_player_objects
from src.advisor_engine import Advisor
from src.rules import BudgetRule, MaxFromTeamRule
from src.team_builder import build_starting_xi

# ----------------------------
# Streamlit setup
# ----------------------------
st.set_page_config(page_title="Fantasy Assistant", page_icon="⚽", layout="wide")
st.title("⚽ Fantasy Football Assistant")
st.caption("Best XI Builder (FPL public API)")

# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.header("Controls")
formation = st.sidebar.selectbox(
    "Formation (DEF-MID-FWD)",
    ["3-4-3", "3-5-2", "4-4-2", "4-3-3", "5-3-2"],
)
budget = st.sidebar.slider("Budget (£m)", 50.0, 100.0, 100.0, 0.5)

# ----------------------------
# Load data
# ----------------------------
with st.spinner("Loading data..."):
    data = fetch_bootstrap_static(ttl_seconds=3600)
    players = build_player_objects(data)

# ----------------------------
# Advisor with rules
# ----------------------------
advisor = Advisor(rules=[BudgetRule(), MaxFromTeamRule(max_per_team=3)])

# ----------------------------
# Build XI + display
# ----------------------------
try:
    xi = build_starting_xi(players, advisor, formation=formation, budget=budget)

    st.subheader(f"Best XI — {formation} (Budget £{budget}m)")
    st.write(str(xi))

    table = [{
        "Name": p.name,
        "Position": p.position,
        "Price": p.price,
        "Total Points": p.total_points,
        "Minutes": p.minutes,
        "Score": round(advisor.score(p), 2),
    } for p in xi]

    st.dataframe(table, use_container_width=True)

except Exception as e:
    st.error(f"Could not build XI: {e}")