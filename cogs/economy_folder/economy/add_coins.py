import asyncio
import random

from cogs import EconomyCog
from discord.ext import commands
from cogs.economy_folder.utils import multiplier_calculator


class AddCoins(EconomyCog):
    _cache = []
    _bl = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 658773712874766366:
            return

        if (message.author.id not in self.constants.black_lists) and (message.author.id not in self.constants.bans):
            if (not message.author.bot) and (message.author.discriminator != 0000):
                if message.content.lower() == 'oasis':
                    if str(message.author.id) not in self._bl:
                        self._bl[str(message.author.id)] = 0

                    t = self._bl[str(message.author.id)]

                    if t > 4:
                        self._bl[str(message.author.id)] += 1
                        self.constants.bans.append(message.author.id)
                        await message.author.send('You have been bot banned for spamming.')

                        c = []
                        for x in self._cache:
                            if x != message.author.id:
                                c.append(x)

                        self._cache = c
                        return

                    if self._bl[str(message.author.id)] > 0:
                        self._bl[str(message.author.id)] += 1
                        return

                    await self.add_experience(message.channel, message.author,
                                              random.choice([0, 0, 1, 1, 2]))

                    if (random.randint(1, 30) == 25) or message.author.id == 750245670761529346:
                        await self.add_coins(message.author, 1000000)
                        await self.add_item(message.author, 'mystery_gem', 1)

                        return await message.reply(
                            embed=await self.create_embed(
                                title='Earned coins!',
                                description=f'You have earned {1000000:,} coins for saying `oasis`!\nYou also found a '
                                            f'Mystery Gem!',
                                colour=await self.get_economy_colour(message.author)
                            )
                        )

                    multi = await multiplier_calculator(message.author)

                    if multi == 0:
                        return

                    coins = random.randint(multi, multi * 2)
                    await self.add_coins(message.author, coins)

                    g = self.bot.get_guild(768814966244769812)

                    if message.author in g.members:
                        await message.reply(
                            embed=await self.create_embed(
                                title='Earned coins!',
                                description=f'You have earned {coins * 2:,} coins for saying `oasis`!\n2x Bonus for '
                                            f'being a bot admin',
                                colour=await self.get_economy_colour(message.author)
                            )
                        )
                        await self.add_coins(message.author, coins)
                        return

                    await message.reply(
                        embed=await self.create_embed(
                            title='Earned coins!',
                            description=f'You have earned {coins:,} coins for saying `oasis`!',
                            colour=await self.get_economy_colour(message.author)
                        )
                    )

                    self._cache.append(message.author.id)
                    self._bl[str(message.author.id)] += 1

                    await asyncio.sleep(5)

                    c = []
                    for x in self._cache:
                        if x != message.author.id:
                            c.append(x)

                    self._cache = c
                    self._bl[str(message.author.id)] = 0


def add_coins(bot):
    bot.add_cog(AddCoins(bot))
