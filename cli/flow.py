import sys
import os
import re
from datetime import datetime
import cv2
import numpy as np

import config
import budget.engine as engine
import cv.capture as capture
import cv.preprocess as preprocess
import cv.ocr as ocr
import cv.extractor as extractor
from db.queries import (
    get_yesterday_leftover,
    add_expense,
    get_daily_total,
    get_expenses_by_date
)

import sys
import os
import re
from datetime import datetime
import cv2
import numpy as np

def get_current_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def handle_shared_amount_logic(extracted_amount: float) -> float:
    print(f"Total Amount: {extracted_amount}")
    print("Enter your share (e.g., '50%', '150', or press Enter for full amount):")
    split_input = input().strip()
    if not split_input:
        return extracted_amount
    if split_input.endswith("%"):
        try:
            percentage = float(split_input.replace("%", "").strip())
            return (percentage / 100.0) * extracted_amount
        except ValueError:
            print("Invalid percentage format. Defaulting to full amount.")
            return extracted_amount
    else:
        try:
            return float(split_input)
        except ValueError:
            print("Invalid numeric entry. Defaulting to full amount.")
            return extracted_amount

def handle_category_selection() -> str:
    while True:
        print("Select a category:")
        for idx, cat in enumerate(config.VALID_CATEGORIES, 1):
            print(f"{idx}. {cat}")
        choice = input().strip()
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(config.VALID_CATEGORIES):
                return config.VALID_CATEGORIES[choice_idx]
        except ValueError:
            pass
        print("Invalid selection. Try again.")

def scan_flow():
    print("Enter image file path (or type 'webcam'):")
    source_input = input().strip()
    raw_text = ""
    try:
        raw_img = capture.load_image(source_input)
        clean_img = preprocess.preprocess(raw_img)
        raw_text = ocr.extract_text(clean_img)
        final_amount = extractor.extract_total(raw_text)
    except Exception as e:
        print(f"Scanner failed, please enter amount manually. Error: {e}")
        final_amount = None

    if final_amount is not None:
        print(f"Extracted Amount: {final_amount}")
        print("Is this amount correct? (y/n):")
        confirm = input().strip().lower()
        if confirm != 'y':
            final_amount = None
            
    if final_amount is None:
        while True:
            print("Enter bill total manually:")
            try:
                final_amount = float(input())
                break
            except ValueError:
                print("Invalid number format.")

    user_share = handle_shared_amount_logic(final_amount)
    category = handle_category_selection()
    print("Enter a description/item note:")
    description = input().strip()
    today_str = get_current_date_str()
    
    add_expense(
        date=today_str,
        amount=final_amount,
        category=category,
        description=description,
        user_share=user_share,
        source="scan",
        raw_text=raw_text
    )
    print("Expense successfully saved to database.")

def manual_flow():
    while True:
        print("Enter bill total:")
        try:
            final_amount = float(input())
            if final_amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid number format.")

    user_share = handle_shared_amount_logic(final_amount)
    category = handle_category_selection()
    print("Enter a description/item note:")
    description = input().strip()
    today_str = get_current_date_str()
    
    add_expense(
        date=today_str,
        amount=final_amount,
        category=category,
        description=description,
        user_share=user_share,
        source="manual",
        raw_text=description
    )
    print("Expense successfully saved to database.")

def view_budget_flow():
    today_str = get_current_date_str()
    print(f"Budget Status for Date: {today_str}")
    
    print("\n--- Itemized Daily Spending ---")
    expenses = get_expenses_by_date(today_str)
    if not expenses:
        print("No expenses recorded today.")
    for exp in expenses:
        print(f"- [{exp['category']}] {exp['description']}: Total: {exp['amount']} | Your Share: {exp['user_share']}")
    
    total_spent_today = get_daily_total(today_str)
    yesterday_leftover = get_yesterday_leftover(today_str)

    effective_budget, remaining = engine.get_budget_state(
        today_date=today_str,
        daily_budget=config.DAILY_BUDGET,
        rollover_enabled=config.ROLLOVER_ENABLED,
        yesterday_leftover=yesterday_leftover,
        amount_spent_today=total_spent_today
    )

    print("\n--- Financial Summary ---")
    print(f"Base Budget       : {config.DAILY_BUDGET}")
    print(f"Rollover Balance  : {yesterday_leftover}")
    print(f"Effective Budget  : {effective_budget}")
    print(f"Total Spent Today : {total_spent_today}")
    print(f"Remaining Balance : {remaining}")
    
    if remaining < 0:
        print(f"Warning: You are over limit by {abs(remaining)}")