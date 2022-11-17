import asyncio
import discord
import json
import os
from discord.ext import commands
from discordTogether import DiscordTogether

client = commands.Bot('s!', help_command=None, intents=discord.Intents.all())
together_client = DiscordTogether(client)


@client.command(name='start-yt', aliases=['start-youtube', 'start-you-tube'])
async def y(ctx):
    link = await together_client.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click the blue link!\n{link}")


@client.event
async def on_message(msg):
    return msg


@client.event
async def on_ready():
    print('Online!')
    
    while True:
        await asyncio.sleep(300)
        ch = client.get_channel(862938282487709706)

        await ch.send(file=discord.File('./cogs/data.json'))
        

@client.group(invoke_without_subcommand=True)
async def profile(ctx, *, member: discord.Member = None):
    user = member or ctx.author
    badges = []
    u = '<:unknownbadge:848773960652816444>'

    em = discord.Embed(title=f'{user.name}\'s profile', colour=discord.Colour.gold(), timestamp=ctx.message.created_at)

    with open('data.json') as f:
        data = json.load(f)

    badges.append('<:premiumuserbadge:848047065577684999>' if user.id in data[
        'premium_users'] else '<:normieuserbadge:848047063890788362>')

    badges.append('' if user.id in data['verified_users'] else u)

    badges.append('<:botownerbadge:848769233432346644>' if user.id == data['owner'] else u)

    badges.append('<:botdeveloperbadge:848047078499811328> ' if user.id in data['developers'] else u)

    badges.append('<:botemployeebadge:848047076134748200> ' if user.id in data['employees'] else u)

    badges.append('<:bughunterbadge:848047073257455626>' if user.id in data['bug_hunters'] else u)

    badges.append('<:goldenbughunterbadge:848047075840229387> ' if user.id in data['premium_bug_hunters'] else u)

    badges.append('<:boosterbadge:848769234870861844>' if user.id in data['boosters'] else u)

    badges.append('<:partnerbadge:848047074117419060>' if user.id in data['partners'] else u)

    em.description = '**Badges:** '

    for x in badges:
        em.description += (x + ' ')

    return await ctx.send(embed=em)


for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        client.load_extension(f'cogs.{fn[:-3]}')

client.run('ODQ5NDk1MTMxMzQ2NTY3MjI4.YLb__g.1UIaXkhf_CNELv47NaPupcnjLHA')
