# SmartSpend 🪙

SmartSpend is a desktop-based personal finance assistant designed to eliminate the tedious, error-prone task of manual expense logging[cite: 1]. By leveraging Computer Vision and OCR, users can simply scan receipts to automatically extract total amounts, apply custom bill-splitting, categorize expenses, and track automated dynamic daily budgets[cite: 1].

Built entirely local-first to ensure maximum data privacy[cite: 1].

---

## 🚀 Key Features

*   **CV-Powered Receipt Scanner:** Automated text detection and extraction of bill totals using OpenCV and OCR[cite: 1].
*   **Smart Bill Splitting:** Instantly calculate your share via percentage presets (50%, 33%, 25%) or custom manual inputs[cite: 1].
*   **Manual Entry Option:** Quick manual logging fallback for expenses where printed bills aren't available[cite: 1].
*   **Dynamic Budget Rollover:** A toggleable budget tracker that dynamically carries over surpluses or deficits to the next day[cite: 1].
*   **Expense Categorization:** Automated mapping to primary spending buckets (Food, Transport, Shopping, Entertainment, Health, Misc)[cite: 1].
*   **Groq AI Insights (Phase 2):** Integrated local analysis via Groq API (Llama-based models) to analyze spending trends and suggest optimization strategies[cite: 1].

---

## 🛠️ Tech Stack

*   **Core Logic:** Python[cite: 1]
*   **Computer Vision:** OpenCV / OCR (EasyOCR or Pytesseract)[cite: 1]
*   **Database:** SQLite / JSON (Local storage persistence)[cite: 1]
*   **User Interface:** CustomTkinter (Sleek, modern desktop UI)[cite: 1]
*   **AI Engine:** Groq API[cite: 1]

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