import pandas as pd

# ----------------------------
# 1️⃣ Create or load your tracker file
# ----------------------------
try:
    df = pd.read_csv("predictions_tracker.csv")
    print("Loaded existing tracker file.")
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "Date", "League", "Match", "Your_Pick", "Result", "Odds", "Outcome", "Profit"
    ])
    print("New tracker created.")

# ----------------------------
# 2️⃣ Add a new prediction
# ----------------------------
def add_prediction(date, league, match, your_pick, result, odds, outcome):
    """
    outcome = 'win', 'lose', or 'push' (for refund)
    result = actual final score, e.g., '2-1'
    odds = decimal odds (e.g., 1.95)
    """
    if outcome.lower() == 'win':
        profit = (odds - 1) * 100  # assuming ₦100 stake
    elif outcome.lower() == 'lose':
        profit = -100
    else:
        profit = 0  # refund

    new_row = {
        "Date": date,
        "League": league,
        "Match": match,
        "Your_Pick": your_pick,
        "Result": result,
        "Odds": odds,
        "Outcome": outcome,
        "Profit": profit
    }

    global df
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("predictions_tracker.csv", index=False)
    print(f"Added: {match} ({outcome.upper()})")

# ----------------------------
# 3️⃣ Generate performance summary
# ----------------------------
def summary():
    total_bets = len(df)
    wins = len(df[df['Outcome'].str.lower() == 'win'])
    losses = len(df[df['Outcome'].str.lower() == 'lose'])
    pushes = len(df[df['Outcome'].str.lower() == 'push'])
    total_profit = df['Profit'].sum()
    roi = (total_profit / (total_bets * 100)) * 100 if total_bets > 0 else 0

    print("\n📊 --- Betting Tracker Summary ---")
    print(f"Total Bets: {total_bets}")
    print(f"Wins: {wins} | Losses: {losses} | Pushes: {pushes}")
    print(f"Win Rate: {wins / total_bets * 100:.2f}%")
    print(f"Total Profit: ₦{total_profit:.2f}")
    print(f"ROI: {roi:.2f}%")

# ----------------------------
# Example Usage
# ----------------------------
# add_prediction("2025-10-18", "Serie A", "Torino vs Napoli", "Napoli to Win", "1-2", 1.70, "win")
# add_prediction("2025-10-18", "La Liga", "Barcelona vs Girona", "BTTS Yes", "2-1", 1.80, "win")

# summary()