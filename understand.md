# FraudGuard System — Implementation Summary

This document explains exactly what has been built for the FraudGuard CA3 project during this session. We have transformed the frontend prototype into a fully functional, end-to-end fraud detection system using real data.

## 1. Data Engineering & Model Training
*   **Real Dataset Integration:** We downloaded the "Fraud Detection Handbook" dataset (`.pkl` files) representing real-world synthetic transaction data. We parsed ~550,000 rows.
*   **Feature Engineering (`feature_engineering.py`):** We utilized the pre-computed behavioral features from the dataset (e.g., customer transaction count in last 1/7/30 days, terminal risk rates). We mapped these to 19 standard ML features. *Crucially, we ensured zero data leakage* (features are strictly computed from past data).
*   **Machine Learning Model (`train_model.py`):** We trained a `RandomForestClassifier` on a chronological subset of 300,000 transactions (80/20 train/test split). 
*   **Performance:** The model achieved ~98.7% accuracy, 83.7% ROC-AUC, and a ~60% recall rate (catching 60% of fraud in a highly imbalanced dataset with ~1% fraud rate). The model and its metrics were saved as `model.joblib` and `metrics.json`.

## 2. Rule Engine & Risk Scoring
*   **Transparent Rules (`rule_engine.py`):** We built 5 distinct business rules that fire based on transaction context:
    1.  **High Amount Deviation:** Transaction amount > 3x the customer's 30-day average.
    2.  **High Transaction Velocity:** More than 3 transactions in the last hour.
    3.  **Unusual Night Transaction:** Transaction occurs between 02:00 and 05:00.
    4.  **Terminal Historical Risk:** Terminal fraud rate > 5%.
    5.  **Customer Behavioural Anomaly:** Amount > customer's historical mean + 3 standard deviations.
*   **Risk Engine (`risk_engine.py`):** Combines the ML probability (50% weight) and the Rule Engine score (50% weight) to produce a final 0-100 Risk Score. The risk is bucketed into `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.

## 3. Fraud Alert Agent
*   **Decision Layer (`fraud_agent.py`):** We created a pure Python orchestration class (not an LLM) that acts as the "Agent". It takes the combined risk score and makes an actionable decision (`ALLOW`, `MONITOR`, `REVIEW`, `ESCALATE`) along with human-readable explanations.

## 4. Backend (Flask API & Database)
*   **Flask Server (`app.py`):** We built a Python Flask server running on port 5050. It exposes several endpoints:
    *   `GET /api/health`: System status.
    *   `POST /api/analyze`: Main endpoint taking transaction JSON, running the full ML/Rule pipeline, and returning the agent decision.
    *   `GET /api/demo-transactions`: Serves the curated demo scenarios dynamically.
    *   `GET /api/overview` & `GET /api/transactions`: Fetches stats and history from the database.
*   **Database (`database.py`):** We implemented a local SQLite database (`database/fraudguard.db`) to persist every transaction analyzed, the risk scores, the rules triggered, and the agent's decision.
*   **Bug Fixes:** We resolved issues with timezone-aware datetimes (`utcnow()` deprecation) and `scikit-learn` feature name warnings by converting input vectors to Pandas DataFrames.

## 5. Frontend Integration
*   **UI Updates:** We updated the `app.js` and `index.html` to point to `http://localhost:5050/api`.
*   **Demo Scenarios:** We curated 5 specific transactions from the dataset (`models/demo_transactions.json`) to serve as viva demonstration scenarios. These include:
    *   Scenario 1 (Normal): A totally legitimate, low-risk transaction.
    *   Scenario 2 (High Amount): A high-amount fraud transaction.
    *   Scenario 5 (Multi-Signal): A transaction that triggers 4 rules simultaneously (night-time, high amount, anomaly) yielding a HIGH risk score.

## Summary of the Flow
When you click **"Analyze Transaction"** in the UI:
1. The frontend sends the raw transaction to `/api/analyze`.
2. The backend looks up the customer and terminal history from the loaded dataset.
3. It computes the 19 features.
4. The Random Forest model generates a fraud probability.
5. The Rule Engine checks the 5 rules.
6. The Risk Engine calculates the 0-100 score.
7. The FraudAlertAgent formats the final recommendation.
8. The transaction is saved to the SQLite database.
9. The frontend displays the rich result panel.
