from cogs import BaseCog
from discord.ext import commands


class Test(BaseCog):
    pass


def setup(bot):
    bot.add_cog(Test(bot))
