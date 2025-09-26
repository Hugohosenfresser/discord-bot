import discord
from discord.ext import commands
import datetime

class Utility(commands.Cog):
    """A set of useful commands for general server utility and moderation."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Checks the bot's latency (response time)."""
        # Bot.latency is in seconds, multiply by 1000 for milliseconds
        latency_ms = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="Pong!",
            description=f"Latency is **{latency_ms}ms**.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name='say')
    async def say(self, ctx, *, message):
        """Makes the bot repeat a message. Requires Manage Messages permission."""
        try:
            # Delete the command message to make the output cleaner
            await ctx.message.delete()
        except discord.Forbidden:
            # Handle cases where the bot cannot delete messages (e.g., missing permissions)
            pass 
        
        await ctx.send(message)

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="You need the **Manage Messages** permission to use the `!say` command.", 
                color=discord.Color.red()
            ), delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description="Usage: `!say <message>`", 
                color=discord.Color.red()
            ), delete_after=10)

    @commands.command(name='userinfo', aliases=['ui', 'whois'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Shows detailed information about a user."""
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"User Info: {member.display_name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.teal(),
            timestamp=datetime.datetime.now()
        )
        
        # Determine account age
        created_at = member.created_at.strftime("%b %d, %Y %I:%M %p UTC")
        joined_at = member.joined_at.strftime("%b %d, %Y %I:%M %p UTC")
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Mention", value=member.mention, inline=True)
        embed.add_field(name="Bot?", value="Yes" if member.bot else "No", inline=True)
        embed.add_field(name="Account Created", value=created_at, inline=False)
        embed.add_field(name="Joined Server", value=joined_at, inline=False)
        
        # Get roles (excluding @everyone) and format them
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        roles_text = ", ".join(roles) if roles else "None"
        embed.add_field(name=f"Roles ({len(roles)})", value=roles_text, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='clear', aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Deletes a specified number of messages in the channel. Requires Manage Messages permission."""
        if amount <= 0:
            return await ctx.send(embed=discord.Embed(
                description="You must delete at least 1 message.", 
                color=discord.Color.red()
            ), delete_after=10)

        # Delete the number of messages specified + 1 (for the command message itself)
        deleted = await ctx.channel.purge(limit=amount + 1)
        
        # Send confirmation message
        await ctx.send(embed=discord.Embed(
            description=f"Successfully cleared **{len(deleted) - 1}** messages.",
            color=discord.Color.green()
        ), delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="You need the **Manage Messages** permission to clear messages.", 
                color=discord.Color.red()
            ), delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description="Usage: `!clear <number_of_messages>`", 
                color=discord.Color.red()
            ), delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(
                description="The amount must be a whole number.", 
                color=discord.Color.red()
            ), delete_after=10)


async def setup(bot):
    await bot.add_cog(Utility(bot))