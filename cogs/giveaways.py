import discord

from cogs import DonationCog
from discord.ext import commands


class DonationLogging(DonationCog):
    role_100 = 794295747800465428
    role_250 = 794295625365192704
    role_500 = 820295774927323156
    role_1000 = 820295730601918494
    role_2500 = 820295144788066375

    special_role = 820294120621867049

    @commands.command(name='mydonos', aliases=['mydonations', 'donation', 'mydonoation', 'mydono'])
    async def donos(self, ctx):
        return await ctx.send(
            embed=await self.create_embed(title=f'{ctx.author.name}\'s Donation statistics',
                                          description=f'{await self.fetch_donation_statistics(ctx.author.id):,}',
                                          colour=discord.Colour.random()))

    @donos.error
    async def donos_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Giveaways'),
        commands.has_role('Giveaway Manager')
    )
    @commands.command(name='dono')
    async def dono(self, ctx: commands.Context, argument1: str = None, user: discord.Member = None,
                   amount: str = None, *, reason='Not provided'):
        if argument1 not in ['add', 'remove', 'check']:
            return await ctx.send(embed=discord.Embed(colour=discord.Colour.red(), title='Error!',
                                                      description='Please provide one of the valid arguments '
                                                                  'below:\n`add`\n`remove`\n`check`\n\nExample: '
                                                                  '`s!dono add @user 100`'))

        if user is None:
            return await ctx.send(embed=discord.Embed(colour=discord.Colour.red(), title='Error!',
                                                      description='Please provide a valid member after this '
                                                                  'command!\n\nExample: `s!dono add @user 100`'))

        if argument1 == 'check':
            return await ctx.send(embed=discord.Embed(title=f'{user.display_name}\'s Donation credit',
                                                      description=f'Total amount donated: '
                                                                  f'{await self.fetch_donation_statistics(user.id):,}'))

        if amount is None:
            return await ctx.send(embed=discord.Embed(colour=discord.Colour.red(), title='Error!',
                                                      description='Please provide a valid amount after this '
                                                                  'command!\n\nExample: `s!dono add @user 100`'))

        def convert_str_to_number(x) -> int:
            total_stars = 0
            num_map = {'k': 1000,
                       'm': 1000000,
                       'b': 1000000000,
                       'e0': 1,
                       'e1': 10,
                       'e2': 100,
                       'e3': 1000,
                       'e4': 10000,
                       'e5': 100000,
                       'e6': 1000000,
                       'e7': 10000000,
                       'e8': 100000000,
                       'e9': 1000000000,
                       'e10': 10000000000}

            if x.isdigit():
                total_stars = int(x)
            else:
                if len(x) > 1:
                    total_stars = float(x[:-1]) * num_map.get(x[-1].lower(), 1)
            return int(total_stars)

        amount = convert_str_to_number(amount)

        try:
            amount = int(amount)
        except ValueError or TypeError:
            return await ctx.send(embed=await self.error(description='Please provide a valid amount!'))

        if argument1 == 'add':
            await self.add_donation(user.id, amount)
            new_amount_donated = await self.fetch_donation_statistics(user.id)

            for args in [(100000000, self.role_100), (250000000, self.role_250), (500000000, self.role_500),
                         (1000000000, self.role_1000), (2500000000, self.role_2500), (2500000000, self.special_role)]:
                for _ in user.roles:
                    if new_amount_donated < args[0]:
                        break
                else:
                    await user.add_roles(discord.Object(id=args[1]))

            await self.bot.get_channel(self.constants.notifs_channel.id).send(
                embed=discord.Embed(colour=discord.Colour.green(), title='Yet another donation',
                                    description=f'{amount:,} was donated by {user.mention}.\nThis was '
                                                f'logged by {ctx.author.mention}.\nTheir new total: '
                                                f'{new_amount_donated:,}\nReason: {reason}'))

            try:
                await user.send(embed=discord.Embed(colour=discord.Colour.green(), title='Added!',
                                                    description=f'{amount:,} donation credit was added'
                                                                f' to your donation credit by {ctx.author.mention}'
                                                                f'.\nYour new total: '
                                                                f'{new_amount_donated:,}\nReason: {reason}'))
            except discord.Forbidden:
                pass

            return await ctx.send(embed=discord.Embed(title='Added!',
                                                      description=f'{amount:,} donation credit was added to '
                                                                  f'{user.mention} by {ctx.author.mention}.\nThe'
                                                                  f'ir new total: '
                                                                  f'{new_amount_donated:,}'))

        if argument1 == 'remove':
            await self.add_donation(user.id, (amount * -1))

            new_amount_donated = await self.fetch_donation_statistics(user.id)

            for args in [(100000000, self.role_100), (250000000, self.role_250), (500000000, self.role_500),
                         (1000000000, self.role_1000), (2500000000, self.role_2500), (2500000000, self.special_role)]:
                for _ in user.roles:
                    if new_amount_donated > args[0]:
                        break
                else:
                    await user.remove_roles(discord.Object(id=args[1]))

            await self.bot.get_channel(self.constants.notifs_channel.id).send(
                embed=discord.Embed(colour=discord.Colour.red(), title='Removed donation credit!',
                                    description=f'{amount:,} was removed from {user.mention}.\nThis was logged'
                                                f' by {ctx.author.mention}.\nTheir new total: '
                                                f'{new_amount_donated:,}'))

            try:
                await user.send(embed=discord.Embed(colour=discord.Colour.red(), title='Removed!',
                                                    description=f'{amount:,} donation credit was removed'
                                                                f' from your donation credit by {ctx.author.mention}'
                                                                f'.\nYour new total: '
                                                                f'{new_amount_donated:,}\nReason: {reason}'))
            except discord.Forbidden:
                pass

            return await ctx.send(embed=discord.Embed(colour=discord.Colour.red(), title='Removed!',
                                                      description=f'{amount:,} donation credit was removed'
                                                                  f' from {user.mention} by {ctx.author.mention}'
                                                                  f'.\nTheir new total: '
                                                                  f'{new_amount_donated:,}\nReason: {reason}'))

    @dono.error
    async def dono_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.command(name='dono-top', aliases=['dt'])
    async def dono_top(self, ctx, *, number=None):
        data = await self.get_all_donation_statistics()

        em = await self.create_embed(title='Top DMC donators', description='', colour=discord.Colour.random())

        data_2 = {}
        data_3 = {}
        count = 1
        description = ''

        for k, v in data.items():
            data_2[int(v['donated_amount'])] = int(k)

        for k, v in sorted(data_2.items(), reverse=True):
            if int(k) > 500000:
                data_3[str(k)] = str(v)

        m_list = []
        for x in ctx.guild.members:
            m_list.append(str(x.id))

        for k, v in data_3.items():
            try:
                number = int(number)
                if count == (number + 1):
                    break
            except:
                if count == 11:
                    break

            if v not in m_list:
                continue

            description += f'{count}. {int(k):,}: {ctx.guild.get_member(int(v)).mention}\n'
            count += 1

        em.description = description
        return await ctx.send(embed=em)

    @dono_top.error
    async def dono_top_error(self, ctx, error):
        await self.log_error(ctx, error)


def setup(bot):
    bot.add_cog(DonationLogging(bot))
