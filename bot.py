import os
import discord
from discord.ext import commands

# Load the environment variables
# You can use a library like `python-dotenv` for this, or just `os.environ`
# bot_token = os.environ.get('BOT_TOKEN') # Assuming a `BOT_TOKEN` is set in your environment
# Here is a placeholder for the bot token
bot_token = 'YOUR_BOT_TOKEN_HERE' 

# Define the command prefix
# It will first check for an environment variable, then fall back to '!'
command_prefix = os.environ.get('COMMAND_PREFIX', '!')

# Set the bot's intents. Intents specify which events the bot will receive.
# For most commands, you'll need at least `Intents.message_content`.
intents = discord.Intents.default()
intents.message_content = True # Required to read messages and command arguments
intents.members = True # Required for member-related events and fetching member info
intents.guilds = True # Required for guild-related events and fetching guild info

# Create the bot instance
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# List the cogs you want to load. The names should match the file names without the `.py` extension.
initial_extensions = [
    'Admin Commands',
    'Core Commands',
    'Doakes and Help',
    'Gambling',
    'Moderation Commands',
]

@bot.event
async def on_ready():
    """This event is called when the bot has successfully connected to Discord."""
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    # Load the cogs when the bot is ready
    for extension in initial_extensions:
        try:
            # Load the extension (the cog file)
            await bot.load_extension(extension.replace(" ", "")) # Remove space from filename
            print(f'Successfully loaded extension: {extension}')
        except Exception as e:
            # If a cog fails to load, print the error
            print(f'Failed to load extension {extension}.')
            print(f'{e}')

# Run the bot with the token
bot.run(bot_token)
