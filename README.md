# MarketPulse

A Telegram bot for real-time cryptocurrency market monitoring. Track prices, set alerts, and manage your portfolio — all inside Telegram.

## Features

- **Price Check** — Look up any cryptocurrency's current price, 24h change, market cap, and rank
- **Market Overview** — Top 10 coins by market cap at a glance
- **Price Alerts** — Set target prices and get notified when the market crosses your threshold
- **Portfolio Tracker** — Log your holdings and see their total value in real time

## Demo

| Command | Description |
|---|---|
| `/start` | Launch the dashboard |
| `/help` | View available commands |
| `/price bitcoin` | Check a coin's price |
| `/top` | Top coins by market cap |
| `/alert ethereum 3000` | Set a price alert |
| `/portfolio` | Manage your holdings |
| `/privacy` | Privacy policy |
| `/terms` | Terms of use |

## Tech Stack

- **Python 3.11+**
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v22.x
- [CoinGecko API](https://www.coingecko.com/en/api) (free, no API key required)
- **Storage:** Local JSON file (portable, no database setup)

## Getting Started

### Prerequisites

- Python 3.11 or later
- A Telegram bot token from [@BotFather](https://t.me/botfather)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/marketpulse-bot.git
cd marketpulse-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your bot token
echo 'BOT_TOKEN="your_telegram_bot_token_here"' > .env

# Run the bot
python main.py
```

### BotFather Setup

1. Open [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the prompts
3. Set a profile photo (high-resolution, at least 512x512)
4. Set a bio using the suggested text from [`BOT_PROFILE.md`](BOT_PROFILE.md)
5. Enable inline mode if desired
6. Copy the token and set it as `BOT_TOKEN`

## Project Structure

```
marketpulse-bot/
├── main.py                # Entry point, handler registration
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── bot/
│   ├── crypto_api.py      # CoinGecko API wrapper
│   ├── database.py        # JSON storage layer
│   ├── handlers.py        # Command and callback handlers
│   ├── keyboards.py       # Inline keyboard layouts
│   └── messages.py        # All user-facing text
├── AD_COPY.md             # Compliant ad copy samples
├── BOT_PROFILE.md         # Recommended Telegram profile setup
├── COMPLIANCE.md          # Full compliance matrix with Telegram ad policies
└── REVIEW_CHECKLIST.md    # Pre-submission review checklist
```

## Compliance

MarketPulse is designed to comply with Telegram's advertising policies for cryptocurrency-related bots. See [`COMPLIANCE.md`](COMPLIANCE.md) for the full compliance matrix.

### Key Compliance Points

- Framed as an **analytics/monitoring tool** — not a trading or investment platform
- **No profit language** — zero references to earnings, returns, or gains
- **Instant interaction** — no login walls, no paywalls, no friction at entry
- **Inline keyboards** — clean navigation without imperatives
- **Transparency** — `/privacy` and `/terms` commands with clear data handling policies

## License

MIT
