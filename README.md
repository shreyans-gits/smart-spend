# SmartSpend 🪙

SmartSpend is a desktop-based personal finance assistant designed to eliminate the tedious, error-prone task of manual expense logging. By leveraging Computer Vision and OCR, users can simply scan receipts to automatically extract total amounts, apply custom bill-splitting, categorize expenses, and track automated dynamic daily budgets.

Built entirely local-first to ensure maximum data privacy.

---

## 🚀 Key Features

*   **CV-Powered Receipt Scanner:** Automated text detection and extraction of bill totals using OpenCV and OCR.
*   **Smart Bill Splitting:** Instantly calculate your share via percentage presets (50%, 33%, 25%) or custom manual inputs.
*   **Manual Entry Option:** Quick manual logging fallback for expenses where printed bills aren't available.
*   **Dynamic Budget Rollover:** A toggleable budget tracker that dynamically carries over surpluses or deficits to the next day.
*   **Expense Categorization:** Automated mapping to primary spending buckets (Food, Transport, Shopping, Entertainment, Health, Misc).
*   **Groq AI Insights (Phase 2):** Integrated local analysis via Groq API (Llama-based models) to analyze spending trends and suggest optimization strategies.

---

## 🛠️ Tech Stack

*   **Core Logic:** Python
*   **Computer Vision:** OpenCV / OCR (EasyOCR or Pytesseract)
*   **Database:** SQLite / JSON (Local storage persistence)
*   **User Interface:** CustomTkinter (Sleek, modern desktop UI)
*   **AI Engine:** Groq API

---

## 📂 Project Structure

```text
smart_spend/
│
├── data/
│   └── spend.db             # Local SQLite database file
│
├── core/
│   ├── database.py          # Schema definitions and CRUD operations
│   ├── budget_engine.py     # Rollover calculations & budget logic
│   └── ocr_engine.py        # OpenCV image preprocessing & text extraction
│
├── ui/
│   ├── app.py               # Main CustomTkinter UI loop
│   └── components.py        # Reusable custom UI widgets
│
├── tests/
│   └── test_logic.py        # Terminal-based harness to verify backend logic
│
├── config.py                # Global configurations (categories, presets)
└── main.py                  # Application entry point