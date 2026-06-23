from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def home_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🔍 Price Check", callback_data="price")],
        [InlineKeyboardButton(text="📖 How to Use", callback_data="howto")],
        [
            InlineKeyboardButton(text="🏆 Top Coins", callback_data="top"),
            InlineKeyboardButton(text="🔔 Alerts", callback_data="alerts"),
        ],
        [
            InlineKeyboardButton(text="📊 Portfolio", callback_data="portfolio"),
            InlineKeyboardButton(text="ℹ️ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="🔐 Privacy", callback_data="privacy"),
            InlineKeyboardButton(text="📜 Terms", callback_data="terms"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def home_keyboard_colored():
    buttons = [
        [InlineKeyboardButton(text="🔍 Price Check", callback_data="price", style="primary")],
        [InlineKeyboardButton(text="📖 How to Use", callback_data="howto", style="success")],
        [
            InlineKeyboardButton(text="🏆 Top Coins", callback_data="top", style="primary"),
            InlineKeyboardButton(text="🔔 Alerts", callback_data="alerts", style="primary"),
        ],
        [
            InlineKeyboardButton(text="📊 Portfolio", callback_data="portfolio", style="primary"),
            InlineKeyboardButton(text="ℹ️ Help", callback_data="help", style="primary"),
        ],
        [
            InlineKeyboardButton(text="🔐 Privacy", callback_data="privacy", style="primary"),
            InlineKeyboardButton(text="📜 Terms", callback_data="terms", style="primary"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_home_keyboard():
    buttons = [[InlineKeyboardButton(text="← Back to Dashboard", callback_data="home")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def portfolio_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="✚ Add Holding", callback_data="portfolio_add", style="primary"),
            InlineKeyboardButton(text="📋 Example", callback_data="portfolio_example", style="success"),
        ],
        [InlineKeyboardButton(text="← Back", callback_data="home")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def alerts_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="✚ New Alert", callback_data="alert_new", style="primary"),
            InlineKeyboardButton(text="📋 Example", callback_data="alert_example", style="success"),
        ],
        [InlineKeyboardButton(text="← Back", callback_data="home")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def price_coins_keyboard():
    coins = [
        ("BTC", "bitcoin"),
        ("ETH", "ethereum"),
        ("SOL", "solana"),
        ("XRP", "ripple"),
        ("DOGE", "dogecoin"),
    ]
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"price_coin:{cid}") for name, cid in coins[:3]],
        [InlineKeyboardButton(text=name, callback_data=f"price_coin:{cid}") for name, cid in coins[3:]],
        [InlineKeyboardButton(text="← Back", callback_data="home")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_keyboard(action, data):
    buttons = [
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data=f"{action}_yes:{data}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data=f"{action}_no:{data}"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
