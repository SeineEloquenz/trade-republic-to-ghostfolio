#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
import csv
import json
from collections import Counter, OrderedDict

# Load the source CSV file
input_file = "transactions.csv"
output_file = "ghostfolio_transactions.csv"
account_name = "Trade Republic"
json_output_file = "profiles.json"
df = pd.read_csv(input_file)

def parse_date(timestamp):
    return datetime.strptime(timestamp, "%d %b %y %H:%M %z")

# Function to format the date
def format_date(dt):
    return dt.strftime("%Y-%m-%d")

with open("ignored_symbols.json", "r") as f:
  ignored_symbols = json.load(f)

# Transform the DataFrame
ghostfolio_data = []
instruments_data = OrderedDict()  # Use OrderedDict to maintain insertion order

for index, row in df.iterrows():
    transaction_type = row["Type"].lower()

    if transaction_type in ["purchase", "saveback", "round up"]:
        action = "Buy"
    elif transaction_type == "dividends":
        action = "Dividend"
    else:
        continue  # Skip transactions that don't match the specified types

    dt = parse_date(row["Timestamp"])

    date = format_date(dt)
    shares = row["Shares"]
    price = row["Rate"]
    fee = row["Commission"]
    symbol = row["Instrument"]
    name = row["Name"]

    if symbol in ignored_symbols:
        continue

    ghostfolio_data.append({
        "Date": date,
        "Code": symbol,
        "Action": action,
        "Name": name,
        "Currency": "EUR",
        "DataSource": "MANUAL",
        "Price": price,
        "Quantity": shares,
        "Fee": fee,
        "Account": account_name,
        "Comment": "TR"
    })

    # Add unique instruments to the OrderedDict
    if symbol not in instruments_data:
        instruments_data[symbol] = {
            "symbol": symbol,
            "profile_data": {
                "assetClass": "EQUITY",
                "assetSubClass": "ETF" if symbol.startswith("IE") else "STOCK",
                "comment": "",
                "currency": "EUR",
                "name": name,
                "scraperConfiguration": {
                    "url": f"https://api.boerse-frankfurt.de/v1/data/quote_box/single?isin={symbol}&mic=XETR",
                    "selector": "$.lastPrice"
                },
                "symbolMapping": {}
            },
            "data_source": {
                "name": "boerse_frankfurt",
                "ticker": f"XETR:{symbol}",
                "start_date": "2021-01-01"
            },
        }

# Save the transformed data to CSV
fieldnames = ["Date", "Code", "Name", "Action", "Currency", "Price", "Quantity", "Fee", "DataSource", "Account", "Comment"]
with open(output_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(ghostfolio_data)

# Save the instrument data to JSON (now with unique instruments)
with open(json_output_file, "w") as json_file:
    json.dump(list(instruments_data.values()), json_file, indent=4)

# Generate statistics
if ghostfolio_data:
    num_transactions = len(ghostfolio_data)
    dates = [entry["Date"] for entry in ghostfolio_data]
    first_date = min(dates)
    last_date = max(dates)
    instruments_counter = Counter((entry["Code"], entry["Name"]) for entry in ghostfolio_data)

    print("\n--- Summary Statistics ---")
    print(f"Number of transactions exported: {num_transactions}")
    print(f"First transaction date: {first_date}")
    print(f"Last transaction date: {last_date}")

    print("\nInstrument Summary:")
    print(f"{'Instrument Code':<20}{'Name':<40}{'Occurrences':<10}")
    print("-" * 70)
    for (code, name), count in instruments_counter.items():
        print(f"{code:<20}{name:<40}{count:<10}")
else:
    print("No transactions were exported.")

print(f"\nFile successfully converted: {output_file}")
print(f"Instrument data saved to: {json_output_file}")
