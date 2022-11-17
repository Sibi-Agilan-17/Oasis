import discord

from cogs import EconomyCog
from discord.ext import commands


class Balance(EconomyCog):
    @commands.command(name='bal', aliases=['balance', 'coins', 'cash'])
    async def bal(self, ctx, *, member: discord.Member = None):
        user = member or ctx.author
        balance = await self.get_balance_as_embed(user)
        return await ctx.send(embed=balance)


def bal(bot):
    bot.add_cog(Balance(bot))
