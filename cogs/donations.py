import discord

from cogs import DonationCog
from discord.ext import commands

donos_message_raw = \
    """
**__Donation guidelines__**

`1.` Talking or misuse of this channel will result in hard mutes.
`2.` How to Donate: use `s!donate` ( ≥ 500k  + tax; level requirements for gaws above 1m ea).
`3.` Keep the messages appropriate according to <#658772308462141450> .
`4.` Type `s!managers` to show available giveaway managers. You may ping other staff members with this role, as well (**no spam pinging**).
`5.` Don't send anything before receiving approval from a giveaway manager.
"""


class Giveaways(DonationCog):
    role_250 = 850583464872902666
    role_500 = 850583465237807135
    role_1000 = 850583465534685214
    role_2500 = 850583465597993000
    role_5000 = 850583465866428447

    @commands.command(name='donos', aliases=['donations'])
    async def donos(self, ctx):
        await ctx.send(embed=await self.create_embed(title='Donation ', description=donos_message_raw,
                                                     colour=discord.Colour.gold()))
        await ctx.send('Type `s!managers` to see which giveaway managers are available now.\nUse `s!donate` to donate.')

    @donos.error
    async def donos_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(title='Help!')
        em.add_field(name='Chat Moderator', value='`decancer`, `set-nick`, `random-name`, `freeze-nick`', inline=False)
        em.add_field(name='Giveaway manager', value='`dono`, `available`, `unavailable`', inline=False)
        em.add_field(name='Heist Leader', value='`heist-add`, `heist-remove`, `heist-check`', inline=False)
        em.add_field(name='All', value='`mydonos`, `donos`, `managers`', inline=False)
        em.add_field(name='Staff', value='`mm-available`, `mm-unavailable`', inline=False)
        em.add_field(name='Trade', value='`middle-mans`', inline=False)
        em.add_field(name='Boosters', value='`snipe`, `snipe-list`, `esnipe`, `esnipe-list`', inline=False)
        em.add_field(name='Fun', value='`chat-bot`', inline=False)
        em.add_field(name='Economy', value='`bal`, `multi`, `level` | Type `oasis` if you want money', inline=False)
        em.set_footer(text='Bot developed by Sibi Agilan#4853')
        await ctx.send(embed=em)

    @help.error
    async def help_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.command(aliases=['perk'])
    async def perks(self, ctx, arg=None, value=None):
        if (arg is None) or (arg not in ['redeem']):
            return await ctx.send(embed=await self.error(description='Please provide any of the following arguments '
                                                                     'with the command:\n`redeem`\n\nExample: `s!perk'
                                                                     ' redeem 250m`'))

        if (value is None) or (value not in ['250m', '500m', '1bil', '2.5bil', '5bil']):
            return await ctx.send(embed=await self.error(description='Please provide any of the following arguments '
                                                                     'with the command:\n`250m`\n`500m`\n`1bil`\n`2'
                                                                     '.5bil`\n`5bil`\n\nExample: `s!perk redeem '
                                                                     '250m`'))

        if value == '250m':
            if await self.fetch_donation_statistics(ctx.author.id) > 250000000:
                await self.add_donation(ctx.author, -250000000)

                await ctx.author.add_roles(discord.Object(id=self.role_250))

                await ctx.send('Successfully redeemed the role!')

                await self.bot.get_channel(794378435254157342).send(
                    embed=await self.create_embed(
                        title='New perk redeemed!',
                        description=f'{ctx.author.mention}({ctx.author.id}) redeemed the {value} perk.\nTheir new '
                                    f'balance: `{await self.fetch_donation_statistics(ctx.author.id):,}`\nThis perk '
                                    f'will automatically expire in 10 days.',
                        colour=discord.Colour.green()))

            return await ctx.send(embed=await self.error(description='Not enough funds lol'))

        if value == '500m':
            if await self.fetch_donation_statistics(ctx.author.id) > 500000000:
                await self.add_donation(ctx.author, -500000000)

                await ctx.author.add_roles(discord.Object(id=self.role_500))

                await ctx.send('Successfully redeemed the role!')

                await self.bot.get_channel(794378435254157342).send(
                    embed=await self.create_embed(
                        title='New perk redeemed!',
                        description=f'{ctx.author.mention}({ctx.author.id}) redeemed the {value} perk.\nTheir new '
                                    f'balance: `{await self.fetch_donation_statistics(ctx.author.id):,}`\nThis perk '
                                    f'will automatically expire in 30 days.',
                        colour=discord.Colour.green()))

            return await ctx.send(embed=await self.error(description='Not enough funds lol'))

        if value == '1bil':
            if await self.fetch_donation_statistics(ctx.author.id) > 1000000000:
                await self.add_donation(ctx.author, -1000000000)

                await ctx.author.add_roles(discord.Object(id=self.role_1000))

                await ctx.send('Successfully redeemed the role!')

                self.bot.get_channel(794378435254157342).send(
                    embed=await self.create_embed(
                        title='New perk redeemed!',
                        description=f'{ctx.author.mention}({ctx.author.id}) redeemed the {value} perk.\nTheir new '
                                    f'balance: `{await self.fetch_donation_statistics(ctx.author.id):,}`\nThis perk '
                                    f'will automatically expire in 1 month.',
                        colour=discord.Colour.green()))

            return await ctx.send(embed=await self.error(description='Not enough funds lol'))

        if value == '2.5bil':
            if await self.fetch_donation_statistics(ctx.author.id) > 2500000000:
                await self.add_donation(ctx.author, -2500000000)

                await ctx.author.add_roles(discord.Object(id=self.role_2500))

                await ctx.send('Successfully redeemed the role!')

                await self.bot.get_channel(794378435254157342).send(
                    embed=await self.create_embed(
                        title='New perk redeemed!',
                        description=f'{ctx.author.mention}({ctx.author.id}) redeemed the {value} perk.\nTheir new '
                                    f'balance: `{await self.fetch_donation_statistics(ctx.author.id):,}`\nThis perk '
                                    f'will automatically expire in 3 months.',
                        colour=discord.Colour.green()))

            return await ctx.send(embed=await self.error(description='Not enough funds lol'))

        if value == '5bil':
            if await self.fetch_donation_statistics(ctx.author.id) > 5000000000:
                await self.add_donation(ctx.author, -5000000000)

                await ctx.author.add_roles(discord.Object(id=self.role_5000))

                await ctx.send('Successfully redeemed the role!')

                await self.bot.get_channel(794378435254157342).send(
                    embed=await self.create_embed(
                        title='New perk redeemed!',
                        description=f'{ctx.author.mention}({ctx.author.id}) redeemed the {value} perk.\nTheir new '
                                    f'balance: `{await self.fetch_donation_statistics(ctx.author.id):,}`\nThis perk '
                                    f'will automatically expire in 6 months.',
                        colour=discord.Colour.green()))

            return await ctx.send(embed=await self.error(description='Not enough funds lol'))


def setup(bot):
    bot.add_cog(Giveaways(bot))
