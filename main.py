import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from bot.handlers import router, alert_checker

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
dp.include_router(router)

async def on_startup(**kwargs):
    asyncio.create_task(alert_checker(bot))

async def main():
    dp.startup.register(on_startup)

    bot_info = await bot.get_me()
    logger.info("Bot started: @%s (ID: %s)", bot_info.username, bot_info.id)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
