import asyncio

from cogs import BaseCog
from discord.ext import commands
from prsaw import RandomStuff


class ChatBot(BaseCog):
    _cache = {}

    def __init__(self, bot):
        super().__init__(bot)

    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    @commands.command(name='chat-bot')
    async def chat_bot(self, ctx, *, text='Hi'):
        if str(ctx.author.id) in self._cache:
            rs = self._cache[str(ctx.author.id)]['random_stuff']
        else:
            rs = RandomStuff(async_mode=True, api_key="8CCkWTKcErIM", bot_name='Oasis')
            self._cache[str(ctx.author.id)] = {
                'random_stuff': rs
            }

        res = await rs.get_ai_response(text)
        await ctx.message.reply(res[0]['message'])


def setup(bot):
    bot.add_cog(ChatBot(bot))
