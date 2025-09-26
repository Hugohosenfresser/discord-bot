import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ------------------- Logging ------------------- #
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ------------------- Environment ------------------- #
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX', '!')
try:
    BACK_ACCESS_USER_ID = int(os.getenv("BACK_ACCESS_USER_ID", "0"))
except ValueError:
    BACK_ACCESS_USER_ID = 0

# ------------------- Intents ------------------- #
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents, help_command=None)
        self.back_access_user_id = BACK_ACCESS_USER_ID
    
    async def setup_hook(self):
        # Load cogs
        cogs_to_load = ['core', 'moderation', 'admin', 'gambling']
        for cog in cogs_to_load:
            try:
                await self.load_extension(f'cogs.{cog}')
                logger.info(f'Loaded cog: {cog}')
            except Exception as e:
                logger.error(f'Failed to load cog {cog}: {e}')

    async def on_ready(self):
        logger.info(f'{self.user} connected!')
        logger.info(f'Bot is in {len(self.guilds)} guilds.')
        activity = discord.Activity(type=discord.ActivityType.watching, name="for commands")
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

# ------------------- Run Bot ------------------- #
if __name__ == '__main__':
    if not TOKEN:
        logger.error("DISCORD_TOKEN not found!")
        sys.exit(1)
    
    bot = MyBot()
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid bot token.")
        sys.exit(1)
