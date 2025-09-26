import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the bot token from the environment variable.
# This is a much safer way to handle your token than hardcoding it.
bot_token = os.getenv('DISCORD_TOKEN')

# Define the command prefix
# It will first check for an environment variable, then fall back to '!'
command_prefix = os.environ.get('COMMAND_PREFIX', '!')

# Set the bot's intents.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Create the bot instance
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# List the cogs to load, using the actual file names (without the .py extension).
# Based on the project structure image, these are the correct module names:
initial_extensions = [
    'core_commands',
    'doakes_help',
    'gambling',
    'moderation_commands',
    # Ensure 'Admin Commands' is loaded if you created it for the setbalance command
    'admin_commands' 
]

@bot.event
async def on_ready():
    """This event is called when the bot has successfully connected to Discord."""
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    # Load the cogs when the bot is ready
    for extension in initial_extensions:
        try:
            # We use the extension name directly, spaces and all, as it matches the filename
            await bot.load_extension(extension)
            print(f'Successfully loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            print(f'{e}')

# Run the bot with the token. If the token isn't found, it will print an error.
if not bot_token:
    print("Error: DISCORD_TOKEN not found in environment variables.")
else:
    bot.run(bot_token)
