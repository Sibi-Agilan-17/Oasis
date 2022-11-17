import asyncio
import discord
import random
import re
import stringcase
import unicodedata
import unidecode

from cogs import BaseCog
from discord.ext import commands
from discord.ext.commands import is_owner


class DeCancer(BaseCog):
    nouns = [
        "Dog",
        "Cat",
        "Gamer",
        "Ork",
        "Memer",
        "Robot",
        "Programmer",
        "Player",
        "Doctor",
        "Communist",
        "Apple",
        "Godfather",
        "Mafia",
        "Detective",
        "Politician"]

    adjectives = [
        "Fast",
        "Defiant",
        "Homeless",
        "Adorable",
        "Delightful",
        "Homely",
        "Quaint",
        "Adventurous",
        "Depressed",
        "Horrible",
        "Aggressive",
        "Determined",
        "Hungry",
        "Real",
        "Agreeable",
        "Different",
        "Hurt",
        "Relieved",
        "Alert",
        "Difficult",
        "Repulsive",
        "Alive",
        "Disgusted",
        "Ill",
        "Rich",
        "Amused",
        "Distinct",
        "Important",
        "Angry",
        "Disturbed",
        "Impossible",
        "Scary",
        "Annoyed",
        "Dizzy",
        "Inexpensive",
        "Selfish",
        "Annoying",
        "Doubtful",
        "Innocent",
        "Shiny",
        "Anxious",
        "Drab",
        "Inquisitive",
        "Shy",
        "Arrogant",
        "Dull",
        "Itchy",
        "Silly",
        "Ashamed",
        "Sleepy",
        "Attractive",
        "Eager",
        "Jealous",
        "Smiling",
        "Average",
        "Easy",
        "Jittery",
        "Smoggy",
        "Awful",
        "Elated",
        "Jolly",
        "Sore",
        "Elegant",
        "Joyous",
        "Sparkling",
        "Bad",
        "Embarrassed",
        "Splendid",
        "Beautiful",
        "Enchanting",
        "Kind",
        "Spotless",
        "Better",
        "Encouraging",
        "Stormy",
        "Bewildered",
        "Energetic",
        "Lazy",
        "Strange",
        "Enthusiastic",
        "Light",
        "Stupid",
        "Bloody",
        "Envious",
        "Lively",
        "Successful",
        "Blue",
        "Evil",
        "Lonely",
        "Super",
        "Blue-eyed",
        "Excited",
        "Long",
        "Blushing",
        "Expensive",
        "Lovely",
        "Talented",
        "Bored",
        "Exuberant",
        "Lucky",
        "Tame",
        "Brainy",
        "Tender",
        "Brave",
        "Fair",
        "Magnificent",
        "Tense",
        "Breakable",
        "Faithful",
        "Misty",
        "Terrible",
        "Bright",
        "Famous",
        "Modern",
        "Tasty",
        "Busy",
        "Fancy",
        "Motionless",
        "Thankful",
        "Fantastic",
        "Muddy",
        "Thoughtful",
        "Calm",
        "Fierce",
        "Mushy",
        "Thoughtless",
        "Careful",
        "Filthy",
        "Mysterious",
        "Tired",
        "Cautious",
        "Fine",
        "Tough",
        "Charming",
        "Foolish",
        "Nasty",
        "Troubled",
        "Cheerful",
        "Fragile",
        "Naughty",
        "Clean",
        "Frail",
        "Nervous",
        "Ugliest",
        "Clear",
        "Frantic",
        "Nice",
        "Ugly",
        "Clever",
        "Friendly",
        "Nutty",
        "Uninterested",
        "Cloudy",
        "Frightened",
        "Unsightly",
        "Clumsy",
        "Funny",
        "Obedient",
        "Unusual",
        "Colorful",
        "Obnoxious",
        "Upset",
        "Combative",
        "Gentle",
        "Odd",
        "Uptight",
        "Comfortable",
        "Gifted",
        "Old-fashioned",
        "Concerned",
        "Glamorous",
        "Open",
        "Vast",
        "Condemned",
        "Gleaming",
        "Outrageous",
        "Victorious",
        "Confused",
        "Glorious",
        "Outstanding",
        "Vivacious",
        "Cooperative",
        "Good",
        "Courageous",
        "Gorgeous",
        "Panicky",
        "Wandering",
        "Crazy",
        "Graceful",
        "Perfect",
        "Weary",
        "Creepy",
        "Grieving",
        "Plain",
        "Wicked",
        "Crowded",
        "Grotesque",
        "Pleasant",
        "Wide-eyed",
        "Cruel",
        "Grumpy",
        "Poised",
        "Wild",
        "Curious",
        "Poor",
        "Witty",
        "Cute",
        "Handsome",
        "Powerful",
        "Worrisome",
        "Happy",
        "Precious",
        "Worried",
        "Dangerous",
        "Healthy",
        "Prickly",
        "Wrong",
        "Dark",
        "Helpful",
        "Proud",
        "Dead",
        "Helpless",
        "Putrid",
        "Zany",
        "Defeated",
        "Hilarious",
        "Puzzled",
        "Zealous",
        "Dank",
        "Sexy",
        "Darth"]

    @staticmethod
    def is_cancerous(text: str) -> bool:
        for segment in text.split():
            for char in segment:
                if not (char.isascii() and char.isalnum()):
                    return True

        return False

    # the magic
    @staticmethod
    def strip_accs(text):
        try:
            text = unicodedata.normalize("NFKC", text)
            text = unicodedata.normalize("NFD", text)
            text = unidecode.unidecode(text)
            text = text.encode("ascii", "ignore")
            text = text.decode("utf-8")
        except Exception as e:
            print(e)

        return str(text)

    # the magician
    async def nick_maker(self, old_shit_nick):
        try:
            old_shit_nick = self.strip_accs(old_shit_nick)
            new_cool_nick = re.sub("[^a-zA-Z0-9 \n.]", "", old_shit_nick)
            new_cool_nick = " ".join(new_cool_nick.split())
            new_cool_nick = stringcase.lowercase(new_cool_nick)
            new_cool_nick = stringcase.titlecase(new_cool_nick)

            if len(new_cool_nick.replace(" ", "")) <= 1 or len(new_cool_nick) > 32:
                return random.choice(self.adjectives + ' ' + self.nouns)

            return new_cool_nick
        except Exception:
            return random.choice(self.adjectives + ' ' + self.nouns)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            if not member.bot:
                await asyncio.sleep(15)  # Waiting for auto mod actions to take place

                if member:
                    nice_nick = await self.nick_maker(member.display_name)
                    await member.edit(nick=nice_nick)
        except Exception as e:
            print(f"Exception occurred in auto decancer: {e}")

    @commands.check_any(
        is_owner(),
        commands.has_permissions(manage_nicknames=True),
        commands.has_role('Farm Hand - Chat Moderator')
    )
    @commands.command(name='decancer', aliases=['dc'])
    async def decancer(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send('Please provide a valid member lol\nExample: `??decancer @user`')

        nice_nick = await self.nick_maker(member.display_name)
        bad_nick = member.display_name

        await member.edit(nick=nice_nick)

        return await ctx.send(
            embed=discord.Embed(title='Edited their nickname!', colour=discord.Colour.green(),
                                description=f'**Old nick:** {bad_nick}\n**New nick:** {nice_nick}'))

    @commands.check_any(
        is_owner(),
        commands.has_permissions(manage_nicknames=True),
        commands.has_role('Farm Hand - Chat Moderator')
    )
    @commands.command(name='set-nick')
    async def set_nick(self, ctx, member: discord.Member, *, nick=None):
        if nick is None:
            nick = random.choice(self.adjectives + ' ' + self.nouns)

        await member.edit(nick=nick)
        await ctx.send(':white_check_mark: Done!')


def setup(bot):
    bot.add_cog(DeCancer(bot))
