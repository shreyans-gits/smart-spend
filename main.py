import sys
from db.schema import init_db
from cli.flow import scan_flow, manual_flow, view_budget_flow

init_db()
import config

print("=== Smart Spend CLI Terminal Active ===")

try:
    while True:
        print("\n1. Log expense (scan)\n2. Log expense (manual)\n3. View today's budget\n4. Exit")
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            scan_flow()
        elif choice == "2":
            manual_flow()
        elif choice == "3":
            view_budget_flow()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option, try again.")
except KeyboardInterrupt:
    print("\n\nSession interrupted. Goodbye!")
    sys.exit(0)