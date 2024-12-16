# Trade Republic to Ghostfolio Transaction Converter

## Description

This Python script converts Trade Republic transaction exports into a format compatible with Ghostfolio, an open-source investment tracking application.

## Prerequisites

- Python 3
- Python Libraries:
  - `pandas`
  - `datetime`
  - `csv`
  - `json`
  - `collections`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/taclab/trade-republic-to-ghostfolio.git
cd trade-republic-to-ghostfolio
```

2. Install dependencies:
```bash
pip install pandas
```

## Complete Workflow

This script integrates into a comprehensive data import workflow:

1. **Transaction Download** 
   - Use [traderepublic-portfolio-downloader](https://github.com/dhojayev/traderepublic-portfolio-downloader) to export your Trade Republic transactions

2. **Transaction Conversion** 
   - Use this script to convert transactions to Ghostfolio format

3. **Market Data Feeding**
   - Use [ghostfolio-feeder](https://github.com/marco-ragusa/ghostfolio-feeder) to import market data

## Usage

1. Place your exported Trade Republic CSV file (`traderepublic_transactions.csv`) in the same directory as the script

2. Run the script:
```bash
python trade_republic_converter.py
```

3. The script will generate two files:
   - `ghostfolio_transactions.csv`: Transactions in Ghostfolio format
   - `instruments_data.json`: Unique instrument data for [ghostfolio-feeder](https://github.com/marco-ragusa/ghostfolio-feeder)

## Features

- Converts buy and dividend transactions
- Generates transaction statistics
- Adds metadata for Ghostfolio scraper configuration


## Limitations

- Currently supports buy and dividend transactions
- Uses a generic scraper configuration for Börse Frankfurt
- Requires post-processing for specific configurations

## Acknowledgments

- [traderepublic-portfolio-downloader](https://github.com/dhojayev/traderepublic-portfolio-downloader)
- [ghostfolio-feeder](https://github.com/marco-ragusa/ghostfolio-feeder)
- [Ghostfolio](https://github.com/ghostfolio/ghostfolio)

## Disclaimer

This script is provided as-is, without warranty. Always verify your imported transactions.