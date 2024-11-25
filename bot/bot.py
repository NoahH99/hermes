import asyncio
import logging

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from config import Config
from extention_loader import load_extensions

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hermes")

config = Config()
config.validate()

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config.command_prefix, intents=intents)

bot.config = config

@bot.event
async def on_ready():
    logger.info(f"Bot connected as {bot.user}")


async def main():
    await load_extensions(bot)
    await bot.start(config.bot_token)


if __name__ == "__main__":
    asyncio.run(main())
