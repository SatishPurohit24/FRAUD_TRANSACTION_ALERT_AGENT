# FraudGuard — Fraud Transaction Alert Agent
**Academic Prototype | CA3 University Project**

> ⚠️ This is an educational prototype built for academic demonstration purposes.
> It does NOT represent a production banking system, real customer data, or actual fraud detection infrastructure.

---

## Project Overview

FraudGuard is a fraud transaction analysis prototype designed for a Fraud/Risk Analyst.
A transaction is submitted to the system; it is analyzed using historical behavioral features,
a machine-learning model, a transparent rule engine, and a FraudAlertAgent decision layer.
The system produces a risk score, triggered rule explanations, and an actionable recommendation.

---

## Architecture

```
Raw Transaction Input
        ↓
Feature Engineering (19 behavioral features)
        ↓
ML Model (Random Forest)   +   Rule Engine (5 rules)
        ↓                          ↓
           Risk Fusion (0-100 score)
                    ↓
             FraudAlertAgent
                    ↓
          Recommendation / Alert
                    ↓
              SQLite Persistence
                    ↓
            Frontend Dashboard
```

See [architecture.md](architecture.md) for more details.

---

## Dataset

**Source:** Fraud Detection Handbook (simulated-data-transformed)  
**Format:** .pkl files (one per day), pre-computed historical features  
**Size used:** 300,000 transactions (chronological subset)  
**Fraud rate:** ~0.75% train, ~1.03% test  
**Actual columns:**
- `TRANSACTION_ID`, `TX_DATETIME`, `CUSTOMER_ID`, `TERMINAL_ID`, `TX_AMOUNT`, `TX_FRAUD`
- Pre-computed stats like `CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW`.

See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for a detailed breakdown.

---

## ML Model

- **Algorithm:** RandomForestClassifier (scikit-learn)
- **Split:** Chronological 80/20 (no shuffle — prevents temporal leakage)

---

## Rule Engine

Five transparent rules. All use ONLY historical data prior to the transaction.

| Rule | Trigger | Points |
|---|---|---|
| R01 — High Amount Deviation | Amount > 3x customer 30-day average | 20 |
| R02 — High Transaction Velocity | >3 transactions from customer within 60 min | 15 |
| R03 — Unusual Night Transaction | Transaction at 02:00–05:00 | 10 |
| R04 — Terminal Historical Risk | Terminal fraud rate > 5% | 15 |
| R05 — Customer Behavioural Anomaly | Amount > mean + 3σ of customer history | 10 |

Max raw rule score: 70. Normalized to 0-1 for risk fusion. See [rules.md](rules.md) for detailed explanations.

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory (do NOT commit this file to GitHub) and add your Gemini API Key:
```env
GEMINI_API_KEY="your_api_key_here"
```

### 3. Download Dataset
```bash
python3 backend/download_data.py
```

### 4. Train Model
```bash
python3 backend/train_model.py
```
This generates the `.joblib` model and demo scenarios.

### 5. Start Backend
```bash
python3 backend/app.py
```
Backend runs at: http://localhost:5050

### 6. Open Frontend
Open `frontend/index.html` in a browser.

---

## Testing
Run the Pytest suite to verify the rule engine, database constraint handling, and ML agent functionality:
```bash
python3 -m pytest tests/test_backend.py -v
```

---

## Deployment Note
This prototype uses SQLite and in-memory Pandas dataframes. To deploy to a serverless environment (e.g. Heroku, Vercel), you must migrate the database to a persistent relational database (e.g., PostgreSQL) and potentially serve the historical dataset via a Feature Store (like Redis).
