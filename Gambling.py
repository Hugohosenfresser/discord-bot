import random
import discord
from discord.ext import commands

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = {}  # User balances stored in memory.

    # ------------------- Utility Functions ------------------- #
    def get_balance(self, user_id):
        """Retrieves a user's balance, creating one if it doesn't exist."""
        if user_id not in self.balances:
            self.balances[user_id] = 100  # Starting balance
        return self.balances[user_id]
        
    def add_balance(self, user_id, amount):
        """Adds an amount to a user's balance."""
        if user_id not in self.balances:
            self.balances[user_id] = 100
        self.balances[user_id] += amount
    
    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx):
        """Checks your current currency balance."""
        user_id = ctx.author.id
        bal = self.get_balance(user_id)
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Balance",
            description=f"You have **{bal}** coins.",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name='daily')
    @commands.cooldown(1, 86400, commands.BucketType.user)  # 24-hour cooldown
    async def daily(self, ctx):
        """Claims your daily bonus of 100 coins."""
        user_id = ctx.author.id
        self.add_balance(user_id, 100)
        embed = discord.Embed(
            title="Daily Bonus Claimed!",
            description="You received **100** coins. Come back in 24 hours!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining = round(error.retry_after)
            hours, rem = divmod(remaining, 3600)
            minutes, seconds = divmod(rem, 60)
            await ctx.send(f"You can claim your daily bonus again in **{hours}h {minutes}m {seconds}s**.", delete_after=10)

    @commands.command(name='roll', aliases=['dice'])
    async def roll(self, ctx, bet: int):
        """Rolls a dice and bets on the outcome. Win double or lose your bet."""
        user_id = ctx.author.id
        bal = self.get_balance(user_id)

        if bet <= 0:
            return await ctx.send(embed=discord.Embed(description="You must bet a positive amount.", color=discord.Color.red()))
        
        if bet > bal:
            return await ctx.send(embed=discord.Embed(description="You don't have enough coins to place that bet.", color=discord.Color.red()))
            
        roll = random.randint(1, 6)
        
        if roll in [1, 2, 3]:
            # Lose
            self.add_balance(user_id, -bet)
            result = "You lost!"
            color = discord.Color.red()
            new_bal = self.get_balance(user_id)
            desc = f"You rolled a **{roll}**.\nYou lost **{bet}** coins.\nYour new balance is **{new_bal}** coins."
        else:
            # Win
            winnings = bet * 2
            self.add_balance(user_id, winnings)
            result = "You won!"
            color = discord.Color.green()
            new_bal = self.get_balance(user_id)
            desc = f"You rolled a **{roll}**.\nYou won **{winnings}** coins!\nYour new balance is **{new_bal}** coins."
            
        embed = discord.Embed(title=f"Dice Roll: {result}", description=desc, color=color)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Gambling(bot))
