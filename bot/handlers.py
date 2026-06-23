import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot

import bot.messages as msg
import bot.keyboards as kb
import bot.crypto_api as api
import bot.database as db

logger = logging.getLogger(__name__)

router = Router()
USER_STATE = {}
USER_DATA = {}

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        msg.WELCOME, reply_markup=kb.home_keyboard_colored()
    )

@router.callback_query(F.data == "home")
async def home(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        msg.HOME_MENU, reply_markup=kb.home_keyboard_colored()
    )

@router.callback_query(F.data == "help")
@router.message(Command("help"))
async def help_cmd(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(
            msg.HELP, reply_markup=kb.back_home_keyboard()
        )
    else:
        await event.answer(
            msg.HELP, reply_markup=kb.back_home_keyboard()
        )

@router.callback_query(F.data == "price")
async def price_prompt(callback_query: CallbackQuery):
    await callback_query.answer()
    USER_STATE[callback_query.from_user.id] = "awaiting_price"
    await callback_query.message.edit_text(
        msg.PRICE_PROMPT, reply_markup=kb.price_coins_keyboard()
    )

@router.callback_query(F.data.startswith("price_coin:"))
async def price_coin_quick(callback_query: CallbackQuery):
    await callback_query.answer()
    coin_id = callback_query.data.split(":", 1)[1]
    await _show_price(callback_query, coin_id)

@router.message(Command("price"))
async def price_command(message: Message, command: CommandObject):
    coin = command.args
    if not coin:
        await message.answer(
            msg.PRICE_PROMPT,
            reply_markup=kb.back_home_keyboard(),
        )
        return
    await _show_price(message, coin)

async def handle_price_input(message: Message):
    await _show_price(message, message.text)

async def _show_price(event: Message | CallbackQuery, coin: str):
    info = api.search_coins(coin)
    if not info:
        text = msg.PRICE_ERROR
        reply = kb.back_home_keyboard()
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text, reply_markup=reply)
        else:
            await event.answer(text, reply_markup=reply)
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

    reply = kb.back_home_keyboard()
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=reply)
    else:
        await event.answer(text, reply_markup=reply)

@router.callback_query(F.data == "howto")
async def howto(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        msg.HOWTO, reply_markup=kb.back_home_keyboard()
    )

@router.callback_query(F.data == "top")
async def top_coins(callback_query: CallbackQuery):
    await callback_query.answer()
    data = api.get_top_coins(10)
    if not data:
        await callback_query.message.edit_text(
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
    await callback_query.message.edit_text(
        "".join(lines), reply_markup=kb.back_home_keyboard()
    )

@router.callback_query(F.data == "alerts")
async def alerts_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    uid = callback_query.from_user.id
    alerts = db.get_alerts(uid)

    if not alerts:
        await callback_query.message.edit_text(
            msg.ALERT_NO_ALERTS,
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
            [InlineKeyboardButton(text=f"\u274c Remove {a['coin_name']}", callback_data=f"alert_remove:{i}")]
        )
    buttons.append([InlineKeyboardButton(text="\u2190 Back", callback_data="home")])
    await callback_query.message.edit_text(
        "".join(lines),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )

@router.message(Command("alert"))
async def alert_command(message: Message, command: CommandObject):
    args = command.args
    if not args:
        await message.answer(
            "Usage: `/alert <coin> <target_price>`\n\n"
            "Example: `/alert bitcoin 45000`",
        )
        return
    parts = args.split()
    if len(parts) < 2:
        await message.answer(
            "⚠️ Please provide both a coin and target price.\n\n"
            "Example: `/alert bitcoin 45000`",
        )
        return
    coin = parts[0]
    try:
        target = float(parts[1].replace(",", "").replace("$", ""))
    except ValueError:
        await message.answer(
            "⚠️ Invalid target price. Example: `/alert bitcoin 45000`",
        )
        return
    info = api.search_coins(coin)
    if not info:
        await message.answer(
            msg.ALERT_ERROR, reply_markup=kb.back_home_keyboard()
        )
        return
    p = api.get_price(info["id"])
    current = p.get("usd", 0) if p else 0
    db.add_alert(message.from_user.id, info["id"], info["name"], info["symbol"], target)
    await message.answer(
        msg.ALERT_CREATED.format(
            name=info["name"],
            symbol=info["symbol"].upper(),
            target=target,
            current=current,
        ),
        reply_markup=kb.home_keyboard_colored(),
    )

@router.callback_query(F.data == "alert_new")
async def alert_new(callback_query: CallbackQuery):
    await callback_query.answer()
    USER_STATE[callback_query.from_user.id] = "awaiting_alert_coin"
    await callback_query.message.edit_text(
        msg.ALERT_SETUP, reply_markup=kb.back_home_keyboard()
    )

@router.callback_query(F.data.startswith("alert_remove:"))
async def alert_remove(callback_query: CallbackQuery):
    await callback_query.answer()
    uid = callback_query.from_user.id
    idx = int(callback_query.data.split(":")[1])
    removed = db.remove_alert(uid, idx)
    if removed:
        await callback_query.message.edit_text(
            msg.ALERT_REMOVED.format(name=removed["coin_name"]),
            reply_markup=kb.alerts_keyboard(),
        )
    else:
        await callback_query.message.edit_text(
            msg.ERROR_GENERIC, reply_markup=kb.back_home_keyboard()
        )

async def handle_alert_coin(message: Message):
    uid = message.from_user.id
    if USER_STATE.get(uid) == "awaiting_alert_coin":
        coin = message.text.strip()
        info = api.search_coins(coin)
        if not info:
            await message.answer(
                msg.ALERT_ERROR, reply_markup=kb.back_home_keyboard()
            )
            return
        USER_DATA[uid] = info
        USER_STATE[uid] = "awaiting_alert_target"
        await message.answer(
            msg.ALERT_COIN_RECEIVED.format(coin=info["name"]),
            reply_markup=kb.back_home_keyboard(),
        )

async def handle_alert_target(message: Message):
    uid = message.from_user.id
    if USER_STATE.get(uid) == "awaiting_alert_target":
        try:
            target = float(message.text.strip().replace(",", "").replace("$", ""))
        except ValueError:
            await message.answer("Please enter a valid number.")
            return

        info = USER_DATA.get(uid)
        if not info:
            USER_STATE[uid] = None
            await message.answer(msg.ERROR_GENERIC)
            return

        p = api.get_price(info["id"])
        current = p.get("usd", 0) if p else 0

        db.add_alert(uid, info["id"], info["name"], info["symbol"], target)
        USER_STATE[uid] = None
        USER_DATA.pop(uid, None)
        await message.answer(
            msg.ALERT_CREATED.format(
                name=info["name"],
                symbol=info["symbol"].upper(),
                target=target,
                current=current,
            ),
            reply_markup=kb.home_keyboard_colored(),
        )

@router.callback_query(F.data == "alert_example")
async def alert_example(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        msg.ALERT_EXAMPLE, reply_markup=kb.alerts_keyboard()
    )

@router.callback_query(F.data == "portfolio_example")
async def portfolio_example(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        msg.PORTFOLIO_EXAMPLE, reply_markup=kb.portfolio_keyboard()
    )

@router.callback_query(F.data == "portfolio")
async def portfolio_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    uid = callback_query.from_user.id
    holdings = db.get_portfolio(uid)

    if not holdings:
        await callback_query.message.edit_text(
            msg.PORTFOLIO_EMPTY,
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
            InlineKeyboardButton(text="\u2795 Add", callback_data="portfolio_add"),
            InlineKeyboardButton(text="\u2796 Remove", callback_data="portfolio_remove"),
        ]
    )
    buttons.append([InlineKeyboardButton(text="\u2190 Back", callback_data="home")])
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )

@router.callback_query(F.data == "portfolio_add")
async def portfolio_add(callback_query: CallbackQuery):
    await callback_query.answer()
    USER_STATE[callback_query.from_user.id] = "awaiting_portfolio_coin"
    await callback_query.message.edit_text(
        msg.PORTFOLIO_ADD_COIN,
        reply_markup=kb.back_home_keyboard(),
    )

async def handle_portfolio_coin(message: Message):
    uid = message.from_user.id
    if USER_STATE.get(uid) == "awaiting_portfolio_coin":
        coin = message.text.strip()
        info = api.search_coins(coin)
        if not info:
            await message.answer(
                msg.ALERT_ERROR, reply_markup=kb.back_home_keyboard()
            )
            return
        USER_DATA[uid] = info
        USER_STATE[uid] = "awaiting_portfolio_amount"
        await message.answer(
            msg.PORTFOLIO_ADD_AMOUNT.format(name=info["name"]),
            reply_markup=kb.back_home_keyboard(),
        )

async def handle_portfolio_amount(message: Message):
    uid = message.from_user.id
    if USER_STATE.get(uid) == "awaiting_portfolio_amount":
        try:
            amount = float(message.text.strip().replace(",", ""))
        except ValueError:
            await message.answer("Please enter a valid number.")
            return

        info = USER_DATA.get(uid)
        if not info:
            USER_STATE[uid] = None
            await message.answer(msg.ERROR_GENERIC)
            return

        p = api.get_price(info["id"])
        price = p.get("usd", 0) if p else 0
        value = amount * price

        db.add_holding(uid, info["id"], info["name"], info["symbol"], amount)
        USER_STATE[uid] = None
        USER_DATA.pop(uid, None)
        await message.answer(
            msg.PORTFOLIO_ADD_CONFIRM.format(
                amount=amount,
                symbol=info["symbol"].upper(),
                name=info["name"],
                value=value,
            ),
            reply_markup=kb.home_keyboard_colored(),
        )

@router.callback_query(F.data == "portfolio_remove")
async def portfolio_remove(callback_query: CallbackQuery):
    await callback_query.answer()
    uid = callback_query.from_user.id
    holdings = db.get_portfolio(uid)

    if not holdings:
        await callback_query.message.edit_text(
            msg.PORTFOLIO_EMPTY,
            reply_markup=kb.portfolio_keyboard(),
        )
        return

    buttons = []
    for i, h in enumerate(holdings):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"\u274c {h['coin_name']} ({h['amount']} {h['symbol'].upper()})",
                    callback_data=f"portfolio_remove_idx:{i}",
                )
            ]
        )
    buttons.append([InlineKeyboardButton(text="\u2190 Back", callback_data="portfolio")])
    await callback_query.message.edit_text(
        msg.PORTFOLIO_REMOVE_PROMPT,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )

@router.callback_query(F.data.startswith("portfolio_remove_idx:"))
async def portfolio_remove_idx(callback_query: CallbackQuery):
    await callback_query.answer()
    uid = callback_query.from_user.id
    idx = int(callback_query.data.split(":")[1])
    removed = db.remove_holding(uid, idx)
    if removed:
        await callback_query.message.edit_text(
            msg.PORTFOLIO_REMOVED.format(name=removed["coin_name"]),
            reply_markup=kb.back_home_keyboard(),
        )
    else:
        await callback_query.message.edit_text(
            msg.ERROR_GENERIC, reply_markup=kb.back_home_keyboard()
        )

@router.message(F.text)
async def handle_text(message: Message):
    uid = message.from_user.id
    state = USER_STATE.get(uid)

    if state == "awaiting_price":
        await handle_price_input(message)
    elif state == "awaiting_alert_coin":
        await handle_alert_coin(message)
    elif state == "awaiting_alert_target":
        await handle_alert_target(message)
    elif state == "awaiting_portfolio_coin":
        await handle_portfolio_coin(message)
    elif state == "awaiting_portfolio_amount":
        await handle_portfolio_amount(message)
    else:
        await message.answer(
            "Use the menu below to navigate 👇",
            reply_markup=kb.home_keyboard_colored(),
        )

@router.callback_query(F.data == "privacy")
@router.message(Command("privacy"))
async def privacy_cmd(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(
            msg.PRIVACY, reply_markup=kb.back_home_keyboard()
        )
    else:
        await event.answer(
            msg.PRIVACY, reply_markup=kb.back_home_keyboard()
        )

@router.callback_query(F.data == "terms")
@router.message(Command("terms"))
async def terms_cmd(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(
            msg.TERMS, reply_markup=kb.back_home_keyboard()
        )
    else:
        await event.answer(
            msg.TERMS, reply_markup=kb.back_home_keyboard()
        )

async def alert_checker(bot: Bot):
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
                            await bot.send_message(
                                uid,
                                msg.ALERT_TRIGGERED.format(
                                    name=a["coin_name"],
                                    symbol=a["symbol"].upper(),
                                    target=a["target"],
                                    price=current,
                                ),
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
