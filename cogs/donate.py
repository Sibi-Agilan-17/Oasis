import asyncio
import discord

from cogs import BaseCog
from discord.ext import commands


class Donate(BaseCog):
    d = 'Please select one of the following:\n\n`1.` Giveaway Request\n`2.` Event Request\n`3.` Friendly Heist'

    @commands.max_concurrency(1, commands.BucketType.user, wait=True)
    @commands.command(name='donate')
    async def donate(self, ctx):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        d_msg = await ctx.send(
            embed=await self.create_embed(
                title='New Donation Request',
                description=self.d,
                colour=discord.Color.blue()
            )
        )

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send(embed=await self.error(description='Timed out!'))

        await ctx.message.delete()
        await d_msg.delete()

        if msg.content == '1':
            await msg.delete()
            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please enter your message.',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=300)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            message = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the amount / list of items you wish to donate.',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            items = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the time of your giveaway.',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            time = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the number of winners for your giveaway.',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            winners = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the requirements(if any)\nRequirements only for 1m+ worth of cash / items',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            req = msg.content

            desc = ''
            desc += f'**Sponsor:** {ctx.author.mention}({ctx.author.display_name}#{ctx.author.discriminator})\n'
            desc += f'**Message:** {message}\n'
            desc += f'**Amount:** {items}\n'
            desc += f'**Time:** {time}\n'
            desc += f'**Requirements:** {req}\n'
            desc += f'**Winners:** {winners}'

            return await ctx.send(
                embed=await self.create_embed(
                    title='A new donation request!',
                    description=desc,
                    colour=discord.Color.blue()
                )
            )

        elif msg.content == '2':
            await msg.delete()
            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the event name.',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            event = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the amount for the prize.',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            amount = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Please provide the additional settings for the event(if any).',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            settings = msg.content

            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Donation Request',
                    description='Any other note for the giveaway managers?',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            note = msg.content

            desc = ''
            desc += f'**Sponsor:** {ctx.author.mention}({ctx.author.display_name}#{ctx.author.discriminator})\n'
            desc += f'**Event:** {event}\n'
            desc += f'**Amount:** {amount}\n'
            desc += f'**Settings:** {settings}\n'
            desc += f'**Additional notes:** {note}'

            return await ctx.send(
                embed=await self.create_embed(
                    title='A new event request!',
                    description=desc,
                    colour=discord.Color.blue()
                )
            )
        elif msg.content == '3':
            await msg.delete()
            d_msg = await ctx.send(
                embed=await self.create_embed(
                    title='New Heist Request',
                    description='Please provide the amount for the heist(minimum 5mil).',
                    colour=discord.Color.blue(),
                    footer='Type `cancel` to cancel'
                )
            )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(embed=await self.error(description='Timed out!'))

            await d_msg.delete()
            await msg.delete()

            if msg.content == 'cancel':
                return

            amount = msg.content

            desc = ''
            desc += f'**Sponsor:** {ctx.author.mention}({ctx.author.display_name}#{ctx.author.discriminator})\n'
            desc += f'**Event:** Friendly Heist\n'
            desc += f'**Amount:** {amount}\n'

            await ctx.send(
                embed=await self.create_embed(
                    title='A new friendly heist request!',
                    description=desc,
                    colour=discord.Color.blue()
                )
            )
            return await ctx.send('Please ping a farmer\'s daughter to host your friendly heist!')

        else:
            await msg.delete()
            return await ctx.send(embed=await self.error(description='Invalid option selected!'))


def setup(bot):
    bot.add_cog(Donate(bot))
