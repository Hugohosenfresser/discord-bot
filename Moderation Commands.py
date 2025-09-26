import discord
from discord.ext import commands
import logging
import sys

logger = logging.getLogger(__name__)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ------------------- Error Handling ------------------- #
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=discord.Embed(title="Command Not Found", description="This command does not exist.", color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing Permissions", description=f"You lack permissions: {', '.join(error.missing_permissions)}", color=discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing Argument", description=f"Missing required argument: {error.param.name}", color=discord.Color.red()))
        else:
            logger.error(f"Error in command {ctx.command}: {error}")
            await ctx.send(embed=discord.Embed(title="Unexpected Error", description="Something went wrong.", color=discord.Color.red()))

    # ------------------- Delete/Purge ------------------- #
    @commands.command(name='delete', aliases=['purge', 'clear'])
    @commands.has_permissions(manage_messages=True)
    async def delete_messages(self, ctx, amount: int, target: discord.Member = None):
        """Deletes messages. Usage: !delete <amount> [@user]"""
        if amount < 1 or amount > 100:
            return await ctx.send(embed=discord.Embed(title="Invalid Amount", description="Amount must be 1-100.", color=discord.Color.red()))
        def check_user(m): return target is None or m.author == target
        deleted_messages = await ctx.channel.purge(limit=amount + 1, check=check_user)
        deleted = len(deleted_messages) - 1 if target is None else len(deleted_messages)
        embed = discord.Embed(title="Messages Deleted", description=f"Deleted {deleted} messages.", color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=10)

    # ------------------- Role Add/Remove ------------------- #
    @commands.command(name='addrole')
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, *, role_name):
        """Adds a role to a user. Usage: !addrole @user <role_name>"""
        role = discord.utils.get(ctx.guild.roles, name=role_name) or discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)
        if not role: return await ctx.send(embed=discord.Embed(title="Role Not Found", description=f"{role_name} not found.", color=discord.Color.red()))
        if role.position >= ctx.guild.me.top_role.position: return await ctx.send(embed=discord.Embed(title="Permission Error", description="Cannot manage this role.", color=discord.Color.red()))
        if role in member.roles: return await ctx.send(embed=discord.Embed(title="Already Has Role", description=f"{member.display_name} already has {role.name}.", color=discord.Color.orange()))
        await member.add_roles(role, reason=f"Added by {ctx.author}")
        await ctx.send(embed=discord.Embed(title="Role Added", description=f"Added {role.name} to {member.display_name}.", color=discord.Color.green()))

    @commands.command(name='removerole')
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, *, role_name):
        """Removes a role from a user. Usage: !removerole @user <role_name>"""
        role = discord.utils.get(ctx.guild.roles, name=role_name) or discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)
        if not role: return await ctx.send(embed=discord.Embed(title="Role Not Found", description=f"{role_name} not found.", color=discord.Color.red()))
        if role.position >= ctx.guild.me.top_role.position: return await ctx.send(embed=discord.Embed(title="Permission Error", description="Cannot manage this role.", color=discord.Color.red()))
        if role not in member.roles: return await ctx.send(embed=discord.Embed(title="Role Not Assigned", description=f"{member.display_name} does not have {role.name}.", color=discord.Color.orange()))
        await member.remove_roles(role, reason=f"Removed by {ctx.author}")
        await ctx.send(embed=discord.Embed(title="Role Removed", description=f"Removed {role.name} from {member.display_name}.", color=discord.Color.green()))

    @commands.command(name='listroles')
    async def list_roles(self, ctx, member: discord.Member = None):
        """Lists roles in the server or for a specific user. Usage: !listroles [@user]"""
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
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))
