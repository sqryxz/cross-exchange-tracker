# Discord Webhook Alert Example

When the cross-exchange tracker detects a significant price discrepancy that exceeds your threshold, it can send an alert to Discord via webhooks. Here's what the alert would look like in your Discord channel:

## Example 1: XRP/USDT Arbitrage Opportunity (1.25% Difference)

![Discord Webhook Alert Example](https://i.imgur.com/placeholder.png)

```
Price Alert Bot
--------------
🚨 **PRICE ALERT** 🚨

[Embed]
Title: XRP/USDT Price Discrepancy
Description: Buy on Binance ($2.336400) and sell on Kraken ($2.365730) - Potential profit: 1.25%
Color: Red

Fields:
Symbol: XRP
Base Currency: USDT
Alert Type: Price Discrepancy

Footer: Alert Time: 2025-03-18 01:15:45
```

## Example 2: BTC/USDT Significant Arbitrage Opportunity (2.5% Difference)

![Discord Webhook Alert Example](https://i.imgur.com/placeholder2.png)

```
Price Alert Bot
--------------
🚨 **PRICE ALERT** 🚨

[Embed]
Title: BTC/USDT Price Discrepancy
Description: Buy on Binance ($68245.50) and sell on CoinGecko ($69950.75) - Potential profit: 2.50%
Color: Red

Fields:
Symbol: BTC
Base Currency: USDT
Alert Type: Price Discrepancy

Footer: Alert Time: 2025-03-18 04:30:15
```

## How to Set Up Discord Webhooks

To receive these alerts in your Discord server:

1. In Discord, go to Server Settings > Integrations > Webhooks
2. Click "New Webhook"
3. Name it "Price Alert Bot" (optional)
4. Choose the channel where you want to receive alerts
5. Click "Copy Webhook URL"
6. In your `config.py` file, set:
   ```python
   ENABLE_WEBHOOK_ALERTS = True
   WEBHOOK_URL = "your-discord-webhook-url-here"
   ```

The system will automatically detect that it's a Discord webhook URL and format the message appropriately. 