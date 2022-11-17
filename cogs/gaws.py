import asyncio
import datetime
import discord
import random

from cogs import BaseCog
from discord.ext import commands


class Test(BaseCog):
    intervals = (
        ('years', 29030400),  # 60 * 60 * 24 * 7 * 4 * 12
        ('months', 2419200),  # 60 * 60 * 24 * 7 * 4
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),  # 1 * 60
        ('seconds', 1),
    )

    running = []

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

    @commands.check_any(commands.is_owner(), commands.has_role('Giveaways'))
    @commands.command(name='gstart')
    async def start(self, ctx, *, all_args):
        """Developer Notes

        -------------------

        Syntax:

        s!gstart [1s | 1m | 1h | 1d] [1w | 10w | 100w] Prize"""

        all_args = all_args.split(' ')

        try:
            time = await self.convert_time(all_args[0])

            if time is None:
                return await ctx.send(embed=await self.error(description='Invalid time provided!'))

            winners = int(all_args[1][:-1])

            if winners > 100:
                return await ctx.send(embed=await self.error(description='This server\'s maximum winners is set to '
                                                                         '100! Please contact an admin to change '
                                                                         'this.'))

            em = discord.Embed(
                title=' '.join(x + ' ' for x in all_args[2:]),
                description=f'React with :tada: to enter!\nTime Remaining: {self.convert_seconds(time)}\nHosted by: '
                            f'{ctx.author.mention}',
                colour=discord.Colour.gold()
            )
            em.set_footer(text=f'{winners} winner(s) | Ends at: ')
            em.timestamp = ctx.message.created_at + datetime.timedelta(seconds=time)

            msg = await ctx.send(embed=em)
            await msg.add_reaction("🎉")

            await asyncio.sleep(time)

            users = await msg.reactions[0].users().flatten()
            users.pop(users.index(self.bot.user))

            winner = random.choice(users)
            em.set_footer(text='Ended at: ')
            em.description = f':tada: Ended!\nWinner: {winner.mention}'

            await msg.edit(embed=em)

            await ctx.send(f'{winner.mention} has won the giveaway for {" ".join(x + " " for x in all_args[2:])}')

        except IndexError:
            return await ctx.send(embed=await self.error(description='Could not identify all of your arguments. '
                                                                     'Please check the instruction manual before '
                                                                     'trying to use another command.'))

        except ValueError or TypeError:
            return await ctx.send(embed=await self.error(description='Invalid winners provided!'))

    @commands.command(name='ar-test')
    async def ar_test(self, ctx):
        await ctx.message.delete()

        em = discord.Embed(
            title='Auto React test: You will be banned if you react',
            description=f'React with :tada: to enter!\nTime Remaining: {self.convert_seconds(120)}\n'
                        f'Hosted by: {ctx.author.mention}',
            colour=discord.Colour.gold()
        )
        em.set_footer(text='1 winner | Ends at: ')
        em.timestamp = ctx.message.created_at + datetime.timedelta(seconds=120)

        msg = await ctx.send(embed=em)
        await msg.add_reaction("🎉")

        await asyncio.sleep(120)

        users = await msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        await msg.delete()

        return await ctx.author.send(
            embed=discord.Embed(
                title='Auto Reactors',
                description=''.join((x.mention + '\n') for x in users)
            )
        )


def setup(bot):
    bot.add_cog(Test(bot))
