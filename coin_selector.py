#!/usr/bin/env python3

"""
A simple menu-based selector for choosing different altcoin pairs
to track with the Cross-Exchange Price Discrepancy Finder.
"""

import os
import sys
from price_discrepancy_finder import PriceDiscrepancyFinder
import config

# Define popular altcoin pairs
POPULAR_PAIRS = [
    {"symbol": "BTC", "base": "USDT", "name": "Bitcoin/USDT"},
    {"symbol": "ETH", "base": "USDT", "name": "Ethereum/USDT"},
    {"symbol": "SOL", "base": "USDT", "name": "Solana/USDT"},
    {"symbol": "ADA", "base": "USDT", "name": "Cardano/USDT"},
    {"symbol": "DOT", "base": "USDT", "name": "Polkadot/USDT"},
    {"symbol": "DOGE", "base": "USDT", "name": "Dogecoin/USDT"},
    {"symbol": "XRP", "base": "USDT", "name": "Ripple/USDT"},
    {"symbol": "LINK", "base": "USDT", "name": "Chainlink/USDT"},
    {"symbol": "AVAX", "base": "USDT", "name": "Avalanche/USDT"},
    {"symbol": "MATIC", "base": "USDT", "name": "Polygon/USDT"},
    {"symbol": "BTC", "base": "USD", "name": "Bitcoin/USD"},
    {"symbol": "ETH", "base": "USD", "name": "Ethereum/USD"},
]

# Add some stablecoin pairs
STABLECOIN_PAIRS = [
    {"symbol": "USDT", "base": "USD", "name": "Tether/USD"},
    {"symbol": "USDC", "base": "USD", "name": "USD Coin/USD"},
    {"symbol": "BUSD", "base": "USD", "name": "Binance USD/USD"},
]

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("\n" + "=" * 60)
    print("  CROSS-EXCHANGE PRICE DISCREPANCY FINDER - PAIR SELECTOR")
    print("=" * 60)
    print("\nSelect a cryptocurrency pair to track:")
    print("-" * 60)

def print_menu(pairs, start_idx=0):
    """Print the menu of available pairs."""
    for i, pair in enumerate(pairs, start=start_idx):
        print(f"{i}. {pair['name']} ({pair['symbol']}/{pair['base']})")

def get_custom_pair():
    """Get a custom pair from user input."""
    print("\nEnter custom pair details:")
    symbol = input("Symbol (e.g., BTC, ETH, SOL): ").strip().upper()
    base = input("Base currency (e.g., USDT, USD, EUR): ").strip().upper()
    
    if not symbol or not base:
        print("Invalid input. Using default ETH/USDT.")
        return {"symbol": "ETH", "base": "USDT"}
    
    return {"symbol": symbol, "base": base, "name": f"{symbol}/{base}"}

def get_threshold():
    """Get the threshold percentage from user input."""
    while True:
        try:
            threshold = float(input("\nEnter price difference threshold % (default: 1.0): ").strip() or "1.0")
            if threshold <= 0:
                print("Threshold must be greater than 0.")
                continue
            return threshold
        except ValueError:
            print("Please enter a valid number.")

def get_interval():
    """Get the check interval from user input."""
    while True:
        try:
            interval = int(input("\nEnter check interval in seconds (default: 60): ").strip() or "60")
            if interval < 10:
                print("Interval must be at least 10 seconds.")
                continue
            return interval
        except ValueError:
            print("Please enter a valid number.")

def select_pair():
    """Display the menu and get the user's selection."""
    clear_screen()
    print_header()
    
    # Print popular pairs
    print("\nPopular Pairs:")
    print_menu(POPULAR_PAIRS)
    
    # Print stablecoin pairs
    print("\nStablecoin Pairs:")
    print_menu(STABLECOIN_PAIRS, start_idx=len(POPULAR_PAIRS))
    
    # Custom pair option
    custom_idx = len(POPULAR_PAIRS) + len(STABLECOIN_PAIRS)
    print(f"\n{custom_idx}. Enter custom pair")
    
    # Get user selection
    while True:
        try:
            choice = input("\nEnter your choice (0-{}): ".format(custom_idx)).strip()
            if not choice:
                # Default to ETH/USDT
                return POPULAR_PAIRS[1]
            
            choice = int(choice)
            if 0 <= choice < len(POPULAR_PAIRS):
                return POPULAR_PAIRS[choice]
            elif len(POPULAR_PAIRS) <= choice < custom_idx:
                return STABLECOIN_PAIRS[choice - len(POPULAR_PAIRS)]
            elif choice == custom_idx:
                return get_custom_pair()
            else:
                print(f"Please enter a number between 0 and {custom_idx}.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    """Main function to run the pair selector."""
    try:
        # Get pair selection
        pair = select_pair()
        
        # Get threshold and interval
        threshold = get_threshold()
        interval = get_interval()
        
        # Display selection
        clear_screen()
        print("\n" + "=" * 60)
        print(f"  TRACKING: {pair['name']}")
        print(f"  THRESHOLD: {threshold}%")
        print(f"  INTERVAL: {interval} seconds")
        print("=" * 60)
        print("\nPress Ctrl+C to stop tracking.\n")
        
        # Create and run the finder with selected pair
        finder = PriceDiscrepancyFinder(
            symbol=pair['symbol'],
            base_currency=pair['base'],
            threshold_percent=threshold
        )
        
        # Run the finder
        finder.run(interval_seconds=interval)
        
    except KeyboardInterrupt:
        print("\nExiting pair selector.")
        sys.exit(0)

if __name__ == "__main__":
    main() 