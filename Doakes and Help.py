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
            "https://c.tenor.com/f9qW6yR6iL4AAAAC/tenor.gif",
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
        
        # --- Define commands by category for better organization ---
        # Note: Commands are based on the previous conversation context (Gambling, Utility Cogs)
        command_categories = {
            "General Commands": {
                "ping": "Check the bot's latency (response time).",
                "say": "Make the bot repeat a message. (Requires Manage Messages)",
                "userinfo": "Get detailed information about a user. `!userinfo [@user]`",
                "doakes": "Send a random Sergeant Doakes GIF and quote.",
            },
            "Economy Commands": {
                "balance": "Check your current currency balance.",
                "daily": "Claim your daily bonus (every 24h).",
                "roll": "Play a dice game and bet. `!roll <amount>`",
            },
            "Moderation Commands": {
                "clear": "Deletes messages. `!clear <amount>` (Requires Manage Messages)",
                "setbalance": "[Admin Only] Set a user's balance. `!setbalance @user <amount>`",
            }
        }
        
        # Helper dictionary to find detailed info easily
        all_commands_info = {}
        for category, commands_list in command_categories.items():
            all_commands_info.update(commands_list)

        # --- Help command implementation ---

        if command_name:
            # Detailed help for a single command
            cmd_info = all_commands_info.get(command_name.lower())
            
            if cmd_info:
                embed = discord.Embed(
                    title=f"Command: {command_name.title()}",
                    description=cmd_info,
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="Command Not Found",
                    description=f"No detailed help available for `{command_name}`. Try using `!help` to see all commands.",
                    color=discord.Color.red()
                )
        else:
            # List all commands (General Help)
            embed = discord.Embed(
                title="Bot Command List",
                description="Here are all the available commands, grouped by category. The prefix is `!`.",
                color=discord.Color.blurple() # A visually appealing color
            )
            
            # Add fields for each category
            for category, commands_list in command_categories.items():
                command_lines = []
                for cmd, desc in commands_list.items():
                    # Format: **!cmd**: description
                    command_lines.append(f"**`!{cmd}`**: {desc}")
                
                # Join lines and add as a non-inline field for a list effect
                embed.add_field(
                    name=f"--- {category} ---", 
                    value="\n".join(command_lines), 
                    inline=False
                )
            
            embed.set_footer(text=f"Use !help <command> for detailed usage information (e.g., !help roll).")
            # Set the bot's profile picture as a thumbnail
            if self.bot.user and self.bot.user.display_avatar:
                 embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Misc(bot))