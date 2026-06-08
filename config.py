from db.queries import get_settings

VALID_CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Housing", "Misc"]

try:
    _raw_settings = get_settings()
except Exception as e:
    _raw_settings = {"daily_budget": "50.00", "rollover_enabled": "false"}

DAILY_BUDGET = float(_raw_settings.get("daily_budget", 50.00))
ROLLOVER_ENABLED = _raw_settings.get("rollover_enabled", "false").lower() == "true"