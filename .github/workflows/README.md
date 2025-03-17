# GitHub Actions for Cross-Exchange Tracker

This directory contains GitHub Actions workflows for the Cross-Exchange Tracker project.

## Available Workflows

### 1. Cross-Exchange Tracker CI (`python-app.yml`)

This workflow runs on every push to the main branch and on pull requests. It:

- Sets up Python 3.10
- Installs dependencies from requirements.txt
- Runs linting with flake8
- Executes the sample script to verify basic functionality

### 2. Scheduled Cross-Exchange Tracker (`scheduled-tracker.yml`)

This workflow runs on a schedule (every 6 hours) and can also be triggered manually. It:

- Sets up Python 3.10
- Installs dependencies
- Creates an environment file with API keys from GitHub Secrets
- Runs the tracker for 10 minutes with BTC/USDT, a 2% threshold, and 30-second check interval
- Uploads the log file as an artifact for later inspection

## Setting Up API Keys

For the scheduled workflow to work properly, you need to set up the following secrets in your GitHub repository:

1. Go to your repository on GitHub
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Add the following secrets:
   - `BINANCE_API_KEY`: Your Binance API key
   - `BINANCE_API_SECRET`: Your Binance API secret
   - `KRAKEN_API_KEY`: Your Kraken API key
   - `KRAKEN_API_SECRET`: Your Kraken API secret

## Manual Triggering

To manually trigger the scheduled workflow:

1. Go to the "Actions" tab in your repository
2. Select "Scheduled Cross-Exchange Tracker" from the workflows list
3. Click "Run workflow" > "Run workflow"

## Viewing Results

After a scheduled run completes:

1. Go to the "Actions" tab
2. Click on the completed workflow run
3. Scroll down to the "Artifacts" section
4. Download "arbitrage-logs" to view the results 