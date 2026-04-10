"""Open Interest change computation."""

from app.state.state_manager import StateManager


def compute_oi_change(state: StateManager, option: dict) -> float:
    """Return the difference between current and previous OI for *option*.

    Returns 0.0 for newly-seen contracts (first tick).
    """
    prev_oi = state.get_oi(
        option["symbol"],
        option["strike"],
        option["option_type"],
    )
    current_oi = option.get("oi", 0.0)
    return current_oi - prev_oi
