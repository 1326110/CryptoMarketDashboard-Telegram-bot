from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def home_keyboard():
    buttons = [
        [InlineKeyboardButton("🔍 Price Check", callback_data="price")],
        [
            InlineKeyboardButton("🏆 Top Coins", callback_data="top"),
            InlineKeyboardButton("🔔 Alerts", callback_data="alerts"),
        ],
        [
            InlineKeyboardButton("📊 Portfolio", callback_data="portfolio"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("🔒 Privacy", callback_data="privacy"),
            InlineKeyboardButton("©️ Terms", callback_data="terms"),
        ],
        [InlineKeyboardButton("📖 How to Use", callback_data="howto")],
    ]
    return InlineKeyboardMarkup(buttons)

def home_keyboard_colored():
    buttons = [
        [InlineKeyboardButton("🔍 Price Check", callback_data="price", style="primary")],
        [InlineKeyboardButton("📖 How to Use", callback_data="howto", style="success")],
        [
            InlineKeyboardButton("🏆 Top Coins", callback_data="top", style="primary"),
            InlineKeyboardButton("🔔 Alerts", callback_data="alerts", style="primary"),
        ],
        [
            InlineKeyboardButton("📊 Portfolio", callback_data="portfolio", style="primary"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help", style="primary"),
        ],
        [
            InlineKeyboardButton("🔒 Privacy", callback_data="privacy", style="primary"),
            InlineKeyboardButton("©️ Terms", callback_data="terms", style="primary"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def back_home_keyboard():
    buttons = [[InlineKeyboardButton("← Back to Dashboard", callback_data="home")]]
    return InlineKeyboardMarkup(buttons)

def portfolio_keyboard():
    buttons = [
        [
            InlineKeyboardButton("➕ Add Holding", callback_data="portfolio_add", style="primary"),
            InlineKeyboardButton("📋 Example", callback_data="portfolio_example", style="success"),
        ],
        [InlineKeyboardButton("← Back", callback_data="home")],
    ]
    return InlineKeyboardMarkup(buttons)

def alerts_keyboard():
    buttons = [
        [InlineKeyboardButton("➕ New Alert", callback_data="alert_new", style="primary")],
        [InlineKeyboardButton("📋 Example", callback_data="alert_example", style="success")],
        [InlineKeyboardButton("← Back", callback_data="home")],
    ]
    return InlineKeyboardMarkup(buttons)

def price_coins_keyboard():
    coins = [
        ("BTC", "bitcoin"),
        ("ETH", "ethereum"),
        ("SOL", "solana"),
        ("XRP", "ripple"),
        ("DOGE", "dogecoin"),
    ]
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"price_coin:{cid}") for name, cid in coins[:3]],
        [InlineKeyboardButton(name, callback_data=f"price_coin:{cid}") for name, cid in coins[3:]],
        [InlineKeyboardButton("← Back", callback_data="home")],
    ]
    return InlineKeyboardMarkup(buttons)

def confirm_keyboard(action, data):
    buttons = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=f"{action}_yes:{data}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"{action}_no:{data}"),
        ]
    ]
    return InlineKeyboardMarkup(buttons)
