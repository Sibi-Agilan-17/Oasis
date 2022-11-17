import discord

from cogs import EconomyCog
from discord.ext import commands


class Inventory(EconomyCog):
    @commands.command(name='inv', aliases=['inventory'])
    async def inv(self, ctx, *, member: discord.Member = None):
        user = member or ctx.author
        data = await self.get_economy_data_for(user)
        color = await self.get_economy_colour(user)
        description = ''

        for k, v in data['inventory'].items():
            if v == 0:
                continue
            if k == 'common_gem':
                description += f'**Common gem**\nOwned: {v}\n\n'
            if k == 'uncommon_gem':
                description += f'**Uncommon gem**\nOwned: {v}\n\n'
            if k == 'rare_gem':
                description += f'**Rare gem**\nOwned: {v}\n\n'
            if k == 'epic_gem':
                description += f'**Epic gem**\nOwned: {v}\n\n'
            if k == 'golden_gem':
                description += f'**Golden gem**\nOwned: {v}\n\n'
            if k == 'diamond_gem':
                description += f'**Diamond gem**\nOwned: {v}\n\n'
            if k == 'emerald_gem':
                description += f'**Emerald gem**\nOwned: {v}\n\n'
            if k == 'legendary_gem':
                description += f'**Legendary gem**\nOwned: {v}\n\n'
            if k == 'mystery_gem':
                description += f'**Mystery gem**\nOwned: {v}\n\n'

        em = discord.Embed(
            title=f'{user.name}\'s inventory',
            colour=color,
            description=description
        )

        return await ctx.send(embed=em)


def inv(bot):
    bot.add_cog(Inventory(bot))
