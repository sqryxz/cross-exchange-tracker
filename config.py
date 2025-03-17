#!/usr/bin/env python3

"""
Configuration settings for the price discrepancy finder.
Edit this file to customize the behavior of the tool.
"""

# Cryptocurrency to track
SYMBOL = "XRP"

# Base currency for comparison
BASE_CURRENCY = "USDT"

# Minimum price difference percentage to log as a potential arbitrage opportunity
THRESHOLD_PERCENT = 1.0

# Time between price checks in seconds
CHECK_INTERVAL = 60

# Logging settings
LOG_FILE = "arbitrage.log"
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Exchange-specific settings
# Set to True to enable the exchange, False to disable
EXCHANGES = {
    "binance": True,
    "kraken": True,
    "coingecko": True
}

# Alert settings
# Cooldown period between alerts in seconds (to avoid alert spam)
ALERT_COOLDOWN = 300  # 5 minutes

# Enable different alert channels
ENABLE_EMAIL_ALERTS = True
ENABLE_SMS_ALERTS = False
ENABLE_WEBHOOK_ALERTS = False

# Email alert settings (only used if ENABLE_EMAIL_ALERTS is True)
EMAIL_FROM = "zjoy11@gmail.com"
EMAIL_TO = "zjoy11@gmail.com"
EMAIL_SUBJECT_PREFIX = "[PRICE ALERT]"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "zjoy11@gmail.com"
SMTP_PASSWORD = ""  # You'll need to set this to your App Password
SMTP_USE_TLS = True

# SMS alert settings (only used if ENABLE_SMS_ALERTS is True)
# These would be used with a service like Twilio
SMS_TO_NUMBER = "+1234567890"
SMS_FROM_NUMBER = "+1987654321"
SMS_API_KEY = "your-api-key"
SMS_API_SECRET = "your-api-secret"

# Webhook alert settings (only used if ENABLE_WEBHOOK_ALERTS is True)
# For Discord webhooks, use your Discord webhook URL (e.g., https://discord.com/api/webhooks/...)
# The code will automatically detect Discord URLs and format the message appropriately
WEBHOOK_URL = "https://example.com/webhook"
WEBHOOK_METHOD = "POST"  # GET or POST
WEBHOOK_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-token"
}

# Advanced settings
# Maximum number of consecutive errors before pausing
MAX_ERRORS = 5

# Pause duration in seconds after reaching MAX_ERRORS
ERROR_PAUSE_DURATION = 300  # 5 minutes 