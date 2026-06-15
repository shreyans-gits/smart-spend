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
from db.queries import get_yesterday_leftover

def get_current_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def handle_shared_amount_logic(extracted_amount: float) -> float:
    split_input = input().strip()
    if not split_input:
        return extracted_amount
    if split_input.endswith("%"):
        try:
            percentage = float(split_input.replace("%", "").strip())
            return (percentage / 100.0) * extracted_amount
        except ValueError:
            return extracted_amount
    else:
        try:
            return float(split_input)
        except ValueError:
            return extracted_amount

def handle_category_selection() -> str:
    while True:
        for idx, cat in enumerate(config.VALID_CATEGORIES, 1):
            print(f"{idx}. {cat}")
        choice = input().strip()
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(config.VALID_CATEGORIES):
                return config.VALID_CATEGORIES[choice_idx]
        except ValueError:
            pass

def scan_flow():
    source_input = input().strip()
    try:
        raw_img = capture.load_image(source_input)
        clean_img = preprocess.preprocess(raw_img)
        raw_text = ocr.extract_text(clean_img)
        final_amount = extractor.extract_total(raw_text)
    except Exception:
        final_amount = None

    if final_amount is not None:
        print(final_amount)
        confirm = input().strip().lower()
        if confirm != 'y':
            final_amount = None
            
    if final_amount is None:
        while True:
            try:
                final_amount = float(input())
                break
            except ValueError:
                pass

    user_share = handle_shared_amount_logic(final_amount)
    category = handle_category_selection()
    description = input().strip()
    today_str = get_current_date_str()
    print(f"{today_str} | {final_amount} | {user_share} | {category}")

def manual_flow():
    while True:
        try:
            final_amount = float(input())
            if final_amount <= 0:
                continue
            break
        except ValueError:
            pass

    user_share = handle_shared_amount_logic(final_amount)
    category = handle_category_selection()
    description = input().strip()
    today_str = get_current_date_str()
    print(f"{today_str} | {final_amount} | {user_share} | {category}")

def view_budget_flow():
    today_str = get_current_date_str()
    print(today_str)
    
    total_spent_today = 35.00  
    yesterday_leftover = get_yesterday_leftover(today_str)

    effective_budget, remaining = engine.get_budget_state(
        today_date=today_str,
        daily_budget=config.DAILY_BUDGET,
        rollover_enabled=config.ROLLOVER_ENABLED,
        yesterday_leftover=yesterday_leftover,
        amount_spent_today=total_spent_today
    )

    print(config.DAILY_BUDGET)
    print(yesterday_leftover)
    print(effective_budget)
    print(total_spent_today)
    print(remaining)