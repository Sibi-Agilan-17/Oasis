"""
### Another one of the cogs I made for my bot which was in bot farm
"""

"""
Invite tracker code credits: DiscordUtils library
"""

from better_profanity import profanity
from discord.errors import Forbidden
from discord import AuditLogAction
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from cogs import BaseCog
from difflib import SequenceMatcher


custom_words = [
    'dick',
    'pussy',
    'penis',
    'vagina',
    'weigner',
    'cum',
    'fuck',
    'blowjob',
    'handjob'
]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class InviteTracker:
    def __init__(self, bot):
        self.bot = bot
        self._cache = {}
        self.add_listeners()

    def add_listeners(self):
        self.bot.add_listener(self.cache_invites, "on_ready")
        self.bot.add_listener(self.update_invite_cache, "on_invite_create")
        self.bot.add_listener(self.remove_invite_cache, "on_invite_delete")
        self.bot.add_listener(self.add_guild_cache, "on_guild_join")
        self.bot.add_listener(self.remove_guild_cache, "on_guild_remove")

    async def cache_invites(self):
        for guild in self.bot.guilds:
            try:
                self._cache[guild.id] = {}
                for invite in await guild.invites():
                    self._cache[guild.id][invite.code] = invite
            except Forbidden:
                continue

    async def update_invite_cache(self, invite):
        if invite.guild.id not in self._cache.keys():
            self._cache[invite.guild.id] = {}
        self._cache[invite.guild.id][invite.code] = invite

    async def remove_invite_cache(self, invite):
        if invite.guild.id not in self._cache.keys():
            return
        ref_invite = self._cache[invite.guild.id][invite.code]
        if (ref_invite.created_at.timestamp() + ref_invite.max_age > datetime.utcnow().timestamp() or ref_invite.max_age == 0) and ref_invite.max_uses > 0 and ref_invite.uses == ref_invite.max_uses - 1:
            try:
                async for entry in invite.guild.audit_logs(limit=1, action=AuditLogAction.invite_delete):
                    if entry.target.code != invite.code:
                        self._cache[invite.guild.id][ref_invite.code].revoked = True
                        return
                else:
                    self._cache[invite.guild.id][ref_invite.code].revoked = True
                    return
            except Forbidden:
                self._cache[invite.guild.id][ref_invite.code].revoked = True
                return
        else:
            self._cache[invite.guild.id].pop(invite.code)

    async def add_guild_cache(self, guild):
        self._cache[guild.id] = {}
        for invite in await guild.invites():
            self._cache[guild.id][invite.code] = invite

    async def remove_guild_cache(self, guild):
        try:
            self._cache.pop(guild.id)
        except KeyError:
            return

    async def fetch_inviter(self, member):
        await sleep(self.bot.latency)

        for new_invite in await member.guild.invites():
            for cached_invite in self._cache[member.guild.id].values():
                if new_invite.code == cached_invite.code and new_invite.uses - cached_invite.uses == 1 or cached_invite.revoked:
                    if cached_invite.revoked:
                        self._cache[member.guild.id].pop(cached_invite.code)
                    elif new_invite.inviter == cached_invite.inviter:
                        self._cache[member.guild.id][cached_invite.code] = new_invite
                    else:
                        self._cache[member.guild.id][cached_invite.code].uses += 1
                    return cached_invite.inviter


class AutoMod(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.invite_tracker = InviteTracker(bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await sleep(120)  # Wait for auto mod actions to take place
        new_member = await member.guild.fetch_member(member.id)
        if new_member:  # User passed auto mod actions successfully
            inviter = await self.invite_tracker.fetch_inviter(new_member)

            if inviter:  # User did not join via vanity link
                similarity = similar(inviter.name, new_member.name)

                ch = self.bot.get_channel(787695946917609472)

                if similarity > 0.65:  # Suspected alt
                    await ch.send(
                        embed=await self.create_embed(
                            title='Suspected alt',
                            description=f'Main: {inviter.id}\nAlt: {new_member.id}'
                        )
                    )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await self.on_message_edit(after)

    @commands.Cog.listener()
    async def on_message(self, message):
        ch = self.bot.get_channel(787695946917609472)

        if message.channel.id == 685572368919298291:  # Trade sellers
            c = message.content.split('\n')
            if (len(c) > 15) or (len(message.clean_content) > 1000):
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Too long trade ad\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif len(message.clean_content) < 10:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Too short / irrelevant ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif 'buying' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Buying ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif 'loan' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Loan ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif 'selling cash' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Fake ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif 'selling coins' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Fake ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )

        elif message.channel.id == 759131412539768872:  # Trade buyers
            c = message.content.split('\n')
            if (len(c) > 15) or (len(message.clean_content) > 1000):
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Too long trade ad\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif len(message.clean_content) < 10:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Too short / irrelevant ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif 'selling' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Selling ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
            elif 'loan' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Loan ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )
        elif message.channel.id == 784080892905652224:  # Fight ads
            if 'loan' in message.clean_content:
                return await ch.send(
                    embed=await self.create_embed(
                        title='Auto Moderator',
                        description=f'Loan ad in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
                    )
                )

        # elif message.channel.id == 658773712874766366:  # General chat
        #     profanity.load_censor_words(custom_words=custom_words)
        #     if profanity.contains_profanity(message.clean_content):
        #         return await ch.send(
        #             embed=await self.create_embed(
        #                 title='Auto Moderator',
        #                 description=f'NSFW in {message.channel.mention}\n\n[Jump!]({message.jump_url})'
        #             )
        #         )

    @commands.command(name='report')
    async def report(self, ctx, *, reason=None):
        await sleep(5)

        if (reason is None) or ((hasattr(ctx.message, 'reference')) and ctx.message.reference.cached_message is None):
            return await ctx.send('Oi you need to reply to a valid message and provide a reason')

        desc = ""
        desc += f'**Report channel:** {ctx.channel.mention}\n**User who reported:** {ctx.author.mention}\n'
        desc += f'\n**User who was reported:** {ctx.message.reference.cached_message.author.mention}\n'
        desc += f'**Report reason(provided by author):** {reason}'
        desc += f'\n\n\n[Jump!]({ctx.message.jump_url})'

        ch = self.bot.get_channel(787695946917609472)
        await ch.send(
            embed=await self.create_embed(
                title='New report!',
                description=desc
            )
        )
        return await ctx.send('Sent your report successfully!')


def setup(bot):
    bot.add_cog(AutoMod(bot))
