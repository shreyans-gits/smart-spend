def get_budget_state(today_date: str, daily_budget: float, rollover_enabled: bool, yesterday_leftover: float, amount_spent_today: float) -> tuple[float, float]:
    if rollover_enabled:
        effective_budget = daily_budget + yesterday_leftover
    else:
        effective_budget = daily_budget

    remaining = effective_budget - amount_spent_today

    return effective_budget, remaining

# Self-contained unit tests to verify the arithmetic works perfectly without a DB
if __name__ == "__main__":
    print("Running engine internal sanity checks...")
    eff_b, rem = get_budget_state("2026-06-11", 50.0, True, 15.0, 20.0)
    assert eff_b == 65.0 and rem == 45.0, f"Test 1 Failed: Got ({eff_b}, {rem})"

    eff_b, rem = get_budget_state("2026-06-11", 50.0, False, 15.0, 20.0)
    assert eff_b == 50.0 and rem == 30.0, f"Test 2 Failed: Got ({eff_b}, {rem})"

    eff_b, rem = get_budget_state("2026-06-11", 50.0, True, -10.0, 10.0)
    assert eff_b == 40.0 and rem == 30.0, f"Test 3 Failed: Got ({eff_b}, {rem})"

    print("All engine calculations passed perfectly!")