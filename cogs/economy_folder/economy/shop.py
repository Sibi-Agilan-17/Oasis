import discord

from cogs import EconomyCog
from discord.ext import commands

page_1 = \
    """
__**Common Gem**__
Price: 100 coins
The common gem posses the power to do nothing!?? Since this is way too common, 
it is called a Common Gem.

__**Uncommon Gem**__
Price: 1,000 coins
The opposite of Common Gem. A little uncommon than the common gem.

__**Rare Gem**__
Price: 10,000 coins
The rare gem is pretty rare, even though some players have thousands of them.

__**Epic Gem**__
Price: 100,000 coins
The epic gem possess the power of epicness, which could be useful sometimes!

__**Golden Gem**__
Price: 1,000,000 coins
The rare golden gem is made of pure gold! Buy it if you can!
"""

page_2 = \
    """
__**Diamond Gem**__
Price: 10,000,000 coins
The super rare diamond gem is never found by the average player! It is owned 
only by the richest of the richest of the richest of the rich! 

__**Legendary Gem**__
Price: 1,000,000,000 coins
The legendary gem is very rare and too op, it has been in the hands of only 
the legends of the bot!
"""


class Shop(EconomyCog):
    @commands.command(name='shop')
    async def shop(self, ctx, number: str ='1'):
        if number == '2':
            p = page_2
        else:
            p = page_1

        em = discord.Embed(
            title='Oasis Shop!',
            color=await self.get_economy_colour(ctx.author)
        )

        em.description = p
        return await ctx.send(embed=em)


def shop(bot):
    bot.add_cog(Shop(bot))
