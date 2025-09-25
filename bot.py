import os
import sys
import logging
import random
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

# Create bot instance (remove default help command to add custom one)
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

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
    embed = discord.Embed(
        title="Hello!",
        description=f"Hello {ctx.author.mention}! Welcome to the server!",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_footer(text="Thanks for using the bot!")
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    
    # Color based on latency
    if latency < 100:
        color = discord.Color.green()
        status = "Excellent"
    elif latency < 200:
        color = discord.Color.yellow()
        status = "Good"
    else:
        color = discord.Color.red()
        status = "High"
    
    embed = discord.Embed(
        title="Pong!",
        color=color
    )
    embed.add_field(
        name="Latency",
        value=f"`{latency}ms`",
        inline=True
    )
    embed.add_field(
        name="Status",
        value=status,
        inline=True
    )
    embed.set_footer(text="Bot response time")
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    """Display bot information"""
    embed = discord.Embed(
        title="Bot Information",
        description="Information about this Discord bot",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Bot Name", 
        value=f"`{bot.user.name}`", 
        inline=False
    )
    
    embed.add_field(
        name="Servers", 
        value=f"`{len(bot.guilds)}` servers", 
        inline=True
    )
    
    embed.add_field(
        name="Command Prefix", 
        value=f"`{PREFIX}`", 
        inline=True
    )
    
    # Count total users across all guilds
    total_users = sum(guild.member_count for guild in bot.guilds if guild.member_count)
    embed.add_field(
        name="Total Users", 
        value=f"`{total_users:,}`", 
        inline=True
    )
    
    embed.add_field(
        name="Invite Bot", 
        value="[Click here to invite me!](https://discord.com/developers/applications)", 
        inline=False
    )
    
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
    embed.set_footer(
        text=f"Bot ID: {bot.user.id} | Made with discord.py",
        icon_url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url
    )
    
    await ctx.send(embed=embed)

@bot.command(name='say')
async def say(ctx, *, message):
    """Make the bot repeat a message"""
    try:
        # Delete the original command message
        await ctx.message.delete()
        
        # Create embed for the message
        embed = discord.Embed(
            description=message,
            color=discord.Color.purple()
        )
        embed.set_author(
            name=f"Message from {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        embed.set_footer(text="Sent via bot")
        
        await ctx.send(embed=embed)
    except discord.Forbidden:
        # If can't delete message, send without deleting
        embed = discord.Embed(
            description=message,
            color=discord.Color.purple()
        )
        embed.set_author(
            name=f"Message from {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        embed.set_footer(text="Sent via bot")
        
        await ctx.send(embed=embed)

@bot.command(name='doakes')
async def doakes(ctx):
    """Send a random Sergeant Doakes GIF from Dexter"""
    
    # List of Doakes GIFs from Dexter
    doakes_gifs = [
        "https://images-ext-1.discordapp.net/external/W0HpZimDJ0l-tY2lClrLVP_CM1aYOWst0YoCzE10iU4/https/media.tenor.com/q8o8tyY9_HsAAAPo/watching-you.mp4",
        "https://tenor.com/view/james-doakes-doakes-curious-suspicious-questioning-gif-14390669560130901665",
        "https://tenor.com/view/doakes-bar-gif-4298875606784040546",
        "https://tenor.com/view/dexter-doakes-squint-stare-suspicious-gif-14432154109786838518",
        "https://tenor.com/view/doakes-dexter-dexter-doakes-gotcha-found-you-gif-14688017774431904057",
        "https://tenor.com/view/dexter-james-doakes-erik-king-stare-staring-gif-1343162792415382650",
    ]
    
    # Doakes quotes
    doakes_quotes = [
        "I will touch you.",
        "ughhhh 😳",
        "I like men :3"
    ]
    
    # Select random GIF and quote
    selected_gif = random.choice(doakes_gifs)
    selected_quote = random.choice(doakes_quotes)
    
    embed = discord.Embed(
        title="Sergeant Doakes",
        description=f"*{selected_quote}*",
        color=discord.Color.dark_red()
    )
    
    embed.set_image(url=selected_gif)
    embed.set_footer(
        text=f"Requested by {ctx.author.display_name} | From Dexter TV Series",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    )
    
    await ctx.send(embed=embed)

@bot.command(name='userinfo')
async def user_info(ctx, member: discord.Member = None):
    """Get detailed information about a user"""
    if member is None:
        member = ctx.author
    
    # Create embed with user's color or default blue
    embed = discord.Embed(
        title=f"User Information",
        description=f"Information for {member.mention}",
        color=member.color if member.color != discord.Color.default() else discord.Color.blue()
    )
    
    # Basic user info
    embed.add_field(
        name="Username", 
        value=f"{member.name}#{member.discriminator}", 
        inline=False
    )
    
    embed.add_field(
        name="User ID", 
        value=f"`{member.id}`", 
        inline=False
    )
    
    embed.add_field(
        name="Display Name", 
        value=member.display_name, 
        inline=False
    )
    
    # Fix status display
    status_map = {
        'online': 'Online',
        'offline': 'Offline', 
        'idle': 'Idle',
        'dnd': 'Do Not Disturb',
        'invisible': 'Invisible'
    }
    status_display = status_map.get(str(member.status), str(member.status).title())
    
    embed.add_field(
        name="Status", 
        value=status_display, 
        inline=False
    )
    
    # Dates with Discord timestamps
    if member.joined_at:
        joined_timestamp = int(member.joined_at.timestamp())
        embed.add_field(
            name="Joined Server", 
            value=f"<t:{joined_timestamp}:F>\n<t:{joined_timestamp}:R>", 
            inline=False
        )
    
    created_timestamp = int(member.created_at.timestamp())
    embed.add_field(
        name="Account Created", 
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
            name=f"Roles ({len(roles)})", 
            value=role_text if role_text else "No roles", 
            inline=False
        )
    else:
        embed.add_field(
            name="Roles (0)", 
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

@bot.command(name='delete', aliases=['purge', 'clear'])
@commands.has_permissions(manage_messages=True)
async def delete_messages(ctx, amount: int, target: discord.Member = None):
    """Delete messages from the channel. Optionally target a specific user."""
    
    # Validate amount
    if amount < 1:
        embed = discord.Embed(
            title="Invalid Amount",
            description="You must specify at least 1 message to delete.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    if amount > 100:
        embed = discord.Embed(
            title="Amount Too Large",
            description="You can only delete up to 100 messages at once.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    try:
        deleted = 0
        
        if target is None:
            # Delete messages from anyone
            deleted_messages = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
            deleted = len(deleted_messages) - 1  # -1 to exclude the command message
        else:
            # Delete messages from specific user
            def check_user(message):
                return message.author == target
            
            # Delete the command message first
            await ctx.message.delete()
            
            # Then purge messages from the target user
            deleted_messages = await ctx.channel.purge(limit=amount, check=check_user)
            deleted = len(deleted_messages)
        
        # Create confirmation embed
        embed = discord.Embed(
            title="Messages Deleted",
            color=discord.Color.green()
        )
        
        if target is None:
            embed.description = f"Successfully deleted {deleted} messages."
        else:
            embed.description = f"Successfully deleted {deleted} messages from {target.display_name}."
        
        embed.add_field(
            name="Deleted by",
            value=ctx.author.mention,
            inline=True
        )
        
        embed.add_field(
            name="Channel",
            value=ctx.channel.mention,
            inline=True
        )
        
        embed.set_footer(text="This message will be deleted in 10 seconds")
        
        # Send confirmation and delete it after 10 seconds
        confirmation = await ctx.send(embed=embed)
        await confirmation.delete(delay=10)
        
    except discord.Forbidden:
        embed = discord.Embed(
            title="Missing Permissions",
            description="I don't have permission to delete messages in this channel.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    except discord.HTTPException as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred while deleting messages: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@delete_messages.error
async def delete_error(ctx, error):
    """Handle errors for the delete command"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Missing Permissions",
            description="You need the `Manage Messages` permission to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Invalid Argument",
            description="Please provide a valid number and optionally mention a user.\n\nUsage: `!delete <amount> [@user]`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx, command_name=None):
    """Display help information for commands"""
    
    if command_name is None:
        # Show all commands
        embed = discord.Embed(
            title="Help - Available Commands",
            description=f"Here are all the commands you can use! Use `{PREFIX}help <command>` for detailed info.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="General Commands",
            value=f"`{PREFIX}hello` - Say hello\n`{PREFIX}ping` - Check bot latency\n`{PREFIX}info` - Bot information",
            inline=False
        )
        
        embed.add_field(
            name="User Commands",
            value=f"`{PREFIX}userinfo [@user]` - Get detailed user info",
            inline=False
        )
        
        embed.add_field(
            name="Utility Commands",
            value=f"`{PREFIX}say <message>` - Make the bot repeat a message",
            inline=False
        )
        
        embed.add_field(
            name="Fun Commands",
            value=f"`{PREFIX}doakes` - Get a random Sergeant Doakes GIF from Dexter",
            inline=False
        )
        
        embed.add_field(
            name="Moderation Commands",
            value=f"`{PREFIX}delete <amount> [@user]` - Delete messages (requires Manage Messages permission)",
            inline=False
        )
        
        embed.set_footer(
            text=f"Bot Prefix: {PREFIX} | Use {PREFIX}help <command> for more details",
            icon_url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url
        )
        
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
        
    else:
        # Show specific command help
        command = bot.get_command(command_name)
        
        if command is None:
            embed = discord.Embed(
                title="Command Not Found",
                description=f"No command named `{command_name}` found.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Use {PREFIX}help to see all commands")
        else:
            embed = discord.Embed(
                title=f"Help - {command.name}",
                description=command.help or "No description available.",
                color=discord.Color.green()
            )
            
            # Add usage information
            signature = f"{PREFIX}{command.name}"
            if command.signature:
                signature += f" {command.signature}"
            
            embed.add_field(
                name="Usage",
                value=f"`{signature}`",
                inline=False
            )
            
            # Add aliases if any
            if command.aliases:
                embed.add_field(
                    name="Aliases",
                    value=", ".join([f"`{alias}`" for alias in command.aliases]),
                    inline=False
                )
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors with styled embeds"""
    
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Command Not Found",
            description=f"The command you tried doesn't exist.\nUse `{PREFIX}help` to see available commands.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Double-check your spelling!")
        await ctx.send(embed=embed)
        
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Missing Argument",
            description=f"You're missing a required argument for this command.\nUse `{PREFIX}help {ctx.command}` for usage information.",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="Missing Argument",
            value=f"`{error.param.name}`",
            inline=True
        )
        await ctx.send(embed=embed)
        
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Invalid Argument",
            description=f"One of your arguments is invalid.\nUse `{PREFIX}help {ctx.command}` for usage information.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Make sure you're using the right format!")
        await ctx.send(embed=embed)
        
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Command on Cooldown",
            description=f"Please wait **{error.retry_after:.1f} seconds** before using this command again.",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Missing Permissions",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Required Permissions",
            value=", ".join(error.missing_permissions),
            inline=False
        )
        await ctx.send(embed=embed)
        
    else:
        logger.error(f'Unexpected error in command {ctx.command}: {error}')
        embed = discord.Embed(
            title="Unexpected Error",
            description="Something went wrong while processing your command.\nThis has been logged for review.",
            color=discord.Color.red()
        )
        embed.set_footer(text="If this persists, please contact the bot developer.")
        await ctx.send(embed=embed)

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
