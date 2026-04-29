# User Behavior and Cohort Retention Analysis

This project analyzes customer retention using cohort analysis on transaction-level e-commerce data.

The goal is to understand how user activity changes after the first purchase and turn retention patterns into product and CRM recommendations.

## Business Problem

A product or CRM team needs to understand whether new customers continue purchasing after their first order.

The key questions:

1. How many users return after the first purchase?
2. At which cohort age does retention drop the most?
3. Which cohorts show stronger or weaker long-term behavior?
4. Where should retention actions focus first?

## Dataset

Dataset: transaction-level e-commerce data.

Main fields used:

| Field | Description |
|---|---|
| CustomerID | Unique customer identifier |
| InvoiceDate | Transaction date |
| InvoiceNo | Transaction identifier |
| Quantity | Number of purchased items |
| UnitPrice | Item price |

## Methodology

The analysis follows this workflow:

1. Load transaction data.
2. Clean missing customer identifiers and invalid records.
3. Define each user's first purchase month.
4. Assign every transaction to a cohort month.
5. Calculate cohort age in months.
6. Count active users by cohort and cohort age.
7. Convert active user counts into retention rates.
8. Visualize the retention matrix as a heatmap.
9. Translate retention patterns into business recommendations.

## Metrics

Cohort size:

```text
cohort_size = number of unique users in the first cohort month
```

Retained users:

```text
retained_users = number of unique users active in a later cohort month
```

Retention rate:

```text
retention_rate = retained_users / cohort_size
```

## Visualization

![Retention Heatmap](screenshots/retention_heatmap.png)

## Key Findings

1. Early retention is the main weak point.
   Month 2 retention drops to roughly 20-40% across cohorts.

2. Retention stabilizes after the first decline.
   Several cohorts hold around 15-30% retention during months 3-6.

3. Some cohorts show temporary retention spikes.
   These spikes may indicate campaign effects, seasonality, or stronger acquisition quality.

4. Older cohorts decline over time.
   Early cohorts fall below 10% by later cohort ages.

## Business Recommendations

1. Focus first on the first 30 days after the first purchase.
   This is where the largest drop happens.

2. Build a second-purchase trigger.
   Users who do not return within the first month should enter a reactivation flow.

3. Compare strong and weak cohorts.
   Look for differences in acquisition source, discount use, country, product category, or onboarding path.

4. Measure retention by segment.
   Overall retention hides important differences between user groups.

5. Track cohort quality over time.
   Newer cohorts should be compared with older cohorts at the same age, not by calendar month only.

## Limitations

- The dataset does not include acquisition source, device type, marketing campaign, or user channel.
- The analysis measures purchase activity only.
- Revenue retention and frequency retention are not included in the current version.
- Cohort spikes are interpreted as signals, not as confirmed campaign effects.
- Seasonality is not isolated from product or marketing changes.

## Next Steps

Planned improvements:

- add revenue retention,
- add average order value by cohort age,
- add cohort comparison by country or product category,
- add SQL version of the cohort calculation,
- build a Tableau dashboard with cohort filters.

## Tools

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
