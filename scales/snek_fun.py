import naff


import naff as dis


from libraries.helperFunctions import isOwner, splitLongStrings, add_to_embed
from libraries.helperFunctions import checkAuthSerers
from libraries.helperFunctions import RgbToHex, HexToRgb
from libraries.helperFunctions import msgReturn
import libraries.quotesLib as quotes

import random
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

class Fun(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot: dis.Client = bot
    
    SHOULDI_PHRASES = [
        "Yes! Go $",
        "No, it won't work.",
        "Hmmm, $ might be a fine idea",
        'Unclear, consider rewording "/"',
        "I don't know, ask someone else about $",
    ]

    @dis.slash_command(name="space", description="Spread a message")
    @dis.slash_option(
        "message",
        "What's gotta be spread",
        dis.OptionTypes.STRING,
        required=True,)
    @dis.slash_option(
        "amount",
        "What's gotta be spread",
        dis.OptionTypes.INTEGER,
        required=False,)
    async def space(self, ctx: dis.InteractionContext, message: str = "", amount: int = 1):
        SPACE_LEN_HARD_CAP = 4000
        exp_len = (len(message) - 1) * amount + len(message)
        if not isOwner(ctx) and exp_len >= SPACE_LEN_HARD_CAP:
            await ctx.send(
                "That message would be {0} characters, waaaay higher than the limit of {1}. Chill.".format(
                    exp_len, SPACE_LEN_HARD_CAP
                )
            )
            return
        to_send = (" " * max(1, amount)).join(message)
        for message in splitLongStrings(to_send):
            await ctx.send(message)
    
    @dis.slash_command(name="color", description="Get info on a color")
    @dis.slash_option(
        "input",
        "A color as hex, rgb, or cmyk",
        dis.OptionTypes.STRING,
        required=True,)
    @dis.cooldown(dis.Buckets.USER, 3, 60)
    async def color(self, ctx: dis.InteractionContext, input: str = ""):
        try:
            color_dict = apis.getColor(input)
            embed = apis.colorDictToEmbed(color_dict)
            embed.set_author(name="[See It Here]", url=color_dict["url"])
            embed.set_footer(
                text="Color picked by: " + ctx.author.display_name,
                icon_url=ctx.author.avatar.url,
            )

            await ctx.send(embed=embed)
        except ValueError:
            embed = dis.Embed(
                title="Error in your input",
                description="The given color is incorrect. Enter it in Hex, RGB, or CMYK form",
                color=0xFF0000,
            )
            embed.set_footer(
                text="Color picked by: " + ctx.author.display_name,
                icon_url=ctx.author.avatar.url,
            )
            await ctx.send(embed=embed)
    
    @dis.slash_command(name="shouldi", description="Should I?")
    @dis.slash_option(
        "question",
        "What's the question?",
        dis.OptionTypes.STRING,
        required=True,)
    async def shouldi(self, ctx: dis.InteractionContext, question: str = ""):
        msg = " " + msg + " "
        # msg = ' '.join(msg)
        phrases = [
            "Yes! Go /",
            "No, it won't work.",
            "Hmmm, / might be a fine idea",
            'Unclear, consider rewording "/"',
            "I don't know, ask someone else about /",
        ]
        embed = dis.Embed(
            title="Should I...",
            description="{}\n{}".format(msg, random.choice(phrases).replace("/", msg)),
        )
        embed.set_footer(text="Asked by: " + ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    
    @dis.slash_command(name="boop", description="Boop")
    @dis.slash_option(
        "user",
        "Who's boopin'",
        dis.OptionTypes.USER,
        True,)
    async def boop(self, ctx: dis.InteractionContext, user: dis.User = None):
        await ctx.send(ctx.author.mention + " has Booped " + user.mention)
    
    @dis.slash_command(name="hugh", description="Hugs")
    @dis.slash_option(
        "user",
        "Who's hugging",
        dis.OptionTypes.USER,
        True,)
    async def hug(self, ctx: dis.InteractionContext, user: dis.User = None):
        if ctx.author.id == user.id:
            await ctx.send(self.bot.user.mention + msgReturn("hug") + user.mention + "!! :hugging:")
        else:
            await ctx.send(ctx.author.mention + msgReturn("hug") + user.mention + "!! :hugging:")
    
    @dis.slash_command(name="hugvc", description="Hug everyone in the vc")
    async def hugvc(self, ctx: dis.InteractionContext):
         if ctx.author.voice is None:
            await ctx.send("Sorry but you are not in a voice channel")
         else:
            noBot = []
            people = ctx.author.voice.channel.members
            for person in people:
                if not person.bot:
                    noBot.append(person)

            if len(people) == 1:
                await ctx.send("Seems your the only one, here have a hug.\n" +self.bot.user.mention + msgReturn("hug") + ctx.author.mention + "!! :hugging:")
            elif len(people) > 1:
                pings = ""
                for pepes in noBot:
                    if pepes.id != ctx.author.id:
                        pings += pepes.user.mention
                
                await ctx.send(ctx.author.mention + msgReturn("hug") + pings + "!! :hugging:")
def setup(bot):
    Fun(bot)