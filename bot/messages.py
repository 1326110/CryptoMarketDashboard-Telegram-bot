WELCOME = (
    "✨ Welcome to *MarketPulse* — your real-time crypto market dashboard.\n\n"
    "I help you track prices, monitor trends, and stay informed.\n\n"
    "⚡ *Quick Start*\n"
    "• Check any coin price instantly\n"
    "• View top market movers\n"
    "• Set custom price alerts\n"
    "• Track your portfolio\n\n"
    "Use the menu below to get started 👇"
)

HOME_MENU = "🏠 *Dashboard* — what would you like to do?"

HOWTO = (
    "📖 *How to Use MarketPulse*\n\n"
    "🔍 *Price Check* — Tap to search any crypto's price, 24h change, and market cap. You can also tap BTC/ETH/SOL/XRP/DOGE for instant results.\n\n"
    "🏆 *Top Coins* — Shows the top 10 cryptocurrencies ranked by market cap with current price and 24h change.\n\n"
    "🔔 *Alerts* — Set a target price for any coin. You'll get a notification when the price crosses your target. Use `/alert bitcoin 45000` for speed.\n\n"
    "📊 *Portfolio* — Log how much of each coin you hold. The bot calculates total value using live prices.\n\n"
    "ℹ️ *Help* — Lists all available commands.\n\n"
    "🔒 *Privacy / ©️ Terms* — How your data is handled and terms of use.\n\n"
    "_All data from CoinGecko • updated every minute_"
)

HELP = (
    "ℹ️ *About MarketPulse*\n\n"
    "I monitor cryptocurrency market data in real time.\n\n"
    "📊 *Features*\n"
    "• `/price <coin>` — check current price\n"
    "• `/top` — top coins by market cap\n"
    "• `/alert <coin> <target>` — set a price alert\n"
    "• `/portfolio` — manage your portfolio\n\n"
    "• `/privacy` — how your data is handled\n"
    "• `/terms` — terms of use\n\n"
    "All data sourced from CoinGecko • updated every minute"
)

PRIVACY = (
    "🔒 *Privacy Policy*\n\n"
    "MarketPulse is designed with your privacy in mind.\n\n"
    "📌 *What we store*\n"
    "• Your Telegram user ID (for alerts and portfolio)\n"
    "• Alert targets you set\n"
    "• Portfolio holdings you enter\n\n"
    "📌 *What we don't store*\n"
    "• Messages or personal conversations\n"
    "• Location or contact data\n"
    "• Any data from third-party services\n\n"
    "📌 *Data handling*\n"
    "• All data stored locally in a JSON file\n"
    "• No data shared with third parties\n"
    "• You can delete your data by removing alerts and portfolio entries\n\n"
    "Contact @username for data removal requests."
)

TERMS = (
    "©️ *Terms of Use*\n\n"
    "By using MarketPulse, you agree to the following:\n\n"
    "📌 *Service*\n"
    "• MarketPulse provides cryptocurrency market data for informational purposes only\n"
    "• Data is sourced from public APIs (CoinGecko) and may have delays\n\n"
    "📌 *Not Financial Advice*\n"
    "• All information is for reference only\n"
    "• No content constitutes financial or investment advice\n"
    "• Always do your own research before making decisions\n\n"
    "📌 *Limitations*\n"
    "• Service provided \"as is\" without warranties\n"
    "• We may suspend or modify the service at any time\n"
    "• Not responsible for API downtime or data inaccuracies\n\n"
    "Use `/help` for support."
)

PRICE_PROMPT = "🔍 Tap a coin below or type a name/symbol (e.g., `bitcoin` or `BTC`):"

PRICE_RESULT = (
    "📊 *{name}* ({symbol})\n\n"
    "💵 Price: `${price:,.{decimals}f}`\n"
    "📈 24h Change: `{change_24h:+.2f}%` {change_emoji}\n"
    "📊 Market Cap: `${market_cap:,.0f}`\n"
    "📍 Rank: `#{rank}`\n\n"
    "_Data from CoinGecko_"
)

PRICE_ERROR = "⚠️ Could not find data for that cryptocurrency. Please check the symbol and try again."

TOP_HEADER = "🏆 *Top Coins by Market Cap*\n\n"

TOP_ROW = "`{rank}.` *{name}* `{symbol}` — `${price:,}` — *{change:+.2f}%* {emoji}\n"

TOP_FOOTER = "\n_Data refreshes every minute • CoinGecko_"

ALERT_SETUP = "🔔 Set a price alert\n\nWhich coin would you like to monitor?"

ALERT_COIN_RECEIVED = "Got it — *{coin}*. Now enter your target price in USD:\n\nExample: `45000`"

ALERT_CREATED = (
    "✅ Alert created!\n\n"
    "📎 *{name}* ({symbol})\n"
    "🎯 Target: `${target:,.2f}`\n"
    "🔍 Current: `${current:,.2f}`\n\n"
    "I'll notify you when the price crosses this level."
)

ALERT_TRIGGERED = (
    "🔔 *Price Alert Triggered*\n\n"
    "*{name}* ({symbol}) has crossed your target of `${target:,.2f}`.\n"
    "Current price: `${price:,.2f}`\n\n"
    "Use `/alerts` to view or manage your alerts."
)

ALERT_ERROR = "⚠️ Could not find that coin. Please check the symbol."

ALERT_NO_ALERTS = "ℹ️ You have no active price alerts. Use `/alert <coin> <target>` to create one."

ALERT_EXAMPLE = (
    "📋 *Alert Example*\n\n"
    "When you set alerts, they appear like this:\n\n"
    "🔔 *Your Active Alerts*\n\n"
    "• Bitcoin — target `$45,000` (current: `$62,296`)\n"
    "• Ethereum — target `$3,000` (current: `$1,653`)\n\n"
    "Tap ➕ New Alert to set your own."
)

ALERT_LIST_HEADER = "🔔 *Your Active Alerts*\n\n"

ALERT_LIST_ROW = "• *{name}* — target `${target:,.2f}` (current: `${current:,.2f}`)\n"

ALERT_REMOVED = "✅ Alert for *{name}* has been removed."

ALERT_CANCEL = "Alert setup cancelled."

PORTFOLIO_EMPTY = (
    "📊 Your portfolio is empty.\n\n"
    "Use the button below to add your first holding."
)

PORTFOLIO_EXAMPLE = (
    "📋 *Portfolio Example*\n\n"
    "When you add holdings, they appear like this:\n\n"
    "📊 *Your Portfolio*\n\n"
    "• 0.5 BTC — `$31,148.00`\n"
    "• 10 ETH — `$16,528.30`\n"
    "--------------------\n"
    "*Total: $47,676.30*\n\n"
    "Tap ➕ Add Holding to get started."
)

PORTFOLIO_ADD_COIN = "Which coin would you like to add? (e.g., `bitcoin` or `ETH`)"

PORTFOLIO_ADD_AMOUNT = "Enter the amount of *{name}* you hold:\n\nExample: `2.5`"

PORTFOLIO_ADD_CONFIRM = (
    "✅ Added to portfolio!\n\n"
    "📎 *{amount} {symbol}* ({name})\n"
    "💵 Value: `${value:,.2f}`"
)

PORTFOLIO_VIEW = (
    "📊 *Your Portfolio*\n\n"
    "{holdings}\n"
    "--------------------\n"
    "💵 *Total Value: `${total:,.2f}`*"
)

PORTFOLIO_ROW = "• *{amount}* {symbol} — `${value:,.2f}`\n"

PORTFOLIO_REMOVE_PROMPT = "Which holding would you like to remove?"

PORTFOLIO_REMOVED = "✅ *{name}* removed from your portfolio."

PORTFOLIO_CANCEL = "Cancelled."

ERROR_GENERIC = "⚠️ Something went wrong. Please try again."

ALREADY_WATCHING = "ℹ️ You already have an alert for *{name}* at `${target:,.2f}`."
