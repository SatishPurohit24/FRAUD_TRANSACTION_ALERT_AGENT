# FraudGuard — Viva Presentation Guide

## 1. Project Overview & Elevator Pitches

### 30-Second Pitch
"FraudGuard is a full-stack, data-driven Agentic AI fraud detection system. It combines historical behavioral feature engineering, a Random Forest machine learning classifier, and deterministic risk rules to evaluate transactions in real-time. Finally, it uses a Large Language Model (Gemini) acting as a risk agent to synthesise these signals into clear, actionable, human-readable explanations for fraud analysts."

### 1-Minute Pitch
"FraudGuard goes beyond traditional machine learning by implementing a complete transaction monitoring pipeline. When a transaction is submitted, the system first computes time-windowed behavioral features (like velocity and historical averages) from a real dataset without leaking future data. It then scores the transaction using an ML model and evaluates it against deterministic business rules (like high amounts or night-time activity). Instead of just returning a risk score, FraudGuard employs an Agentic AI layer using Gemini to analyze the signals and generate a contextual explanation and recommendation. This creates an end-to-end prototype of how modern financial institutions combine ML, rules, and GenAI to empower human analysts."

---

## 2. Architecture & Tech Stack

- **Frontend**: Vanilla HTML/JS/CSS. A thin, responsive UI layer focusing on clear data presentation. Contains no business logic and no API keys.
- **Backend Orchestrator**: Python (Flask). Manages the API endpoints, orchestrates the analysis pipeline, and serves the static frontend.
- **Data Layer**: SQLite (`analysis_results`). Stores all analyzed transactions and their explanations for dashboard aggregation.
- **Machine Learning**: `scikit-learn` Random Forest Classifier, trained on the Fraud Detection Handbook dataset.
- **Agentic AI Layer**: `google-genai` SDK. Leverages Gemini to synthesize the raw ML probabilities and triggered rules into human-readable text.

---

## 3. The Analysis Pipeline (End-to-End Flow)

When an analyst clicks "Analyze Transaction", the following sequence occurs entirely on the backend:

1.  **Input Reception**: The backend receives basic transaction details (ID, Customer, Terminal, Amount, Timestamp).
2.  **Dynamic Feature Engineering**: `feature_engineering.py` computes 19 behavioral features based on the `HISTORY_DF` (the pre-loaded dataset). 
3.  **Machine Learning Inference**: The computed features are passed to the pre-trained Random Forest model (`model.joblib`), which returns a raw fraud probability.
4.  **Rule Evaluation**: The transaction is evaluated against 4 deterministic business rules (High Amount Deviation, Velocity, Night-time, Terminal Risk).
5.  **Risk Scoring**: The ML probability and rule scores are combined into a final Risk Score (0-100) and categorized (LOW, MEDIUM, HIGH, CRITICAL).
6.  **Agentic Synthesis**: The `FraudAlertAgent` sends the raw data, ML probability, and triggered rules to the Gemini API. Gemini acts as an expert analyst and generates a natural language explanation and recommendation.
7.  **Persistence & Return**: The full analysis is saved to SQLite and returned to the frontend for display.

---

## 4. Addressing Data Leakage

A critical concept in financial ML is preventing **Data Leakage** (using data from the future to predict the past). 

FraudGuard strictly prevents leakage during dynamic feature engineering:
- In `feature_engineering.py`, when aggregating customer or terminal history, the system explicitly enforces: `hist["TX_DATETIME"] < dt`.
- The `cutoff` logic ensures that only transactions occurring *strictly before* the timestamp of the current transaction are used to calculate velocities and moving averages. Future transactions in the dataset are completely hidden from the computation.

---

## 5. Dataset Information

The project uses a subset of the **Fraud Detection Handbook** dataset (simulated transactions).
- The dataset is loaded dynamically into the backend at startup as `HISTORY_DF`.
- The dashboard now pulls actual metrics (Total Transactions, Fraud Percentage, Date Range) directly from this DataFrame.
- Demo Scenarios on the "Analyze" page are randomly sampled from the live dataset, mixing normal and fraudulent transactions to provide realistic test cases.

---

## 6. Important Notes for the Viva Demonstration

- **No Hardcoded Data**: Reiterate to the examiner that the dashboard statistics and demo scenarios are driven by the actual dataset and SQLite history, not hardcoded placeholders.
- **API Rate Limits**: If Gemini fails due to quota limits (`429 Resource Exhausted`), the `FraudAlertAgent` will automatically gracefully degrade and fall back to a deterministic explanation. This proves system resilience.
- **Security**: The Gemini API key is securely stored in `.env` and is strictly loaded by the backend. It is completely invisible to the frontend client.

---

### End of Guide
*Good luck with your CA3 Viva Demonstration!*
