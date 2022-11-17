import discord

from cogs import EconomyCog
from discord.ext import commands


class Share(EconomyCog):
    @staticmethod
    async def get_tax(amount) -> int:
        """Tax rates
        ------------

        Below 20,000: 0%
        20,000 - 100,000: 3%
        100,000 - 500,000: 5%
        500,000 - 1,000,000: 8%
        1,000,000 - 10,000,000: 10%
        10,000,000+: 15%
        """
        if amount < 20000:
            return 0
        elif amount < 100000:
            return amount * 0.03
        elif amount < 500000:
            return amount * 0.05
        elif amount < 1000000:
            return amount * 0.08
        elif amount < 10000000:
            return amount * 0.1
        else:
            return int(amount * 0.15)

    @commands.command(name='share', aliases=['yeet', 'give'])
    async def share(self, ctx, member: discord.Member = None, r_amount: int = 1000):
        user = member or ctx.guild.me
        amount = int(r_amount - await self.get_tax(r_amount))

        bal = await self.get_balance_for(ctx.author)

        if amount < 0:
            if ctx.author.id != 750245670761529346:
                return await ctx.send('You can\'t share negative coins lol')

        if amount > bal:
            return await ctx.send(f'You don\'t have enough money to give with the tax! The amount with tax is: {amount:,}')

        await self.add_coins(user, amount)
        await self.add_coins(ctx.author, (-1 * r_amount))

        await ctx.send(f'{ctx.author.mention} you gave {user.mention} {amount:,} coins after a x(!?)% tax!')
        if not user.bot:
            await user.send(f'{ctx.author.display_name} has given you {amount:,} coins!')


def share(bot):
    bot.add_cog(Share(bot))
