import random
import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='doakes')
    async def doakes(self, ctx):
        """Sends a random Sergeant Doakes GIF and quote."""
        doakes_gifs = [
            "https://c.tenor.com/EqPfcX1wzHoAAAAd/tenor.gif",
            "https://c.tenor.com/x7XtuEuhFqEAAAAd/tenor.gif",
            "https://c.tenor.com/f9qW6yR6iL4AAAAC/tenor.gif", # This is the corrected URL
        ]
        doakes_quotes = ["I will touch you.", "ughhhh 😳", "I like men :3"]
        selected_gif = random.choice(doakes_gifs)
        selected_quote = random.choice(doakes_quotes)
        embed = discord.Embed(title="Sergeant Doakes", description=f"*{selected_quote}*", color=discord.Color.dark_red())
        embed.set_image(url=selected_gif)
        embed.set_footer(text=f"Requested by {ctx.author.display_name} | From Dexter TV Series", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='help')
    async def help_command(self, ctx, command_name: str = None):
        """Show a list of commands or detailed info for a specific command."""
        
        embed = discord.Embed(
            title="Bot Commands",
            color=discord.Color.blue()
        )
        
        # Command descriptions
        commands_info = {
            "hello": "Say hello to the bot.",
            "ping": "Check bot latency.",
            "info": "Display bot information.",
            "say": "Make the bot repeat a message. Usage: !say <message>",
            "doakes": "Send a random Sergeant Doakes GIF.",
            "userinfo": "Get detailed information about a user. Usage: !userinfo [@user]",
            "balance": "Check your current gambling balance.",
            "daily": "Claim your daily gambling bonus.",
            "roll": "Play a dice game and bet. Usage: !roll <amount>",
            "delete": "Delete messages. Usage: !delete <amount> [@user]",
            "addrole": "Add a role to a user. Usage: !addrole @user <role_name>",
            "removerole": "Remove a role from a user. Usage: !removerole @user <role_name>",
            "listroles": "List roles in the server or for a specific user. Usage: !listroles [@user]"
        }
        
        if command_name:
            # Detailed help for a single command
            cmd_info = commands_info.get(command_name.lower())
            if cmd_info:
                embed.title = f"Help - {command_name}"
                embed.description = cmd_info
            else:
                embed.title = "Command Not Found"
                embed.description = f"No help available for `{command_name}`"
        else:
            # List all commands
            for cmd, desc in commands_info.items():
                embed.add_field(name=f"`{self.bot.command_prefix}{cmd}`", value=desc, inline=False)
            
            embed.set_footer(text=f"Use {self.bot.command_prefix}help <command> for more info on a command.")
        
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Misc(bot))
