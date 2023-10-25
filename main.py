import argparse
import asyncio
import logging
import os

import aiogram
from dotenv import load_dotenv
from bot import handlers

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
                    filename='logs.log')


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    return parser.parse_args()


def read_token():
    load_dotenv()
    return os.environ['TOKEN']


async def main():
    token = read_token()
    bot = aiogram.Bot(token=token)
    try:
        dp = aiogram.Dispatcher(bot)
        handlers.load_context()
        handlers.setup_handlers(dp)
        await dp.start_polling()
    finally:
        handlers.close_context()
        await (await bot.get_session()).close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
