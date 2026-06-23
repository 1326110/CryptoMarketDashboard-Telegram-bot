import asyncio
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from config import BOT_TOKEN
from bot.handlers import (
    start,
    home,
    help_cmd,
    howto,
    price_command,
    alert_command,
    price_prompt,
    price_coin_quick,
    top_coins,
    alerts_menu,
    alert_new,
    alert_remove,
    alert_example,
    portfolio_menu,
    portfolio_example,
    portfolio_add,
    portfolio_remove,
    portfolio_remove_idx,
    handle_text,
    privacy_cmd,
    terms_cmd,
    alert_checker,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def post_init(app):
    asyncio.create_task(alert_checker(app))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("privacy", privacy_cmd))
    app.add_handler(CommandHandler("terms", terms_cmd))
    app.add_handler(CommandHandler("alert", alert_command))
    app.add_handler(CallbackQueryHandler(home, pattern="^home$"))
    app.add_handler(CallbackQueryHandler(help_cmd, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(howto, pattern="^howto$"))
    app.add_handler(CallbackQueryHandler(privacy_cmd, pattern="^privacy$"))
    app.add_handler(CallbackQueryHandler(terms_cmd, pattern="^terms$"))
    app.add_handler(CallbackQueryHandler(price_prompt, pattern="^price$"))
    app.add_handler(CallbackQueryHandler(price_coin_quick, pattern=r"^price_coin:"))
    app.add_handler(CallbackQueryHandler(top_coins, pattern="^top$"))
    app.add_handler(CallbackQueryHandler(alerts_menu, pattern="^alerts$"))
    app.add_handler(CallbackQueryHandler(alert_new, pattern="^alert_new$"))
    app.add_handler(CallbackQueryHandler(alert_remove, pattern=r"^alert_remove:"))
    app.add_handler(CallbackQueryHandler(alert_example, pattern="^alert_example$"))
    app.add_handler(CallbackQueryHandler(portfolio_menu, pattern="^portfolio$"))
    app.add_handler(CallbackQueryHandler(portfolio_add, pattern="^portfolio_add$"))
    app.add_handler(CallbackQueryHandler(portfolio_remove, pattern="^portfolio_remove$"))
    app.add_handler(CallbackQueryHandler(portfolio_example, pattern="^portfolio_example$"))
    app.add_handler(
        CallbackQueryHandler(portfolio_remove_idx, pattern=r"^portfolio_remove_idx:")
    )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    async def error_handler(update, context):
        logger.error("Unhandled error: %s", context.error)
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Something went wrong. Please try again.",
            )
    app.add_error_handler(error_handler)

    print("MarketPulse bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
