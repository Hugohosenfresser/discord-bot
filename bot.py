import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX', '!')

# Set up bot intents (permissions)
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.watching, name="for commands")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    """Event triggered when a message is sent"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Log messages (optional - remove in production if not needed)
    print(f'Message from {message.author}: {message.content}')
    
    # Process commands
    await bot.process_commands(message)

@bot.command(name='hello')
async def hello(ctx):
    """Say hello to the user"""
    await ctx.send(f'Hello {ctx.author.mention}! 👋')

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! 🏓 Latency: {latency}ms')

@bot.command(name='info')
async def info(ctx):
    """Display bot information"""
    embed = discord.Embed(
        title="Bot Information",
        color=discord.Color.blue()
    )
    embed.add_field(name="Bot Name", value=bot.user.name, inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Prefix", value=PREFIX, inline=True)
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    
    await ctx.send(embed=embed)

@bot.command(name='say')
async def say(ctx, *, message):
    """Make the bot repeat a message"""
    # Delete the original command message
    await ctx.message.delete()
    # Send the repeated message
    await ctx.send(message)

@bot.command(name='userinfo')
async def user_info(ctx, member: discord.Member = None):
    """Get information about a user"""
    if member is None:
        member = ctx.author
    
    embed = discord.Embed(
        title=f"User Info - {member.display_name}",
        color=member.color
    )
    embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required argument. Check the command usage with `!help <command>`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided. Check the command usage with `!help <command>`")
    else:
        print(f'An error occurred: {error}')
        await ctx.send("❌ An unexpected error occurred.")

# Run the bot
if __name__ == '__main__':
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found in environment variables.")
        print("Please create a .env file with your bot token.")
        exit(1)
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Error: Invalid bot token. Please check your DISCORD_TOKEN in the .env file.")
    except Exception as e:
        print(f"Error starting bot: {e}")