import discord

from cogs import EconomyCog
from discord.ext import commands
from cogs.economy_folder.utils import multiplier_calculator


class Multipliers(EconomyCog):
    @commands.command(name='multi', aliases=['multipliers', 'multis'])
    async def multi(self, ctx):
        em = await self.create_embed(
            title=f'{ctx.author.name}\'s multipliers',
            description=f'Your total multiplier: {await multiplier_calculator(ctx.author)}%',
            colour=discord.Colour.random()
        )
        return await ctx.send(embed=em)


def multi(bot):
    bot.add_cog(Multipliers(bot))
