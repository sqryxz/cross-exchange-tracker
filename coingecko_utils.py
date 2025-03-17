#!/usr/bin/env python3

"""
Utility functions for working with CoinGecko's API.
CoinGecko uses specific coin IDs and currency formats that differ from other exchanges.
"""

def get_coingecko_coin_id(symbol):
    """
    Convert a standard cryptocurrency symbol to CoinGecko's specific coin ID.
    
    Args:
        symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH')
        
    Returns:
        str: The CoinGecko coin ID
    """
    # Common mappings for major assets
    symbol_mapping = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'xrp': 'ripple',
        'ltc': 'litecoin',
        'bch': 'bitcoin-cash',
        'ada': 'cardano',
        'dot': 'polkadot',
        'sol': 'solana',
        'doge': 'dogecoin',
        'link': 'chainlink',
        'uni': 'uniswap',
        'xlm': 'stellar',
        'matic': 'matic-network',
        'avax': 'avalanche-2',
        'atom': 'cosmos',
        'algo': 'algorand',
        'fil': 'filecoin',
        'vet': 'vechain',
        'etc': 'ethereum-classic',
        'theta': 'theta-token',
        'trx': 'tron',
        'axs': 'axie-infinity',
        'icp': 'internet-computer',
        'xtz': 'tezos',
        'ftm': 'fantom',
        'near': 'near',
        'egld': 'elrond-erd-2',
        'xmr': 'monero',
        'flow': 'flow',
        'hbar': 'hedera-hashgraph',
        'eos': 'eos',
        'cake': 'pancakeswap-token',
        'qnt': 'quant-network',
        'xec': 'ecash',
        'mana': 'decentraland',
        'sand': 'the-sandbox',
        'enj': 'enjincoin',
        'stx': 'blockstack',
        'gala': 'gala',
        'one': 'harmony',
        'chz': 'chiliz',
        'hot': 'holotoken',
        'kcs': 'kucoin-shares',
        'neo': 'neo',
        'btt': 'bittorrent',
        'waves': 'waves',
        'mkr': 'maker',
        'hnt': 'helium',
        'dash': 'dash',
        'zec': 'zcash',
    }
    
    # Convert symbol to lowercase for case-insensitive matching
    symbol_lower = symbol.lower()
    
    # Return the mapped coin ID or the lowercase symbol if not found
    return symbol_mapping.get(symbol_lower, symbol_lower)

def get_coingecko_currency(currency):
    """
    Convert a standard currency code to CoinGecko's specific format.
    
    Args:
        currency (str): The currency code (e.g., 'USD', 'EUR', 'USDT')
        
    Returns:
        str: The CoinGecko currency format
    """
    # Common mappings for currencies
    currency_mapping = {
        'usdt': 'tether',
        'usdc': 'usd-coin',
        'busd': 'binance-usd',
        'dai': 'dai',
        'ust': 'terrausd',
        'tusd': 'true-usd',
        'usdp': 'paxos-standard',
        'gusd': 'gemini-dollar',
    }
    
    # Convert currency to lowercase for case-insensitive matching
    currency_lower = currency.lower()
    
    # Return the mapped currency or the lowercase currency if not found
    return currency_mapping.get(currency_lower, currency_lower)

def parse_coingecko_price_data(price_data, coin_id, currency):
    """
    Extract relevant price information from CoinGecko's response.
    
    Args:
        price_data (dict): The price data from CoinGecko's API
        coin_id (str): The coin ID used in the request
        currency (str): The currency used in the request
        
    Returns:
        float or None: The price if available, None otherwise
    """
    try:
        if coin_id in price_data and currency in price_data[coin_id]:
            return float(price_data[coin_id][currency])
        return None
    except (KeyError, ValueError, TypeError):
        return None
