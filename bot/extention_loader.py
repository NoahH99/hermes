import importlib
import logging
import os

from discord.ext.commands import Bot

logger = logging.getLogger("extension.loader")


async def load_extensions(bot: Bot, cogs_directory: str = "cogs"):
    """
    Dynamically load all cogs from the specified directory into the bot.

    :param bot: The instance of the bot where extensions will be loaded.
    :param cogs_directory: The relative directory to scan for cog files.
    """
    cogs_dir = os.path.join(os.path.dirname(__file__), cogs_directory)

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            extension = f"{cogs_directory}.{filename[:-3]}"

            try:
                module = importlib.import_module(extension)
                if not hasattr(module, "setup"):
                    raise ImportError(f"Cog '{extension}' does not have a setup function.")

                await bot.load_extension(extension)
                logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")
