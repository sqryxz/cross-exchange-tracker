# Discord Webhook Alert - Visual Representation

When the cross-exchange tracker detects a significant price discrepancy, here's what the alert would actually look like in your Discord channel:

## XRP/USDT Arbitrage Opportunity (1.25% Difference)

```
┌─────────────────────────────────────────────────────────────────┐
│ Price Alert Bot                                       Today at 1:15 PM │
│ 🚨 **PRICE ALERT** 🚨                                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                                                             │ │
│ │ XRP/USDT Price Discrepancy                                  │ │
│ │                                                             │ │
│ │ Buy on Binance ($2.336400) and sell on Kraken ($2.365730)   │ │
│ │ - Potential profit: 1.25%                                   │ │
│ │                                                             │ │
│ │ Symbol           Base Currency      Alert Type              │ │
│ │ XRP              USDT               Price Discrepancy       │ │
│ │                                                             │ │
│ │ Alert Time: 2025-03-18 01:15:45                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## BTC/USDT Significant Arbitrage Opportunity (2.5% Difference)

```
┌─────────────────────────────────────────────────────────────────┐
│ Price Alert Bot                                       Today at 4:30 PM │
│ 🚨 **PRICE ALERT** 🚨                                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                                                             │ │
│ │ BTC/USDT Price Discrepancy                                  │ │
│ │                                                             │ │
│ │ Buy on Binance ($68245.50) and sell on CoinGecko ($69950.75)│ │
│ │ - Potential profit: 2.50%                                   │ │
│ │                                                             │ │
│ │ Symbol           Base Currency      Alert Type              │ │
│ │ BTC              USDT               Price Discrepancy       │ │
│ │                                                             │ │
│ │ Alert Time: 2025-03-18 04:30:15                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## How to Configure Discord Webhooks in Your Project

To set up Discord webhook alerts in your cross-exchange tracker:

1. **Create a webhook in Discord**:
   - Go to your Discord server
   - Click on Server Settings > Integrations > Webhooks
   - Click "New Webhook"
   - Name it "Price Alert Bot"
   - Choose the channel where you want to receive alerts
   - Click "Copy Webhook URL"

2. **Configure your project**:
   - Open `config.py`
   - Set the following values:
     ```python
     # Enable webhook alerts
     ENABLE_WEBHOOK_ALERTS = True
     
     # Set your Discord webhook URL
     WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-url"
     
     # These are already set correctly by default for Discord
     WEBHOOK_METHOD = "POST"
     WEBHOOK_HEADERS = {
         "Content-Type": "application/json"
     }
     ```

3. **Test your configuration**:
   - Run the tracker with a low threshold to trigger alerts
   - Check your Discord channel for the alerts

The system automatically detects Discord webhook URLs and formats the messages with proper embeds, fields, and formatting to make the alerts visually appealing and informative. 