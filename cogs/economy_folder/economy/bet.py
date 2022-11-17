import asyncio
import discord
import random

from cogs import EconomyCog
from discord.ext import commands
from cogs.economy_folder.utils import multiplier_calculator


class Bet(EconomyCog):
    _cache = []
    _bl = {}

    @commands.cooldown(5, 1, commands.BucketType.user)
    @commands.command(name='bet', aliases=['roll', 'gamble'])
    async def bet(self, ctx, *, amount):
        if str(ctx.author.id) not in self._bl:
            self._bl[str(ctx.author.id)] = 0

        t = self._bl[str(ctx.author.id)]

        if t > 1:
            self._bl[str(ctx.author.id)] += 1
            self.constants.bans.append(ctx.author.id)
            await ctx.author.send('You have been bot banned for spamming.')

            c = []
            for x in self._cache:
                if x != ctx.author.id:
                    c.append(x)

            self._cache = c
            return

        if self._bl[str(ctx.author.id)] > 0:
            self._bl[str(ctx.author.id)] += 1
            return

        data = await self.get_balance_for(ctx.author)

        if amount == 'max':
            if data > 1000000:
                amount = 1000000
            else:
                amount = data

        try:
            int(amount)
        except ValueError or TypeError:
            return await ctx.send(embed=await self.error(description='Invalid number provided!\nProvide a valid '
                                                                     'number or `max`'))
        else:
            amount = int(amount)

        if amount < 1000:
            return await ctx.send(embed=await self.error(description='The minimum bet amount is 1,000!'))

        if amount > 1000000:
            return await ctx.send(embed=await self.error(description='The maximum bet amount is 1,000,000!'))

        data = await self.get_economy_data_for(ctx.author)

        if data['balance'] < amount:
            return await ctx.send(embed=await self.error(description='You don\'t have enough money!'))

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        bot = random.choice(numbers)
        player = random.choice(numbers)

        await self.add_experience(ctx, ctx.author, random.choice([0, 0, 0, 0, 1]))

        if bot == player:
            winnings = int(amount * 3/10)
            await self.add_coins(ctx.author, -winnings)

            em = await self.create_embed(
                    title=f'{ctx.author.display_name}\'s gambling game!',
                    colour=discord.Colour.gold()
                )

            em.add_field(name='Oasis', value=f'Rolled `{bot}`', inline=True)
            em.add_field(name=f'{ctx.author.display_name}', value=f'Rolled `{player}`', inline=True)
            em.add_field(name='You lost', value=f'{abs(winnings):,} coins!', inline=False)

            await ctx.send(embed=em)

        elif bot > player:
            winnings = int(amount)
            await self.add_coins(ctx.author, -winnings)

            em = await self.create_embed(
                title=f'{ctx.author.display_name}\'s gambling game!',
                colour=discord.Colour.red()
            )

            em.add_field(name='Oasis', value=f'Rolled `{bot}`', inline=True)
            em.add_field(name=f'{ctx.author.display_name}', value=f'Rolled `{player}`', inline=True)
            em.add_field(name='You lost', value=f'{abs(winnings):,} coins!', inline=False)

            await ctx.send(embed=em)

        elif bot < player:
            w_amount = int((amount * 0.009) * int(await multiplier_calculator(ctx.author) / 1.5))
            winnings = random.choice([x for x in range(w_amount - int(amount / 4), w_amount + int(amount / 4))])

            await self.add_coins(ctx.author, winnings)

            em = await self.create_embed(
                title=f'{ctx.author.display_name}\'s gambling game!',
                colour=discord.Colour.green()
            )

            em.add_field(name='Oasis', value=f'Rolled `{bot}`', inline=True)
            em.add_field(name=f'{ctx.author.display_name}', value=f'Rolled `{player}`', inline=True)
            em.add_field(name='You won', value=f'{abs(winnings):,} coins!', inline=False)

            await ctx.send(embed=em)

        self._cache.append(ctx.author.id)
        self._bl[str(ctx.author.id)] += 1

        c = []
        for x in self._cache:
            if x != ctx.author.id:
                c.append(x)

        self._cache = c
        self._bl[str(ctx.author.id)] = 0


def bet(bot):
    bot.add_cog(Bet(bot))
