import asyncio
import discord
import json

from discord.ext import commands

staff_roles = [
    790290355631292467,
    723035638357819432,
    855877108055015465,
    814004142796046408,
    682698693472026749,
    658770981816500234,
    663162896158556212

]


class AutoMod(commands.Cog):
    mute_role_id = 864063973984829440
    spam_data = {}

    def __init__(self, bot, *, cache=None):
        if cache is None:
            cache = {}

        if cache != {}:  # We already have our cache info
            self.spam_data = cache['spam_data']
            self.processing = cache['processing']
        else:
            self.processing = []

        bot.add_listener(self.message_recieve, 'on_message')

    def __del__(self):
        self.quit()

    @staticmethod
    def is_mutable(m):
        return (not m.author.bot) and (m.author.id not in staff_roles)

    @staticmethod
    def quit():
        pass

    def retrive_cache(self) -> dict:
        return {
            'spam_data': self.spam_data,
            'processing': self.processing
        }

    @staticmethod
    async def schedule(*args, action, timer):
        await asyncio.sleep(timer)
        action(args)

    async def message_recieve(self, message):
        if not self.is_mutable(message):  # staff over rides
            return {'action_to_take': None, 'error': 'Staff over rides'}
        if message.author.id in self.processing:  # this kid has been caught and is pending action
            return {'action_to_take': None, 'error': 'Another message by user in process'}

        try:
            self.spam_data[str(message.author.id)] += 1
        except KeyError:
            self.spam_data[str(message.author.id)] = 1

        if self.spam_data[str(message.author.id)] > 6:  # ah we got someone
            self.processing.append(message.author.id)
        else:
            # So what's happening here is that the person
            # is not staff and is mutable by the bot. And also,
            # they are not caught yet. But, we have given them
            # a spam mark which has to be removed. For Bot
            # Farm, the spam threshold has been set to
            # 7 messages / 6 seconds. Hence we wait for
            # 6 seconds then remove our point.

            await asyncio.sleep(6)
            self.spam_data[str(message.author.id)] -= 1
            return False  # User safe

        # Now we have caught a spammer, time to deal

        try:
            await message.author.add_roles(discord.Object(id=self.mute_role_id))
            # They need to know their mute and its reason
            await message.author.send(f'You were muted in {message.guild.name} for 10 minutes.\nReason: Spamming messages in {message.channel.name}  6 messages / 7 seconds.')
        except discord.Forbidden:
            pass
        except discord.NotFound:  # Looks like someone was quick enough to spam and leave
            pass

        # Logging
        with open('./cogs/auto_mod.json', 'r') as f:
            data = json.load(f)

        data['mutes'].append(message.author.id)

        with open('./cogs/auto_mod.json', 'w') as f:
            json.dump(data, f)

        # Now let us schedule our mute
        await self.schedule(discord.Object(id=self.mute_role_id), action=message.author.remove_roles, timer=600)

        # Logging
        with open('./cogs/auto_mod.json', 'r') as f:
            data = json.load(f)

        data['mutes'] = [x for x in self.processing if x != message.author.id]
        self.processing = [x for x in self.processing if x != message.author.id]

        with open('./cogs/auto_mod.json', 'w') as f:
            json.dump(data, f)

        return {'action_to_take': None, 'action_taken': 'mute', 'error': None,
                'reason': f'Spamming messages in {message.channel.name}: Triggered spam mute '}


def setup(bot):
    bot.add_cog(AutoMod(bot))
