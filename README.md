# Cross-Exchange Price Discrepancy Finder

A Python tool that tracks a single altcoin's price on Binance and Kraken exchanges, identifies any notable price gaps, and logs potential arbitrage signals.

## Features

- Real-time price monitoring on Binance and Kraken exchanges
- Configurable price difference threshold for arbitrage opportunities
- Detailed logging of price discrepancies and potential arbitrage opportunities
- Customizable cryptocurrency pairs and check intervals
- Command-line interface for easy configuration
- Interactive menu to select from popular cryptocurrency pairs
- Automated alerts for price discrepancies exceeding 1%
  - Email alerts via SMTP
  - SMS alerts via Twilio
  - Webhook alerts for integration with Slack, Discord, or custom applications

## Requirements

- Python 3.6+
- API keys for Binance and Kraken (for private endpoints)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cross-exchange-tracker.git
   cd cross-exchange-tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with your API keys:
   ```
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_API_SECRET=your_binance_secret_key
   
   KRAKEN_API_KEY=your_kraken_api_key
   KRAKEN_API_SECRET=your_kraken_secret_key
   ```

## Usage

### Interactive Coin Selector (Recommended)

The easiest way to use the tool is with the interactive coin selector:

```
python3 coin_selector.py
```

This will display a menu of popular cryptocurrency pairs to track. You can:
- Select from popular altcoin pairs
- Select from stablecoin pairs
- Enter a custom pair
- Set your desired threshold percentage
- Set your preferred check interval

### Basic Usage

```
# Track Bitcoin/USDT with default settings
python3 run.py -s BTC -b USDT

# Track Ethereum/USD with a 2% threshold
python3 run.py -s ETH -b USD -t 2.0

# Track Solana/USDT with a 30-second check interval
python3 run.py -s SOL -b USDT -i 30

# Track Ethereum with Kraken disabled
python3 run.py -s ETH -b USDT --disable-kraken

# Track Bitcoin with verbose logging
python3 run.py -s BTC -b USDT -l DEBUG
```

### Using the Command-Line Interface

The tool provides a flexible command-line interface:

```
python3 run.py [-h] [-s SYMBOL] [-b BASE] [-t THRESHOLD] [-i INTERVAL]
               [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
               [--disable-binance] [--disable-kraken]
```

Options:
```
-h, --help            Show this help message and exit
-s SYMBOL, --symbol SYMBOL
                      Cryptocurrency symbol to track (e.g., BTC, ETH, SOL)
-b BASE, --base BASE  Base currency for comparison (e.g., USDT, USD, EUR)
-t THRESHOLD, --threshold THRESHOLD
                      Minimum price difference percentage to log as a potential
                      arbitrage opportunity
-i INTERVAL, --interval INTERVAL
                      Time between price checks in seconds
-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                      Set the logging level
--disable-binance     Disable Binance exchange
--disable-kraken      Disable Kraken exchange
```

Examples:

```
# Track Bitcoin with a 2% threshold, checking every 30 seconds
python3 run.py -s BTC -t 2.0 -i 30

# Track Solana against USD with debug logging
python3 run.py -s SOL -b USD -l DEBUG
```

### Configuration File

You can also customize the default settings by editing the `config.py` file:

```python
# Cryptocurrency to track
SYMBOL = "ETH"

# Base currency for comparison
BASE_CURRENCY = "USDT"

# Minimum price difference percentage to log as a potential arbitrage opportunity
THRESHOLD_PERCENT = 1.0

# Time between price checks in seconds
CHECK_INTERVAL = 60

# Alert settings
ALERT_COOLDOWN = 300  # 5 minutes between alerts to avoid spam
ENABLE_EMAIL_ALERTS = False  # Set to True to enable email alerts
ENABLE_SMS_ALERTS = False    # Set to True to enable SMS alerts
ENABLE_WEBHOOK_ALERTS = False  # Set to True to enable webhook alerts
```

## Alerts

The tool can send alerts when price discrepancies exceed 1%. To enable alerts:

1. Edit the `config.py` file and set the desired alert channels to `True`:
   ```python
   ENABLE_EMAIL_ALERTS = True
   ENABLE_SMS_ALERTS = True
   ENABLE_WEBHOOK_ALERTS = True
   ```

2. Configure the alert settings for your chosen channels:

   ### Email Alerts
   ```python
   EMAIL_FROM = "alerts@example.com"
   EMAIL_TO = "your-email@example.com"
   EMAIL_SUBJECT_PREFIX = "[PRICE ALERT]"
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   SMTP_USERNAME = "your-username"
   SMTP_PASSWORD = "your-password"
   SMTP_USE_TLS = True
   ```

   ### SMS Alerts (via Twilio)
   ```python
   SMS_TO_NUMBER = "+1234567890"
   SMS_FROM_NUMBER = "+1987654321"
   SMS_API_KEY = "your-twilio-api-key"
   SMS_API_SECRET = "your-twilio-api-secret"
   ```

   ### Webhook Alerts
   ```python
   WEBHOOK_URL = "https://hooks.slack.com/services/your-webhook-url"
   WEBHOOK_METHOD = "POST"  # GET or POST
   WEBHOOK_HEADERS = {
       "Content-Type": "application/json"
   }
   ```

3. For SMS alerts, install the Twilio package:
   ```
   pip install twilio
   ```

## Logs

The tool logs information to both the console and an `arbitrage.log` file, including:
- Current prices on both exchanges
- Price differences
- Potential arbitrage opportunities

## Disclaimer

This tool is for educational purposes only. It does not account for:
- Trading fees
- Withdrawal/deposit fees
- Slippage
- Transfer times between exchanges
- Market depth/liquidity

Always conduct your own research and risk assessment before engaging in any trading activities.

## License

MIT 