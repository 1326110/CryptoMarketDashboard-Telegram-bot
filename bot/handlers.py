import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import bot.messages as msg
import bot.keyboards as kb
import bot.crypto_api as api
import bot.database as db

logger = logging.getLogger(__name__)

USER_STATE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        msg.WELCOME, parse_mode="Markdown", reply_markup=kb.home_keyboard_colored()
    )

async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        msg.HOME_MENU, parse_mode="Markdown", reply_markup=kb.home_keyboard_colored()
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            msg.HELP, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )
    else:
        await update.message.reply_text(
            msg.HELP, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )

async def price_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    USER_STATE[update.effective_user.id] = "awaiting_price"
    await query.edit_message_text(
        msg.PRICE_PROMPT, parse_mode="Markdown", reply_markup=kb.price_coins_keyboard()
    )

async def price_coin_quick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    coin_id = query.data.split(":", 1)[1]
    await _show_price(update, context, coin_id)

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            msg.PRICE_PROMPT,
            parse_mode="Markdown",
            reply_markup=kb.back_home_keyboard(),
        )
        return
    coin = " ".join(context.args)
    await _show_price(update, context, coin)

async def handle_price_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if USER_STATE.get(uid) == "awaiting_price":
        USER_STATE[uid] = None
        await _show_price(update, context, update.message.text)

async def _show_price(update: Update, context: ContextTypes.DEFAULT_TYPE, coin: str):
    info = api.search_coins(coin)
    if not info:
        text = msg.PRICE_ERROR
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=kb.back_home_keyboard())
        else:
            await update.message.reply_text(text, reply_markup=kb.back_home_keyboard())
        return

    detail = api.get_price_with_detail(info["id"])
    if not detail:
        text = msg.PRICE_ERROR
    else:
        change = detail.get("price_change_percentage_24h", 0) or 0
        emoji = "\U0001f7e2" if change >= 0 else "\U0001f534"
        decimals = 2 if detail["current_price"] >= 1 else 6
        text = msg.PRICE_RESULT.format(
            name=detail["name"],
            symbol=detail["symbol"].upper(),
            price=detail["current_price"],
            decimals=decimals,
            change_24h=change,
            change_emoji=emoji,
            market_cap=detail.get("market_cap", 0),
            rank=detail.get("market_cap_rank", "N/A"),
        )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )
    else:
        await update.message.reply_text(
            text, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )

async def howto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        msg.HOWTO, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
    )

async def top_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = api.get_top_coins(10)
    if not data:
        await query.edit_message_text(
            msg.ERROR_GENERIC, reply_markup=kb.back_home_keyboard()
        )
        return

    lines = [msg.TOP_HEADER]
    for c in data:
        change = c.get("price_change_percentage_24h", 0) or 0
        emoji = "\U0001f7e2" if change >= 0 else "\U0001f534"
        lines.append(
            msg.TOP_ROW.format(
                rank=c.get("market_cap_rank", "?"),
                name=c["name"],
                symbol=c["symbol"].upper(),
                price=c["current_price"],
                change=change,
                emoji=emoji,
            )
        )
    lines.append(msg.TOP_FOOTER)
    await query.edit_message_text(
        "".join(lines), parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
    )

async def alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    alerts = db.get_alerts(uid)

    if not alerts:
        await query.edit_message_text(
            msg.ALERT_NO_ALERTS,
            parse_mode="Markdown",
            reply_markup=kb.alerts_keyboard(),
        )
        return

    lines = [msg.ALERT_LIST_HEADER]
    buttons = []
    for i, a in enumerate(alerts):
        p = api.get_price(a["coin_id"])
        current = p.get("usd", 0) if p else 0
        lines.append(
            msg.ALERT_LIST_ROW.format(
                name=a["coin_name"], target=a["target"], current=current
            )
        )
        buttons.append(
            [InlineKeyboardButton(f"\u274c Remove {a['coin_name']}", callback_data=f"alert_remove:{i}")]
        )
    buttons.append([InlineKeyboardButton("\u2190 Back", callback_data="home")])
    await query.edit_message_text(
        "".join(lines),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: `/alert <coin> <target_price>`\n\n"
            "Example: `/alert bitcoin 45000`",
            parse_mode="Markdown",
        )
        return
    coin = context.args[0]
    try:
        target = float(context.args[1].replace(",", "").replace("$", ""))
    except ValueError:
        await update.message.reply_text(
            "⚠️ Invalid target price. Example: `/alert bitcoin 45000`",
            parse_mode="Markdown",
        )
        return
    info = api.search_coins(coin)
    if not info:
        await update.message.reply_text(
            msg.ALERT_ERROR, reply_markup=kb.back_home_keyboard()
        )
        return
    p = api.get_price(info["id"])
    current = p.get("usd", 0) if p else 0
    db.add_alert(update.effective_user.id, info["id"], info["name"], info["symbol"], target)
    await update.message.reply_text(
        msg.ALERT_CREATED.format(
            name=info["name"],
            symbol=info["symbol"].upper(),
            target=target,
            current=current,
        ),
        parse_mode="Markdown",
        reply_markup=kb.home_keyboard_colored(),
    )

async def alert_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    USER_STATE[update.effective_user.id] = "awaiting_alert_coin"
    await query.edit_message_text(
        msg.ALERT_SETUP, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
    )

async def alert_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    parts = query.data.split(":")
    idx = int(parts[1])
    removed = db.remove_alert(uid, idx)
    if removed:
        await query.edit_message_text(
            msg.ALERT_REMOVED.format(name=removed["coin_name"]),
            parse_mode="Markdown",
            reply_markup=kb.alerts_keyboard(),
        )
    else:
        await query.edit_message_text(
            msg.ERROR_GENERIC, reply_markup=kb.back_home_keyboard()
        )

async def handle_alert_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if USER_STATE.get(uid) == "awaiting_alert_coin":
        coin = update.message.text.strip()
        info = api.search_coins(coin)
        if not info:
            await update.message.reply_text(
                msg.ALERT_ERROR, reply_markup=kb.back_home_keyboard()
            )
            return
        context.user_data["alert_coin"] = info
        USER_STATE[uid] = "awaiting_alert_target"
        await update.message.reply_text(
            msg.ALERT_COIN_RECEIVED.format(coin=info["name"]),
            parse_mode="Markdown",
            reply_markup=kb.back_home_keyboard(),
        )

async def handle_alert_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if USER_STATE.get(uid) == "awaiting_alert_target":
        try:
            target = float(update.message.text.strip().replace(",", "").replace("$", ""))
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return

        info = context.user_data.get("alert_coin")
        if not info:
            USER_STATE[uid] = None
            await update.message.reply_text(msg.ERROR_GENERIC)
            return

        p = api.get_price(info["id"])
        current = p.get("usd", 0) if p else 0

        db.add_alert(uid, info["id"], info["name"], info["symbol"], target)
        USER_STATE[uid] = None
        await update.message.reply_text(
            msg.ALERT_CREATED.format(
                name=info["name"],
                symbol=info["symbol"].upper(),
                target=target,
                current=current,
            ),
            parse_mode="Markdown",
            reply_markup=kb.home_keyboard_colored(),
        )

async def alert_example(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        msg.ALERT_EXAMPLE, parse_mode="Markdown", reply_markup=kb.alerts_keyboard()
    )

async def portfolio_example(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        msg.PORTFOLIO_EXAMPLE, parse_mode="Markdown", reply_markup=kb.portfolio_keyboard()
    )

async def portfolio_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    holdings = db.get_portfolio(uid)

    if not holdings:
        await query.edit_message_text(
            msg.PORTFOLIO_EMPTY,
            parse_mode="Markdown",
            reply_markup=kb.portfolio_keyboard(),
        )
        return

    lines = []
    total = 0
    buttons = []
    for i, h in enumerate(holdings):
        p = api.get_price(h["coin_id"])
        price = p.get("usd", 0) if p else 0
        value = h["amount"] * price
        total += value
        lines.append(
            msg.PORTFOLIO_ROW.format(amount=h["amount"], symbol=h["symbol"].upper(), value=value)
        )

    text = msg.PORTFOLIO_VIEW.format(holdings="".join(lines), total=total)
    buttons.append(
        [
            InlineKeyboardButton("\u2795 Add", callback_data="portfolio_add"),
            InlineKeyboardButton("\u2796 Remove", callback_data="portfolio_remove"),
        ]
    )
    buttons.append([InlineKeyboardButton("\u2190 Back", callback_data="home")])
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

async def portfolio_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    USER_STATE[update.effective_user.id] = "awaiting_portfolio_coin"
    await query.edit_message_text(
        msg.PORTFOLIO_ADD_COIN,
        parse_mode="Markdown",
        reply_markup=kb.back_home_keyboard(),
    )

async def handle_portfolio_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if USER_STATE.get(uid) == "awaiting_portfolio_coin":
        coin = update.message.text.strip()
        info = api.search_coins(coin)
        if not info:
            await update.message.reply_text(
                msg.ALERT_ERROR, reply_markup=kb.back_home_keyboard()
            )
            return
        context.user_data["portfolio_coin"] = info
        USER_STATE[uid] = "awaiting_portfolio_amount"
        await update.message.reply_text(
            msg.PORTFOLIO_ADD_AMOUNT.format(name=info["name"]),
            parse_mode="Markdown",
            reply_markup=kb.back_home_keyboard(),
        )

async def handle_portfolio_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if USER_STATE.get(uid) == "awaiting_portfolio_amount":
        try:
            amount = float(update.message.text.strip().replace(",", ""))
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return

        info = context.user_data.get("portfolio_coin")
        if not info:
            USER_STATE[uid] = None
            await update.message.reply_text(msg.ERROR_GENERIC)
            return

        p = api.get_price(info["id"])
        price = p.get("usd", 0) if p else 0
        value = amount * price

        db.add_holding(uid, info["id"], info["name"], info["symbol"], amount)
        USER_STATE[uid] = None
        await update.message.reply_text(
            msg.PORTFOLIO_ADD_CONFIRM.format(
                amount=amount,
                symbol=info["symbol"].upper(),
                name=info["name"],
                value=value,
            ),
            parse_mode="Markdown",
            reply_markup=kb.home_keyboard_colored(),
        )

async def portfolio_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    holdings = db.get_portfolio(uid)

    if not holdings:
        await query.edit_message_text(
            msg.PORTFOLIO_EMPTY,
            parse_mode="Markdown",
            reply_markup=kb.portfolio_keyboard(),
        )
        return

    buttons = []
    for i, h in enumerate(holdings):
        buttons.append(
            [
                InlineKeyboardButton(
                    f"\u274c {h['coin_name']} ({h['amount']} {h['symbol'].upper()})",
                    callback_data=f"portfolio_remove_idx:{i}",
                )
            ]
        )
    buttons.append([InlineKeyboardButton("\u2190 Back", callback_data="portfolio")])
    await query.edit_message_text(
        msg.PORTFOLIO_REMOVE_PROMPT,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

async def portfolio_remove_idx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    idx = int(query.data.split(":")[1])
    removed = db.remove_holding(uid, idx)
    if removed:
        await query.edit_message_text(
            msg.PORTFOLIO_REMOVED.format(name=removed["coin_name"]),
            parse_mode="Markdown",
            reply_markup=kb.back_home_keyboard(),
        )
    else:
        await query.edit_message_text(
            msg.ERROR_GENERIC, reply_markup=kb.back_home_keyboard()
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    state = USER_STATE.get(uid)

    if state == "awaiting_price":
        await handle_price_input(update, context)
    elif state == "awaiting_alert_coin":
        await handle_alert_coin(update, context)
    elif state == "awaiting_alert_target":
        await handle_alert_target(update, context)
    elif state == "awaiting_portfolio_coin":
        await handle_portfolio_coin(update, context)
    elif state == "awaiting_portfolio_amount":
        await handle_portfolio_amount(update, context)
    else:
        await update.message.reply_text(
            "Use the menu below to navigate 👇",
            reply_markup=kb.home_keyboard_colored(),
        )

async def privacy_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            msg.PRIVACY, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )
    else:
        await update.message.reply_text(
            msg.PRIVACY, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )

async def terms_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            msg.TERMS, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )
    else:
        await update.message.reply_text(
            msg.TERMS, parse_mode="Markdown", reply_markup=kb.back_home_keyboard()
        )

async def alert_checker(app: Application):
    import asyncio
    from config import CHECK_INTERVAL

    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        try:
            data = db.load_all()
            for uid_str, u_data in data.get("users", {}).items():
                uid = int(uid_str)
                alerts = u_data.get("alerts", [])
                triggered = []
                for i, a in enumerate(alerts):
                    p = api.get_price(a["coin_id"])
                    if not p:
                        continue
                    current = p.get("usd", 0)
                    if current >= a["target"]:
                        try:
                            await app.bot.send_message(
                                uid,
                                msg.ALERT_TRIGGERED.format(
                                    name=a["coin_name"],
                                    symbol=a["symbol"].upper(),
                                    target=a["target"],
                                    price=current,
                                ),
                                parse_mode="Markdown",
                            )
                            triggered.append(i)
                        except Exception:
                            logger.exception("Failed to send alert")
                for i in reversed(triggered):
                    alerts.pop(i)
                if triggered:
                    db._save_user(uid, u_data)
        except Exception:
            logger.exception("Alert checker error")
