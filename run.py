#!/usr/bin/env python3

"""
Command-line interface for the Cross-Exchange Price Discrepancy Finder.
This script allows you to run the finder with custom parameters without editing the config file.
"""

import argparse
import logging
from price_discrepancy_finder import PriceDiscrepancyFinder
import config

def main():
    """Parse command-line arguments and run the price discrepancy finder."""
    parser = argparse.ArgumentParser(
        description="Cross-Exchange Price Discrepancy Finder",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-s", "--symbol",
        default=config.SYMBOL,
        help="Cryptocurrency symbol to track (e.g., BTC, ETH, SOL)"
    )
    
    parser.add_argument(
        "-b", "--base",
        default=config.BASE_CURRENCY,
        help="Base currency for comparison (e.g., USDT, USD, EUR)"
    )
    
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=config.THRESHOLD_PERCENT,
        help="Minimum price difference percentage to log as a potential arbitrage opportunity"
    )
    
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=config.CHECK_INTERVAL,
        help="Time between price checks in seconds"
    )
    
    parser.add_argument(
        "-l", "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=config.LOG_LEVEL,
        help="Set the logging level"
    )
    
    parser.add_argument(
        "--disable-binance",
        action="store_true",
        help="Disable Binance exchange"
    )
    
    parser.add_argument(
        "--disable-kraken",
        action="store_true",
        help="Disable Kraken exchange"
    )
    
    parser.add_argument(
        "--disable-coingecko",
        action="store_true",
        help="Disable CoinGecko exchange"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    # Override exchange settings from command line
    if args.disable_binance:
        config.EXCHANGES["binance"] = False
    
    if args.disable_kraken:
        config.EXCHANGES["kraken"] = False
    
    if args.disable_coingecko:
        config.EXCHANGES["coingecko"] = False
    
    # Log the configuration
    logger.info(f"Starting with configuration:")
    logger.info(f"Symbol: {args.symbol}")
    logger.info(f"Base currency: {args.base}")
    logger.info(f"Threshold: {args.threshold}%")
    logger.info(f"Check interval: {args.interval} seconds")
    logger.info(f"Enabled exchanges: {', '.join([k for k, v in config.EXCHANGES.items() if v])}")
    
    # Create and run the finder
    finder = PriceDiscrepancyFinder(
        symbol=args.symbol,
        base_currency=args.base,
        threshold_percent=args.threshold
    )
    
    finder.run(interval_seconds=args.interval)

if __name__ == "__main__":
    main() 