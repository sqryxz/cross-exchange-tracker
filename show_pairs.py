#!/usr/bin/env python3

"""
A simple script to show the available cryptocurrency pairs
for the Cross-Exchange Price Discrepancy Finder.
"""

from coin_selector import POPULAR_PAIRS, STABLECOIN_PAIRS

def show_pairs():
    """Display the available cryptocurrency pairs."""
    print("\n" + "=" * 60)
    print("  AVAILABLE CRYPTOCURRENCY PAIRS")
    print("=" * 60)
    
    print("\nPopular Pairs:")
    print("-" * 60)
    for i, pair in enumerate(POPULAR_PAIRS):
        print(f"{i}. {pair['name']} ({pair['symbol']}/{pair['base']})")
    
    print("\nStablecoin Pairs:")
    print("-" * 60)
    for i, pair in enumerate(STABLECOIN_PAIRS, start=len(POPULAR_PAIRS)):
        print(f"{i}. {pair['name']} ({pair['symbol']}/{pair['base']})")
    
    print("\nTo track any of these pairs, use:")
    print("python3 run.py -s SYMBOL -b BASE")
    print("\nExample:")
    print("python3 run.py -s BTC -b USDT")
    print("\nOr use the interactive selector:")
    print("python3 coin_selector.py")
    print("\n")

if __name__ == "__main__":
    show_pairs() 