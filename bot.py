import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.watching, name="for commands")
    await bot.change_presence(activity=activity)
    logger.info('Bot status set and ready to receive commands')

@bot.event
async def on_message(message):
    """Event triggered when a message is sent"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Log messages for debugging (Railway-friendly)
    logger.debug(f'Message from {message.author}: {message.content[:50]}...')
    
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
    """Get detailed information about a user"""
    if member is None:
        member = ctx.author
    
    # Create embed with user's color or default blue
    embed = discord.Embed(
        title=f"📋 User Information",
        description=f"Information for {member.mention}",
        color=member.color if member.color != discord.Color.default() else discord.Color.blue()
    )
    
    # Basic user info
    embed.add_field(
        name="👤 Username", 
        value=f"{member.name}#{member.discriminator}", 
        inline=False
    )
    
    embed.add_field(
        name="🆔 User ID", 
        value=f"`{member.id}`", 
        inline=False
    )
    
    embed.add_field(
        name="📛 Display Name", 
        value=member.display_name, 
        inline=False
    )
    
    embed.add_field(
        name="🟢 Status", 
        value=str(member.status).title().replace('Dnd', 'Do Not Disturb'), 
        inline=False
    )
    
    # Dates with Discord timestamps
    if member.joined_at:
        joined_timestamp = int(member.joined_at.timestamp())
        embed.add_field(
            name="📅 Joined Server", 
            value=f"<t:{joined_timestamp}:F>\n<t:{joined_timestamp}:R>", 
            inline=False
        )
    
    created_timestamp = int(member.created_at.timestamp())
    embed.add_field(
        name="🎂 Account Created", 
        value=f"<t:{created_timestamp}:F>\n<t:{created_timestamp}:R>", 
        inline=False
    )
    
    # User roles (excluding @everyone)
    roles = [role for role in member.roles if role.name != "@everyone"]
    if roles:
        # Sort roles by position (highest first)
        roles.sort(key=lambda x: x.position, reverse=True)
        
        # Create role list with mentions
        role_list = [role.mention for role in roles]
        
        # Split roles into chunks if too many (Discord has embed limits)
        if len(role_list) > 20:
            role_text = ", ".join(role_list[:20]) + f"\n... and {len(role_list) - 20} more"
        else:
            role_text = ", ".join(role_list)
        
        embed.add_field(
            name=f"🎭 Roles ({len(roles)})", 
            value=role_text if role_text else "No roles", 
            inline=False
        )
    else:
        embed.add_field(
            name="🎭 Roles (0)", 
            value="No roles", 
            inline=False
        )
    
    # Set thumbnail to user's avatar
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    else:
        embed.set_thumbnail(url=member.default_avatar.url)
    
    # Footer with additional info
    embed.set_footer(
        text=f"Requested by {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    )
    
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
        logger.error(f'Unexpected error in command {ctx.command}: {error}')
        await ctx.send("❌ An unexpected error occurred.")

# Run the bot
if __name__ == '__main__':
    if TOKEN is None:
        logger.error("DISCORD_TOKEN not found in environment variables.")
        logger.error("Please set your bot token in Railway environment variables.")
        sys.exit(1)
    
    try:
        logger.info("Starting Discord bot...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid bot token. Please check your DISCORD_TOKEN environment variable.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error starting bot: {e}")
        sys.exit(1)
