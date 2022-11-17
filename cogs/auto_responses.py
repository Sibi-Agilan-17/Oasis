import asyncio
import random

from cogs import BaseCog
from discord.ext import commands


class Test(BaseCog):
    cooldown = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 747853054329487500:
            if message.author.bot or self.cooldown:
                return

            if '.donate' in message.content and not message.channel.permissions_for(message.author).manage_messages:
                role = message.guild.get_role(855877108055015465)
                available = [x for x in role.members if not str(x.status) in ('offline', 'do not disturb')]

                if len(available) < 1:
                    return

                await message.channel.send(random.choice(available).mention)

                self.cooldown = True
                await asyncio.sleep(300)
                self.cooldown = False


def setup(bot):
    bot.add_cog(Test(bot))
