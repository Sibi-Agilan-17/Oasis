from cogs import EconomyCog
from discord.ext import commands


class Prestige(EconomyCog):
    @commands.command(name='prestige')
    async def level(self, ctx):
        user = ctx.author
        data = await self.get_economy_data_for(user)
        balance = data['balance']
        level = data['level']

        try:
            inventory = data['inventory']
        except KeyError:
            await self.add_user_to_economy(user)
            inventory = data['inventory']

        try:
            mystery_gem = inventory['mystery_gem']
        except KeyError:
            mystery_gem = 0

        try:
            p_l = data['prestige']
            pq_l = data['prestige']
        except KeyError:
            p_l = 0
            pq_l = 1

        if p_l == 0:
            p_l = 1
            pq_l = 0
        else:
            p_l += 1

        L = (level >= (100 * p_l))

        if (balance >= (100000000 * p_l)) and (1000 if L > 999 else L) and (mystery_gem >= (25 * p_l)):
            data['balance'] = int(10000000 * p_l)
            data['level'] = 1
            data['experience'] = 1
            data[
                'color'] = 'green' if p_l < 2 else 'yellow' if p_l < 4 else 'pink' if p_l < 6 else 'black' if p_l < 11 else 'dark blue'
            data['prestige'] = int(pq_l + 1)
            data['inventory'] = {'golden_gem': int(5 * p_l), 'diamond_gem': int(1 * p_l)}

            await self.set_economy_data_for(user, data)

            return await ctx.send(
                f'Congratulations {user.mention} on achieving Prestige {(pq_l + 1):,}'
                f'\nYou received:\n\t+{int(1e7 * p_l):,} coins\n\t+{int(5 * p_l):,}x Gold Gems\n\t+{int(1 * p_l):,}x Diamond Gem'
            )

        L = int(100 * p_l)
        return await ctx.send(
            embed=await self.create_embed(
                title=f'Prestige {p_l} Requirements',
                description=f'Coins: {int(1e8 * p_l):,}\nLevel: {1000 if L > 999 else L:,}\nMystery Gems: {int(25 * p_l):,}',
                colour=await self.get_economy_colour(user)
            )
        )


def prestige(bot):
    bot.add_cog(Prestige(bot))
