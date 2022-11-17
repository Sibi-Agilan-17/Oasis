import discord

from cogs import EconomyCog
from discord.ext import commands


class Level(EconomyCog):
    @commands.command(name='level')
    async def level(self, ctx, *, member: discord.Member = None):
        user = member or ctx.author
        level = await self.get_level_as_embed(user)
        return await ctx.send(embed=level)


def level(bot):
    bot.add_cog(Level(bot))
