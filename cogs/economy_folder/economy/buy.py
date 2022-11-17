import discord

from cogs import EconomyCog
from discord.ext import commands
from cogs.economy_folder.utils.shop import *


class Buy(EconomyCog):
    @commands.command(name='buy')
    async def buy(self, ctx, item, amount=1):
        try:
            int(amount)
        except TypeError or ValueError:
            return await ctx.send(embed=await self.error(description='Invalid amount provided!'))

        if amount < 0:
            return await ctx.send(embed=await self.error(description='Invalid amount provided!'))

        if item in ['commongem', 'common', 'cgem']:
            i_name = 'common_gem'
            i = common_gem

        elif item in ['uncommongem', 'uncommon', 'ucgem', 'ugem']:
            i_name = 'uncommon_gem'
            i = uncommon_gem

        elif item in ['raregem', 'rare', 'rgem']:
            i_name = 'rare_gem'
            i = rare_gem

        elif item in ['epicgem', 'epic', 'egem']:
            i_name = 'epic_gem'
            i = epic_gem

        elif item in ['goldengem', 'golden', 'ggem']:
            i_name = 'golden_gem'
            i = golden_gem

        elif item in ['diamondgem', 'diamond', 'dgem']:
            i_name = 'diamond_gem'
            i = diamond_gem

        elif item in ['legendarygem', 'legendary', 'lgem']:
            i_name = 'legendary_gem'
            i = legendary_gem
        else:
            return await ctx.send(embed=await self.error(description='Invalid item provided!'))

        i_price = i.buy_price

        bal = await self.get_balance_for(ctx.author)
        if int(bal) < int((i_price * amount)):
            return await ctx.send(embed=await self.error(description='You don\'t have enough cash!'))

        await self.add_coins(ctx.author, (-1 * (i_price * amount)))
        await self.add_item(ctx.author, i_name, amount)

        em = discord.Embed(
            title='Purchase successful!',
            description=f'{ctx.author} just bought `{amount:,}` {i.name.title()}(s) for `{int(i_price * amount):,}` coins!',
            colour=await self.get_economy_colour(ctx.author),
        )
        em.set_footer(text='Thank you for your purchase!')
        return await ctx.send(embed=em)


def buy(bot):
    bot.add_cog(Buy(bot))
