import asyncio

from discord.ext import commands


class AutoMod(commands.Cog):
    BOT_FARM_GUILD_ID = 0

    def __init__(self, bot):
        # Let's fill up our cache
        cache = {}

        guild = bot.fetch_guild(self.BOT_FARM_GUILD_ID)
        # Using meth. `fetch_guild` instead of `get_guild`
        # because the client cache may not yet be filled.

        for channel in guild.text_channels:
            # Loop through the list of channels in the server
            # And add them to the cache
            cache[str(channel.id)] = channel

        self.cache = cache
        self.bot = bot
        self.processing = []
        self.bot.add_listener(self.on_message, 'on_message')

    async def on_message(self, message):
        if message.author.id in self.processing:
            # Another instance of the function is checking the same user already
            return

        if message.channel.id in (self.cache.keys()):  # Message is not from test server or some other server
            self.processing.append(message.author.id)  # To prevent another instance from acting on the same user.

            # Alright the next upcoming processes are complex but I will try my best to explain

            sent_messages = [message.content]  # A list to keep track of the messages a user sends.

            for _ in range(50):  # Max limit
                try:
                    msg = self.bot.wait_for('message', check=lambda m: m.author.id == message.author.id, timeout=60)
                    # Check explanation:
                    #                     Message author is the same,
                    #                     Not including channel id because you can run the command in a different
                    #                     channel afterwards.
                except asyncio.TimeoutError:  # No message received in a minute
                    return

                if msg.content not in sent_messages:
                    sent_messages.append(msg.content)

            for _ in range(250):
                try:
                    msg = self.bot.wait_for('message', check=lambda m: m.author.id == message.author.id, timeout=60)
                    # Check explanation:
                    #                     Message author is the same,
                    #                     Not including channel id because you can run the command in a different
                    #                     channel afterwards.
                except asyncio.TimeoutError:  # No message received in a minute
                    return

                if msg.content not in sent_messages:  # A different message found in between
                    return

                # User keeps on repeating the same set of messages
                # Must be an auto-typer
        