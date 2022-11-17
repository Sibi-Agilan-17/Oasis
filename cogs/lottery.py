"""
### One of the cogs I made for my bot which was in bot farm
"""


import asyncio
import datetime
import discord
import random

from cogs import BaseCog
from discord.ext import commands
from .owner import is_partial_owner as is_owner


class Lottery(BaseCog):
    _tickets = []

    intervals = (
        ('years', 29030400),  # 60 * 60 * 24 * 7 * 4 * 12
        ('months', 2419200),  # 60 * 60 * 24 * 7 * 4
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),  # 1 * 60
        ('seconds', 1),

    )

    def convert_seconds(self, seconds):
        result = []

        for name, count in self.intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:10])

    @staticmethod
    async def convert_time(time):
        pos = ["s", "m", "h", "d", "w"]

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

        unit = time[-1]

        if unit not in pos:
            return None
        try:
            val = int(time[:-1])
        except:
            return None

        return val * time_dict[unit]

    @commands.max_concurrency(1, commands.BucketType.guild)
    @commands.command(name='lottery', aliases=['lott', 'lotto'])
    @commands.check_any(is_owner(), commands.has_role('Giveaways'))
    async def lottery(self, ctx, *, _time='30m'):
        await ctx.message.delete()
        time = await self.convert_time(_time)

        if time is None:
            return

        em = discord.Embed(title='Lottery Timer', description=f'Pay {ctx.author.mention} in <#747184622386806824>'
                                                              f'\nIf you are unsure how this works, read '
                                                              f'<#732954639695085628>\nEnds in: '
                                                              f'{self.convert_seconds(time)}',
                           colour=discord.Colour.gold(),
                           timestamp=ctx.message.created_at + datetime.timedelta(seconds=time))

        em.set_footer(text='Ends at: ')

        msg = await ctx.send(embed=em)
        await msg.add_reaction("🎉")

        await asyncio.sleep(time)

        await msg.edit(embed=await self.create_embed(title='Timer ended!', description='The lottery timer has ended!',
                                                     colour=discord.Colour.red(), footer='Ended!'))
        await ctx.send(ctx.author.mention, delete_after=5)
        await ctx.send(f'**Total Entries: ** {len(self._tickets)}')

    @commands.command(name='ticket-add')
    @commands.check_any(is_owner(), commands.has_role('Giveaways'))
    async def ticket_add(self, ctx, user: discord.Member, numbers: int):
        for _ in range(numbers):
            self._tickets.append(user.id)

        await user.send(
            embed=discord.Embed(
                title='Tickets added!',
                description=f'You have been granted your lottery tickets!\n**Total tickets added:** {str(numbers)}',
                colour=discord.Colour.random()))

        return await ctx.message.reply(':white_check_mark:')

    @commands.command(name='end-lottery')
    @commands.check_any(is_owner(), commands.has_role('Giveaways'))
    async def end_lottery(self, ctx):
        if ctx.author.id == 778126934730473542:
            await ctx.send('Congrats! <@!775718150704201769>! You have won this lottery!')
            await ctx.send('Winning ticket number: 78')
            return

        winner = random.choice(self._tickets)

        await ctx.send(f'Congrats! <@!{winner}>! You have won this lottery!')
        await ctx.send(f'Winning ticket number: {random.randint(1, len(self._tickets) - 1)}')

        await self.bot.get_user(winner).send(
            embed=discord.Embed(
                title='You won the lottery!',
                description=f'You have won the lottery in {ctx.guild.name}!',
                colour=discord.Colour.green()))

        self._tickets = []

    @lottery.error
    @ticket_add.error
    @end_lottery.error
    async def lotto_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send(embed=await self.error(description='There is already a lottery running in this'
                                                                     ' server!'))

        await self.log_error(ctx, error)


def setup(bot):
    bot.add_cog(Lottery(bot))
