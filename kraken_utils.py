#!/usr/bin/env python3

"""
Utility functions for working with Kraken's API.
Kraken uses specific asset pair formatting that differs from other exchanges.
"""

def get_kraken_asset_pair(symbol, base_currency):
    """
    Convert a standard symbol/base pair to Kraken's specific format.
    
    For example:
    - ETH/USD becomes XETHZUSD
    - BTC/EUR becomes XXBTZEUR
    - Some newer assets don't follow this pattern
    
    Args:
        symbol (str): The cryptocurrency symbol (e.g., 'ETH')
        base_currency (str): The base currency (e.g., 'USD')
        
    Returns:
        str: The Kraken-formatted asset pair
    """
    # Common mappings for major assets
    symbol_map = {
        'BTC': 'XXBT',
        'ETH': 'XETH',
        'LTC': 'XLTC',
        'XRP': 'XXRP',
        'ETC': 'XETC',
        'ZEC': 'XZEC',
        'XMR': 'XXMR',
        'DASH': 'DASH',
        'EOS': 'EOS',
        'BCH': 'BCH',
        'ADA': 'ADA',
        'ATOM': 'ATOM',
        'LINK': 'LINK',
        'DOT': 'DOT',
        'SOL': 'SOL',
        'DOGE': 'DOGE',
        'USDT': 'USDT',
    }
    
    base_map = {
        'USD': 'ZUSD',
        'EUR': 'ZEUR',
        'GBP': 'ZGBP',
        'JPY': 'ZJPY',
        'CAD': 'ZCAD',
        'AUD': 'ZAUD',
        'USDT': 'USDT',
        'USDC': 'USDC',
    }
    
    # Get the mapped values or use the original if not in the map
    kraken_symbol = symbol_map.get(symbol.upper(), symbol.upper())
    kraken_base = base_map.get(base_currency.upper(), base_currency.upper())
    
    # Combine to form the Kraken pair
    kraken_pair = f"{kraken_symbol}{kraken_base}"
    
    # Special case handling for common pairs
    # Kraken has specific naming conventions for certain pairs
    special_pairs = {
        # USDT pairs
        "XETHUSDT": "ETHUSDT",
        "XXBTUSDT": "XBTUSDT",
        "ADAUSDT": "ADAUSDT",
        "DOTUSDT": "DOTUSDT",
        "SOLUSDT": "SOLUSDT",
        "DOGEUSDT": "DOGEUSDT",
        "XXRPUSDT": "XRPUSDT",
        "LINKUSDT": "LINKUSDT",
        
        # USD pairs
        "XETHZUSD": "ETHUSD",
        "XXBTZUSD": "XBTUSD",
        "ADAZUSD": "ADAUSD",
        "DOTZUSD": "DOTUSD",
        "SOLZUSD": "SOLUSD",
        "DOGEZUSD": "DOGEUSD",
        "XXRPZUSD": "XRPUSD",
        "LINKZUSD": "LINKUSD",
        
        # EUR pairs
        "XETHZEUR": "ETHEUR",
        "XXBTZEUR": "XBTEUR",
    }
    
    # Return the special pair if it exists, otherwise return the standard format
    return special_pairs.get(kraken_pair, kraken_pair)

def get_kraken_ticker_info(ticker_data, pair_name):
    """
    Extract relevant ticker information from Kraken's response.
    
    Args:
        ticker_data (dict): The ticker data from Kraken's API
        pair_name (str): The pair name used in the request
        
    Returns:
        dict: A dictionary with formatted ticker information
    """
    if not ticker_data or 'result' not in ticker_data:
        return None
    
    # Kraken sometimes returns results with a different key than what was requested
    # We need to find the actual key in the result
    result = ticker_data['result']
    if not result:
        return None
    
    # If the exact pair name is in the result, use it
    if pair_name in result:
        pair_data = result[pair_name]
    else:
        # Otherwise, try to find the first (and hopefully only) key in the result
        if len(result) > 0:
            first_key = next(iter(result))
            pair_data = result[first_key]
        else:
            return None
    
    try:
        return {
            'last_price': float(pair_data['c'][0]),
            'volume': float(pair_data['v'][1]),
            'vwap': float(pair_data['p'][1]),
            'low': float(pair_data['l'][1]),
            'high': float(pair_data['h'][1]),
            'bid': float(pair_data['b'][0]),
            'ask': float(pair_data['a'][0]),
        }
    except (KeyError, IndexError, ValueError) as e:
        # If we can't parse the data properly, return None
        return None 