from db.schema import init_db

def main():
    print("--- Step 1: Initializing the Database ---")
    init_db()
    print("Database initialization step verified.\n")

    print("--- Step 2: Importing Configuration Pipeline ---")
    import config
    
    print("--- Step 3: Verifying Extracted Configuration Values ---")
    print(f"DAILY_BUDGET     : {config.DAILY_BUDGET} (Type: {type(config.DAILY_BUDGET).__name__})")
    print(f"ROLLOVER_ENABLED : {config.ROLLOVER_ENABLED} (Type: {type(config.ROLLOVER_ENABLED).__name__})")
    print(f"VALID_CATEGORIES : {config.VALID_CATEGORIES}")
    
    print("\n--- Status ---")
    if config.DAILY_BUDGET == 50.0 and config.ROLLOVER_ENABLED is False:
        print("Success! The data pipeline chain is solid. Clear for Phase 2.")
    else:
        print("Warning: Loaded configuration does not match default expectations.")

if __name__ == "__main__":
    main()