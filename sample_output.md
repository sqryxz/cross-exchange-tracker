# Cross-Exchange Tracker Sample Output

This document shows sample outputs from the cross-exchange tracker, including scenarios with significant price discrepancies that would trigger arbitrage alerts.

## Normal Operation (Small Price Differences)

```
2025-03-18 00:41:18,024 - INFO - Starting with configuration:
2025-03-18 00:41:18,024 - INFO - Symbol: XRP
2025-03-18 00:41:18,024 - INFO - Base currency: USDT
2025-03-18 00:41:18,024 - INFO - Threshold: 1.0%
2025-03-18 00:41:18,024 - INFO - Enabled exchanges: binance, kraken, coingecko
2025-03-18 00:41:18,255 - INFO - Binance client initialized successfully
2025-03-18 00:41:18,255 - INFO - Kraken client initialized successfully
2025-03-18 00:41:18,255 - INFO - CoinGecko client initialized successfully
2025-03-18 00:41:18,255 - INFO - Initialized price discrepancy finder for XRP/USDT
2025-03-18 00:41:18,255 - INFO - Binance pair: XRPUSDT, Kraken pair: XRPUSDT
2025-03-18 00:41:18,255 - INFO - Arbitrage threshold set to 1.0%
2025-03-18 00:41:18,255 - INFO - Enabled exchanges: binance, kraken, coingecko

2025-03-18 00:41:19,015 - INFO - [2025-03-18 00:41:19] Current prices - Binance: $2.336400, Kraken: $2.336730, CoinGecko: $2.340000
2025-03-18 00:41:19,015 - INFO - Price difference between Binance and Kraken: 0.01%
2025-03-18 00:41:19,015 - INFO - Price difference between Binance and CoinGecko: 0.15%
2025-03-18 00:41:19,015 - INFO - Price difference between CoinGecko and Kraken: 0.14%

2025-03-18 00:41:24,822 - INFO - [2025-03-18 00:41:24] Current prices - Binance: $2.335200, Kraken: $2.336730, CoinGecko: $2.340000
2025-03-18 00:41:24,822 - INFO - Price difference between Binance and Kraken: 0.07%
2025-03-18 00:41:24,822 - INFO - Price difference between Binance and CoinGecko: 0.21%
2025-03-18 00:41:24,822 - INFO - Price difference between CoinGecko and Kraken: 0.14%

2025-03-18 00:42:30,415 - INFO - [2025-03-18 00:42:30] Current prices - Binance: $2.334800, Kraken: $2.336730, CoinGecko: $2.330000
2025-03-18 00:42:30,416 - INFO - Price difference between Binance and Kraken: 0.08%
2025-03-18 00:42:30,416 - INFO - Price difference between Binance and CoinGecko: 0.21%
2025-03-18 00:42:30,416 - INFO - Price difference between CoinGecko and Kraken: 0.29%
```

## Arbitrage Opportunity Detected (> 1% Difference)

```
2025-03-18 01:15:45,123 - INFO - [2025-03-18 01:15:45] Current prices - Binance: $2.336400, Kraken: $2.365730, CoinGecko: $2.340000
2025-03-18 01:15:45,124 - INFO - Price difference between Binance and Kraken: 1.25%
2025-03-18 01:15:45,124 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Binance ($2.336400) and sell on Kraken ($2.365730) - Potential profit: 1.25%
2025-03-18 01:15:45,124 - INFO - Price difference between Binance and CoinGecko: 0.15%
2025-03-18 01:15:45,124 - INFO - Price difference between CoinGecko and Kraken: 1.10%
2025-03-18 01:15:45,124 - WARNING - ARBITRAGE OPPORTUNITY: Buy on CoinGecko ($2.340000) and sell on Kraken ($2.365730) - Potential profit: 1.10%
2025-03-18 01:15:45,125 - INFO - Sending alert for arbitrage opportunity
2025-03-18 01:15:45,126 - INFO - Email alert sent successfully
```

## Significant Arbitrage Opportunity (> 2% Difference)

```
2025-03-18 02:30:12,456 - INFO - [2025-03-18 02:30:12] Current prices - Binance: $2.336400, Kraken: $2.336730, CoinGecko: $2.390000
2025-03-18 02:30:12,457 - INFO - Price difference between Binance and Kraken: 0.01%
2025-03-18 02:30:12,457 - INFO - Price difference between Binance and CoinGecko: 2.29%
2025-03-18 02:30:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Binance ($2.336400) and sell on CoinGecko ($2.390000) - Potential profit: 2.29%
2025-03-18 02:30:12,457 - INFO - Price difference between CoinGecko and Kraken: 2.28%
2025-03-18 02:30:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Kraken ($2.336730) and sell on CoinGecko ($2.390000) - Potential profit: 2.28%
2025-03-18 02:30:12,458 - INFO - Sending alert for arbitrage opportunity
2025-03-18 02:30:12,459 - INFO - Email alert sent successfully
2025-03-18 02:30:12,460 - INFO - SMS alert sent successfully
```

## Error Handling Example

```
2025-03-18 03:45:23,789 - INFO - [2025-03-18 03:45:23] Current prices - Binance: $2.336400, Kraken: $2.336730
2025-03-18 03:45:23,790 - WARNING - Could not fetch price from CoinGecko: Rate limit exceeded
2025-03-18 03:45:23,790 - INFO - Price difference between Binance and Kraken: 0.01%

2025-03-18 03:46:23,789 - INFO - [2025-03-18 03:46:23] Current prices - Binance: $2.336400
2025-03-18 03:46:23,790 - WARNING - Could not fetch price from Kraken: Connection timeout
2025-03-18 03:46:23,790 - WARNING - Could not fetch price from CoinGecko: Rate limit exceeded
2025-03-18 03:46:23,790 - WARNING - Could not fetch prices from at least two exchanges
```

## Different Cryptocurrency Example (BTC/USDT)

```
2025-03-18 04:15:45,123 - INFO - Starting with configuration:
2025-03-18 04:15:45,123 - INFO - Symbol: BTC
2025-03-18 04:15:45,123 - INFO - Base currency: USDT
2025-03-18 04:15:45,123 - INFO - Threshold: 1.0%
2025-03-18 04:15:45,123 - INFO - Enabled exchanges: binance, kraken, coingecko

2025-03-18 04:15:46,234 - INFO - [2025-03-18 04:15:46] Current prices - Binance: $68245.50, Kraken: $68267.30, CoinGecko: $68250.00
2025-03-18 04:15:46,235 - INFO - Price difference between Binance and Kraken: 0.03%
2025-03-18 04:15:46,235 - INFO - Price difference between Binance and CoinGecko: 0.01%
2025-03-18 04:15:46,235 - INFO - Price difference between CoinGecko and Kraken: 0.03%

2025-03-18 04:16:46,345 - INFO - [2025-03-18 04:16:46] Current prices - Binance: $68245.50, Kraken: $68950.75, CoinGecko: $68250.00
2025-03-18 04:16:46,346 - INFO - Price difference between Binance and Kraken: 1.03%
2025-03-18 04:16:46,346 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Binance ($68245.50) and sell on Kraken ($68950.75) - Potential profit: 1.03%
2025-03-18 04:16:46,346 - INFO - Price difference between Binance and CoinGecko: 0.01%
2025-03-18 04:16:46,346 - INFO - Price difference between CoinGecko and Kraken: 1.03%
2025-03-18 04:16:46,346 - WARNING - ARBITRAGE OPPORTUNITY: Buy on CoinGecko ($68250.00) and sell on Kraken ($68950.75) - Potential profit: 1.03%
2025-03-18 04:16:46,347 - INFO - Sending alert for arbitrage opportunity
2025-03-18 04:16:46,348 - INFO - Email alert sent successfully
```

## Multiple Consecutive Arbitrage Opportunities

```
2025-03-18 05:30:12,456 - INFO - [2025-03-18 05:30:12] Current prices - Binance: $2.336400, Kraken: $2.336730, CoinGecko: $2.390000
2025-03-18 05:30:12,457 - INFO - Price difference between Binance and Kraken: 0.01%
2025-03-18 05:30:12,457 - INFO - Price difference between Binance and CoinGecko: 2.29%
2025-03-18 05:30:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Binance ($2.336400) and sell on CoinGecko ($2.390000) - Potential profit: 2.29%
2025-03-18 05:30:12,457 - INFO - Price difference between CoinGecko and Kraken: 2.28%
2025-03-18 05:30:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Kraken ($2.336730) and sell on CoinGecko ($2.390000) - Potential profit: 2.28%
2025-03-18 05:30:12,458 - INFO - Sending alert for arbitrage opportunity
2025-03-18 05:30:12,459 - INFO - Email alert sent successfully

2025-03-18 05:31:12,456 - INFO - [2025-03-18 05:31:12] Current prices - Binance: $2.336400, Kraken: $2.336730, CoinGecko: $2.395000
2025-03-18 05:31:12,457 - INFO - Price difference between Binance and Kraken: 0.01%
2025-03-18 05:31:12,457 - INFO - Price difference between Binance and CoinGecko: 2.51%
2025-03-18 05:31:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Binance ($2.336400) and sell on CoinGecko ($2.395000) - Potential profit: 2.51%
2025-03-18 05:31:12,457 - INFO - Price difference between CoinGecko and Kraken: 2.49%
2025-03-18 05:31:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Kraken ($2.336730) and sell on CoinGecko ($2.395000) - Potential profit: 2.49%
2025-03-18 05:31:12,458 - INFO - Sending alert for arbitrage opportunity
2025-03-18 05:31:12,459 - INFO - Email alert sent successfully

2025-03-18 05:32:12,456 - INFO - [2025-03-18 05:32:12] Current prices - Binance: $2.336400, Kraken: $2.336730, CoinGecko: $2.385000
2025-03-18 05:32:12,457 - INFO - Price difference between Binance and Kraken: 0.01%
2025-03-18 05:32:12,457 - INFO - Price difference between Binance and CoinGecko: 2.08%
2025-03-18 05:32:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Binance ($2.336400) and sell on CoinGecko ($2.385000) - Potential profit: 2.08%
2025-03-18 05:32:12,457 - INFO - Price difference between CoinGecko and Kraken: 2.07%
2025-03-18 05:32:12,457 - WARNING - ARBITRAGE OPPORTUNITY: Buy on Kraken ($2.336730) and sell on CoinGecko ($2.385000) - Potential profit: 2.07%
2025-03-18 05:32:12,458 - INFO - Sending alert for arbitrage opportunity
2025-03-18 05:32:12,459 - INFO - Email alert sent successfully
``` 