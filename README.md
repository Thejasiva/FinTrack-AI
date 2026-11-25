# FinTrack AI

**AI-Powered Personal Finance Management System with Smart Expense Analysis and Budget Recommendations**

A beginner-friendly final-year project built with Python, Flask, SQLite, HTML, CSS, Chart.js, and Scikit-learn.

## Features

- Add and delete expenses
- Assign expenses to categories
- Save a monthly budget
- View current-month spending and remaining budget
- Display category-wise spending in a chart
- Generate a simple Linear Regression budget estimate
- Show spending tips and a monthly report
- Store data locally in SQLite

## Requirements

- Python 3.10 or newer
- Internet connection for the Chart.js CDN when viewing charts

## Run on Windows

Open Command Prompt or PowerShell in this project folder.

1. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

2. Activate it in PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If using Command Prompt instead:

   ```bat
   venv\Scripts\activate.bat
   ```

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   python app.py
   ```

5. Open this address in your browser:

   http://127.0.0.1:5000

The `finance.db` SQLite database is created automatically on first launch.

## Project structure

```text
FinTrack_AI/
├── app.py
├── ml_recommendation.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── report.html
└── static/
    └── css/
        └── style.css
```

## How the recommendation works

`ml_recommendation.py` trains a small Scikit-learn Linear Regression model on demonstration values and predicts a suggested budget from the current month's spending total. The application also checks the highest spending category and generates basic tips.

This is a learning demonstration, not a production-grade financial prediction system. For a stronger academic evaluation, collect suitable anonymized monthly expense data and explain the limitations of the small sample dataset.

## Notes

- The dashboard shows expenses for the current calendar month.
- This starter version has no login or multi-user accounts.
- Do not use real sensitive financial data in a classroom demo.
- Debug mode is enabled for local development only. Turn it off before any public deployment.
