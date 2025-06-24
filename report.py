import pandas as pd


# Total spend data
total_spent_data = {
    "Player":       ["AM", "AS", "MC", "PK", "Raj", "SG", "SDG", "Vaibhav"],
    "Amount Spent": [13400.10, 3083.71, 5670.00, 6300.72, 16788.68, 3769.48, 4048.64, 2017.63]
}

# F&B spend
fnb_data = {
    "Player":       ["AM", "MC", "PK", "Raj", "SG", "SDG", "Vaibhav"],
    "F&B Spent":    [1609.17, 462.86, 1241.92, 2691.35, 77.50, 1337.43, 85.00]
}

# Court + Shuttle spend
court_shuttle_data = {
    "Player":               ["AM", "AS", "MC", "PK", "Raj", "SG", "SDG", "Vaibhav"],
    "Court+Shuttle Spent":  [11790.93, 3083.71, 5207.14, 5058.80, 14097.33, 3691.98, 2711.21, 1932.63]
}

# === DataFrame Operations ===

# Create DataFrames
df_total = pd.DataFrame(total_spent_data)
df_fnb = pd.DataFrame(fnb_data)
df_court = pd.DataFrame(court_shuttle_data)

# Merge all into one DataFrame
df_combined = pd.merge(df_total, df_fnb, on="Player", how="left")
df_combined = pd.merge(df_combined, df_court, on="Player", how="left")
df_combined.fillna(0, inplace=True)

# Calculate percentages
df_combined["% F&B"] = (df_combined["F&B Spent"] / df_combined["Amount Spent"] * 100).round(2)
df_combined["% Court+Shuttle"] = (df_combined["Court+Shuttle Spent"] / df_combined["Amount Spent"] * 100).round(2)

# === Consistency Check ===
df_combined["Mismatch"] = (df_combined["F&B Spent"] + df_combined["Court+Shuttle Spent"] - df_combined["Amount Spent"]).round(2)
df_combined["Is Mismatch?"] = df_combined["Mismatch"].abs() > 0.01

# === Optional: Format Numbers ===
formatted_df = df_combined.copy()
for col in ["Amount Spent", "F&B Spent", "Court+Shuttle Spent", "% F&B", "% Court+Shuttle", "Mismatch"]:
    formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

# === Display Results ===
print("\n=== Full Expense Breakdown by Player ===\n")
print(formatted_df.to_string(index=False))

# === Show Only Mismatches ===
if df_combined["Is Mismatch?"].any():
    print("\nWARNING: The following players have mismatches in total vs component spends:\n")
    print(formatted_df[df_combined["Is Mismatch?"]].to_string(index=False))
else:
    print("\n All totals match their F&B + Court+Shuttle spends.")

# === Save to CSV ===
df_combined.drop(columns=["Is Mismatch?"], inplace=True)
df_combined.to_csv("badminton_expense_breakdown.csv", index=False)
print("\nSaved as 'badminton_expense_breakdown.csv'")
