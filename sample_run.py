#!/usr/bin/env python3

"""
Sample script to generate a quick output from the Cross-Exchange Price Discrepancy Finder.
This script runs the finder for a limited number of checks to demonstrate the output format.
"""

import logging
import time
from datetime import datetime
from price_discrepancy_finder import PriceDiscrepancyFinder
import config

def main():
    """Run the price discrepancy finder for a limited number of checks."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    # Log the configuration
    logger.info(f"Starting sample run with configuration:")
    logger.info(f"Symbol: {config.SYMBOL}")
    logger.info(f"Base currency: {config.BASE_CURRENCY}")
    logger.info(f"Threshold: {config.THRESHOLD_PERCENT}%")
    logger.info(f"Enabled exchanges: {', '.join([k for k, v in config.EXCHANGES.items() if v])}")
    
    # Create the finder
    finder = PriceDiscrepancyFinder(
        symbol=config.SYMBOL,
        base_currency=config.BASE_CURRENCY,
        threshold_percent=config.THRESHOLD_PERCENT
    )
    
    # Run for a limited number of checks
    logger.info("Running for 3 price checks with 5 second intervals")
    
    for i in range(3):
        logger.info(f"Price check #{i+1}")
        
        # Get prices from each exchange
        binance_price = finder.get_binance_price()
        kraken_price = finder.get_kraken_price()
        coingecko_price = finder.get_coingecko_price()
        
        # Store prices in a dictionary for easier display
        prices = {
            "Binance": binance_price,
            "Kraken": kraken_price,
            "CoinGecko": coingecko_price
        }
        
        # Filter out None values
        valid_prices = {k: v for k, v in prices.items() if v is not None}
        
        if valid_prices:
            # Display current prices
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            price_strings = []
            for exchange, price in valid_prices.items():
                price_strings.append(f"{exchange}: ${price:.6f}")
            
            logger.info(f"[{timestamp}] Current prices - {', '.join(price_strings)}")
            
            # Compare all pairs of exchanges
            for exchange1, price1 in valid_prices.items():
                for exchange2, price2 in valid_prices.items():
                    if exchange1 >= exchange2:  # Skip duplicate comparisons
                        continue
                    
                    diff_percent = finder.calculate_price_difference(price1, price2)
                    
                    if diff_percent is None:
                        continue
                    
                    logger.info(f"Price difference between {exchange1} and {exchange2}: {diff_percent:.2f}%")
                    
                    if diff_percent >= finder.threshold_percent:
                        # Determine which exchange has the lower price (buy) and which has the higher price (sell)
                        buy_exchange = exchange2 if price1 > price2 else exchange1
                        sell_exchange = exchange1 if price1 > price2 else exchange2
                        buy_price = min(price1, price2)
                        sell_price = max(price1, price2)
                        
                        # Create the arbitrage opportunity message
                        arb_message = f"Buy on {buy_exchange} (${buy_price:.6f}) and sell on {sell_exchange} (${sell_price:.6f}) - Potential profit: {diff_percent:.2f}%"
                        
                        # Log the arbitrage opportunity
                        logger.warning(f"ARBITRAGE OPPORTUNITY: {arb_message}")
        else:
            logger.warning("Could not fetch prices from any exchange")
        
        # Wait before next check (except for the last iteration)
        if i < 2:
            logger.info(f"Waiting 5 seconds before next check...")
            time.sleep(5)
    
    logger.info("Sample run completed")

if __name__ == "__main__":
    main() 