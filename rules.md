# FraudGuard Deterministic Rules

The rule engine operates alongside the Machine Learning model to evaluate 5 distinct classical banking rules. The scores from these rules make up 50% of the final risk score. The maximum rule score is 70 points, which is mathematically normalized to a percentage.

## R01 — High Amount Deviation
- **Purpose**: Detects transactions that are significantly larger than what the customer usually spends.
- **Logic**: Compares the current transaction amount with the customer's 30-day historical average.
- **Threshold**: Amount > 3.0 × (30-day customer average).
- **Points**: 20
- **Example**: If a user usually spends $50 on average, a $200 transaction (4.0x) will trigger this rule.
- **Why it helps**: Protects against sudden account takeovers draining funds in large chunks.
- **Limitations**: Fails if the user is making a rare but legitimate large purchase (e.g., buying a laptop or car).

## R02 — High Transaction Velocity
- **Purpose**: Detects rapid-fire transactions indicative of stolen card testing or automated skimming.
- **Logic**: Counts the number of transactions by the same customer in the past 1 hour.
- **Threshold**: > 3 transactions in 1 hour.
- **Points**: 15
- **Example**: A user makes 4 separate $10 purchases online within 30 minutes.
- **Why it helps**: Fraudsters often test stolen details with multiple small transactions to see if the card is active.
- **Limitations**: Can be triggered legitimately if a user is checking out of multiple online stores quickly.

## R03 — Unusual Night Transaction
- **Purpose**: Detects anomalous behavior occurring during atypical hours for the user's timezone.
- **Logic**: Checks if the transaction's hour falls within a configured late-night window.
- **Threshold**: Hour between 02:00 and 05:00 (inclusive).
- **Points**: 10
- **Example**: A transaction processed at 03:45.
- **Why it helps**: Physical and localized digital fraud often occurs when the victim is asleep to delay detection.
- **Limitations**: Will flag legitimate night-shift workers or international travelers.

## R04 — Terminal Historical Risk
- **Purpose**: Protects against merchants, ATMs, or digital gateways with a proven history of compromised transactions.
- **Logic**: Calculates the historical fraud percentage for the given terminal over the past 30 days.
- **Threshold**: > 5.0% historical fraud rate.
- **Points**: 15
- **Example**: A terminal processed 100 transactions in the last month, and 7 were confirmed fraud (7.0%).
- **Why it helps**: Skimmers and compromised web terminals concentrate fraud risk in specific IDs.
- **Limitations**: A small terminal with very few transactions may falsely trip this threshold if a single fraud case occurs.

## R05 — Customer Behavioural Anomaly
- **Purpose**: Uses statistical variance to understand not just average spend, but the usual *fluctuation* of the customer's spending habits.
- **Logic**: Computes the z-score of the transaction based on the customer's 30-day mean and standard deviation.
- **Threshold**: Amount > 3.0 Standard Deviations above the mean.
- **Points**: 10
- **Example**: Mean = $100, Std Dev = $20. A $170 transaction is 3.5σ above the mean.
- **Why it helps**: More robust than simple averages. It understands that some users have highly variable spending (high std dev) while others are rigid (low std dev).
- **Limitations**: Requires enough transaction history to form a mathematically sound standard deviation.
