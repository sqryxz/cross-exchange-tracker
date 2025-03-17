#!/usr/bin/env python3

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests
from binance.client import Client as BinanceClient
import krakenex
from pycoingecko import CoinGeckoAPI
from kraken_utils import get_kraken_asset_pair, get_kraken_ticker_info
from coingecko_utils import get_coingecko_coin_id, get_coingecko_currency, parse_coingecko_price_data
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class PriceDiscrepancyFinder:
    def __init__(self, symbol=config.SYMBOL, base_currency=config.BASE_CURRENCY, threshold_percent=config.THRESHOLD_PERCENT):
        """
        Initialize the price discrepancy finder.
        
        Args:
            symbol (str): The cryptocurrency symbol to track
            base_currency (str): The base currency for comparison
            threshold_percent (float): The minimum price difference percentage to log as a potential arbitrage opportunity
        """
        self.symbol = symbol
        self.base_currency = base_currency
        self.threshold_percent = threshold_percent
        self.binance_pair = f"{symbol}{base_currency}"
        self.kraken_pair = get_kraken_asset_pair(symbol, base_currency)
        
        # Error tracking
        self.consecutive_errors = 0
        
        # Initialize exchange clients
        if config.EXCHANGES["binance"]:
            try:
                self.binance_client = BinanceClient(
                    os.getenv('BINANCE_API_KEY'),
                    os.getenv('BINANCE_API_SECRET')
                )
                logger.info("Binance client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing Binance client: {e}")
                self.binance_client = None
                config.EXCHANGES["binance"] = False
        else:
            self.binance_client = None
            
        if config.EXCHANGES["kraken"]:
            try:
                self.kraken_client = krakenex.API(
                    key=os.getenv('KRAKEN_API_KEY'),
                    secret=os.getenv('KRAKEN_API_SECRET')
                )
                logger.info("Kraken client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing Kraken client: {e}")
                self.kraken_client = None
                config.EXCHANGES["kraken"] = False
        else:
            self.kraken_client = None
            
        if config.EXCHANGES["coingecko"]:
            try:
                # Use the free API tier without an API key
                self.coingecko_client = CoinGeckoAPI()
                logger.info("CoinGecko client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing CoinGecko client: {e}")
                self.coingecko_client = None
                config.EXCHANGES["coingecko"] = False
        else:
            self.coingecko_client = None
        
        # Initialize alert tracking
        self.last_alert_time = None
        self.alert_cooldown = config.ALERT_COOLDOWN if hasattr(config, 'ALERT_COOLDOWN') else 300  # Default 5 minutes
        
        logger.info(f"Initialized price discrepancy finder for {symbol}/{base_currency}")
        logger.info(f"Binance pair: {self.binance_pair}, Kraken pair: {self.kraken_pair}")
        logger.info(f"Arbitrage threshold set to {threshold_percent}%")
        logger.info(f"Enabled exchanges: {', '.join([k for k, v in config.EXCHANGES.items() if v])}")
    
    def get_binance_price(self):
        """Get the current price from Binance."""
        if not config.EXCHANGES["binance"] or self.binance_client is None:
            return None
            
        try:
            ticker = self.binance_client.get_ticker(symbol=self.binance_pair)
            self.consecutive_errors = 0  # Reset error counter on success
            return float(ticker['lastPrice'])
        except Exception as e:
            logger.error(f"Error fetching Binance price: {e}")
            self.consecutive_errors += 1
            return None
    
    def get_kraken_price(self):
        """Get the current price from Kraken."""
        if not config.EXCHANGES["kraken"] or self.kraken_client is None:
            return None
            
        try:
            response = self.kraken_client.query_public('Ticker', {'pair': self.kraken_pair})
            if 'error' in response and response['error']:
                logger.error(f"Kraken API error: {response['error']}")
                self.consecutive_errors += 1
                return None
            
            # Extract the price from the response using our utility function
            ticker_info = get_kraken_ticker_info(response, self.kraken_pair)
            if ticker_info:
                self.consecutive_errors = 0  # Reset error counter on success
                return ticker_info['last_price']
            
            # Fallback to direct extraction if our utility function fails
            for pair_name, pair_data in response['result'].items():
                self.consecutive_errors = 0  # Reset error counter on success
                return float(pair_data['c'][0])  # 'c' is the last trade closed array, [0] is the price
            
            self.consecutive_errors += 1
            return None
        except Exception as e:
            logger.error(f"Error fetching Kraken price: {e}")
            self.consecutive_errors += 1
            return None
    
    def get_coingecko_price(self):
        """Get the current price from CoinGecko."""
        if not config.EXCHANGES["coingecko"] or self.coingecko_client is None:
            return None
            
        try:
            # Convert symbol and base_currency to CoinGecko format using utility functions
            coin_id = get_coingecko_coin_id(self.symbol)
            currency = get_coingecko_currency(self.base_currency)
            
            # Get the price from CoinGecko
            price_data = self.coingecko_client.get_price(ids=coin_id, vs_currencies=currency)
            
            # Parse the price data using utility function
            price = parse_coingecko_price_data(price_data, coin_id, currency)
            
            # If price is None and we were trying to use USDT, fall back to USD
            if price is None and self.base_currency.lower() == 'usdt':
                logger.info("Falling back to USD for CoinGecko price")
                fallback_currency = 'usd'
                price_data = self.coingecko_client.get_price(ids=coin_id, vs_currencies=fallback_currency)
                price = parse_coingecko_price_data(price_data, coin_id, fallback_currency)
            
            if price is not None:
                self.consecutive_errors = 0  # Reset error counter on success
                return price
            else:
                logger.error(f"CoinGecko API returned unexpected data format: {price_data}")
                self.consecutive_errors += 1
                return None
        except Exception as e:
            logger.error(f"Error fetching CoinGecko price: {e}")
            self.consecutive_errors += 1
            return None
    
    def calculate_price_difference(self, price1, price2):
        """
        Calculate the percentage difference between two prices.
        
        Args:
            price1 (float): First price
            price2 (float): Second price
            
        Returns:
            float: Percentage difference
        """
        if price1 is None or price2 is None:
            return None
        
        avg_price = (price1 + price2) / 2
        diff_percent = abs(price1 - price2) / avg_price * 100
        return diff_percent
    
    def send_alert(self, message):
        """
        Send an alert when a significant price discrepancy is detected.
        
        Args:
            message (str): The alert message
        """
        # Check if we're within the cooldown period
        current_time = datetime.now()
        if self.last_alert_time and (current_time - self.last_alert_time).total_seconds() < self.alert_cooldown:
            logger.debug(f"Alert suppressed due to cooldown: {message}")
            return
        
        # Update the last alert time
        self.last_alert_time = current_time
        
        # Log the alert with a special prefix for easy filtering
        logger.critical(f"🚨 PRICE ALERT 🚨 {message}")
        
        # If configured, send the alert via other channels
        if hasattr(config, 'ENABLE_EMAIL_ALERTS') and config.ENABLE_EMAIL_ALERTS:
            self.send_email_alert(message)
        
        if hasattr(config, 'ENABLE_SMS_ALERTS') and config.ENABLE_SMS_ALERTS:
            self.send_sms_alert(message)
        
        if hasattr(config, 'ENABLE_WEBHOOK_ALERTS') and config.ENABLE_WEBHOOK_ALERTS:
            self.send_webhook_alert(message)
    
    def send_email_alert(self, message):
        """Send an email alert."""
        if not hasattr(config, 'EMAIL_TO') or not config.EMAIL_TO:
            logger.warning("Email alerts enabled but EMAIL_TO not configured")
            return
        
        # Use SMTP method for email alerts
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Create the email message
            email = MIMEMultipart()
            email['From'] = config.EMAIL_FROM if hasattr(config, 'EMAIL_FROM') else "price-alerts@crypto-tracker.com"
            email['To'] = config.EMAIL_TO
            email['Subject'] = f"{config.EMAIL_SUBJECT_PREFIX if hasattr(config, 'EMAIL_SUBJECT_PREFIX') else '[PRICE ALERT]'} {self.symbol}/{self.base_currency}"
            
            # Create the email body
            body = f"""
            <html>
            <body>
                <h2>Price Discrepancy Alert</h2>
                <p><strong>Symbol:</strong> {self.symbol}/{self.base_currency}</p>
                <p><strong>Alert:</strong> {message}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>This is an automated alert from your Cross-Exchange Price Tracker.</p>
            </body>
            </html>
            """
            
            # Attach the body to the email
            email.attach(MIMEText(body, 'html'))
            
            # Connect to the SMTP server and send the email
            smtp_server = config.SMTP_SERVER if hasattr(config, 'SMTP_SERVER') else "smtp.gmail.com"
            smtp_port = config.SMTP_PORT if hasattr(config, 'SMTP_PORT') else 587
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if hasattr(config, 'SMTP_USE_TLS') and config.SMTP_USE_TLS:
                    server.starttls()
                
                if hasattr(config, 'SMTP_USERNAME') and hasattr(config, 'SMTP_PASSWORD'):
                    server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
                
                server.send_message(email)
                
            logger.info(f"Email alert sent successfully via SMTP to {config.EMAIL_TO}")
            
        except Exception as e:
            logger.error(f"Error sending email alert via SMTP: {str(e)}")
    
    def send_sms_alert(self, message):
        """Send an SMS alert using Twilio."""
        if not hasattr(config, 'SMS_TO_NUMBER') or not config.SMS_TO_NUMBER:
            logger.warning("SMS alerts enabled but SMS_TO_NUMBER not configured")
            return
            
        # Check if Twilio credentials are configured
        if not hasattr(config, 'SMS_API_KEY') or not config.SMS_API_KEY or \
           not hasattr(config, 'SMS_API_SECRET') or not config.SMS_API_SECRET or \
           not hasattr(config, 'SMS_FROM_NUMBER') or not config.SMS_FROM_NUMBER:
            logger.warning("SMS alerts enabled but Twilio credentials not fully configured")
            return
            
        try:
            # Try to import the Twilio client
            # Note: This requires the twilio package to be installed
            # You can install it with: pip install twilio
            try:
                from twilio.rest import Client
            except ImportError:
                logger.error("Twilio package not installed. Install it with: pip install twilio")
                return
                
            # Initialize the Twilio client
            client = Client(config.SMS_API_KEY, config.SMS_API_SECRET)
            
            # Format the message
            sms_body = f"PRICE ALERT - {self.symbol}/{self.base_currency}: {message}"
            
            # Send the SMS
            message = client.messages.create(
                body=sms_body,
                from_=config.SMS_FROM_NUMBER,
                to=config.SMS_TO_NUMBER
            )
            
            logger.info(f"SMS alert sent to {config.SMS_TO_NUMBER} (SID: {message.sid})")
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
    
    def send_webhook_alert(self, message):
        """Send a webhook alert to the configured endpoint."""
        if not hasattr(config, 'WEBHOOK_URL') or not config.WEBHOOK_URL:
            logger.warning("Webhook alerts enabled but WEBHOOK_URL not configured")
            return
            
        try:
            import requests
            import json
            
            # Check if this is a Discord webhook URL
            is_discord_webhook = "discord.com/api/webhooks" in config.WEBHOOK_URL
            
            # Prepare the webhook payload
            if is_discord_webhook:
                # Format for Discord webhook
                embed_color = 15548997  # Red color in decimal
                
                payload = {
                    "username": "Price Alert Bot",
                    "content": f"🚨 **PRICE ALERT** 🚨",
                    "embeds": [
                        {
                            "title": f"{self.symbol}/{self.base_currency} Price Discrepancy",
                            "description": message,
                            "color": embed_color,
                            "fields": [
                                {
                                    "name": "Symbol",
                                    "value": self.symbol,
                                    "inline": True
                                },
                                {
                                    "name": "Base Currency",
                                    "value": self.base_currency,
                                    "inline": True
                                },
                                {
                                    "name": "Alert Type",
                                    "value": "Price Discrepancy",
                                    "inline": True
                                }
                            ],
                            "footer": {
                                "text": f"Alert Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        }
                    ]
                }
            else:
                # Standard webhook format for other services
                payload = {
                    "symbol": self.symbol,
                    "base_currency": self.base_currency,
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "alert_type": "price_discrepancy"
                }
            
            # Get the webhook method (default to POST)
            method = config.WEBHOOK_METHOD if hasattr(config, 'WEBHOOK_METHOD') else "POST"
            
            # Get the webhook headers (default to JSON content type)
            headers = config.WEBHOOK_HEADERS if hasattr(config, 'WEBHOOK_HEADERS') else {
                "Content-Type": "application/json"
            }
            
            # Send the webhook request
            if method.upper() == "POST":
                response = requests.post(
                    config.WEBHOOK_URL,
                    data=json.dumps(payload),
                    headers=headers
                )
            else:  # Default to GET
                response = requests.get(
                    config.WEBHOOK_URL,
                    params=payload,
                    headers=headers
                )
            
            # Check if the request was successful
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Webhook alert sent successfully (status code: {response.status_code})")
            else:
                logger.warning(f"Webhook alert failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
    
    def check_arbitrage_opportunity(self):
        """Check for arbitrage opportunities between exchanges."""
        binance_price = self.get_binance_price()
        kraken_price = self.get_kraken_price()
        coingecko_price = self.get_coingecko_price()
        
        # Store prices in a dictionary for easier comparison
        prices = {
            "Binance": binance_price,
            "Kraken": kraken_price,
            "CoinGecko": coingecko_price
        }
        
        # Filter out None values
        valid_prices = {k: v for k, v in prices.items() if v is not None}
        
        if len(valid_prices) < 2:
            logger.warning("Could not fetch prices from at least two exchanges")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log all available prices
        price_strings = []
        for exchange, price in valid_prices.items():
            price_strings.append(f"{exchange}: ${price:.2f}")
        
        logger.info(f"[{timestamp}] Current prices - {', '.join(price_strings)}")
        
        # Compare all pairs of exchanges
        for exchange1, price1 in valid_prices.items():
            for exchange2, price2 in valid_prices.items():
                if exchange1 >= exchange2:  # Skip duplicate comparisons
                    continue
                
                diff_percent = self.calculate_price_difference(price1, price2)
                
                if diff_percent is None:
                    continue
                
                logger.info(f"Price difference between {exchange1} and {exchange2}: {diff_percent:.2f}%")
                
                if diff_percent >= self.threshold_percent:
                    # Determine which exchange has the lower price (buy) and which has the higher price (sell)
                    buy_exchange = exchange2 if price1 > price2 else exchange1
                    sell_exchange = exchange1 if price1 > price2 else exchange2
                    buy_price = min(price1, price2)
                    sell_price = max(price1, price2)
                    
                    # Create the arbitrage opportunity message
                    arb_message = f"Buy on {buy_exchange} (${buy_price:.2f}) and sell on {sell_exchange} (${sell_price:.2f}) - Potential profit: {diff_percent:.2f}%"
                    
                    # Log the arbitrage opportunity
                    logger.warning(f"ARBITRAGE OPPORTUNITY: {arb_message}")
                    
                    # Send an alert if the discrepancy exceeds 1%
                    if diff_percent >= 1.0:
                        alert_message = f"{self.symbol}/{self.base_currency}: {arb_message}"
                        self.send_alert(alert_message)
    
    def run(self, interval_seconds=config.CHECK_INTERVAL):
        """
        Run the price discrepancy finder at regular intervals.
        
        Args:
            interval_seconds (int): Time between checks in seconds
        """
        logger.info(f"Starting price discrepancy finder, checking every {interval_seconds} seconds")
        
        try:
            while True:
                logger.info(f"Checking prices for {self.symbol}/{self.base_currency}...")
                
                # Check if we need to pause due to too many errors
                if self.consecutive_errors >= config.MAX_ERRORS:
                    logger.error(f"Too many consecutive errors ({self.consecutive_errors}). Pausing for {config.ERROR_PAUSE_DURATION} seconds.")
                    time.sleep(config.ERROR_PAUSE_DURATION)
                    self.consecutive_errors = 0
                    continue
                
                try:
                    self.check_arbitrage_opportunity()
                except Exception as e:
                    logger.error(f"Error checking arbitrage opportunity: {e}")
                    self.consecutive_errors += 1
                
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Price discrepancy finder stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Create and run the price discrepancy finder
    # You can customize the symbol, base currency, and threshold by editing config.py
    finder = PriceDiscrepancyFinder()
    
    # Run the finder with the configured check interval
    finder.run() 