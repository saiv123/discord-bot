import naff as dis

from libraries.helperFunctions import getEmbedsFromLibraryQuery

class Meme(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot: dis.Client = bot
    
    @dis.slash_command(name="meme", description="Get a meme")
    @dis.slash_option(
        "category"
        "What category do you want",
        dis.OptionTypes.STRING,
        False,)
    async def meme(self, ctx: dis.InteractionContext, category: str="", **kwargs):
        memePath = "ClassWork/"
        embed = getEmbedsFromLibraryQuery(memePath, category)[0]
        embed.set_footer(text="Requested by: " + ctx.author.nickname, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    
    @dis.slash_command(name="nsfw", description="Get a Porn")
    @dis.slash_option(
        "category"
        "What category do you want",
        dis.OptionTypes.STRING,
        False,)
    async def meme(self, ctx: dis.InteractionContext, category: str="", **kwargs):
        prawnPath = "MyHomework/"
        # checks of user is trying to get past the nsfw filter
        if ctx.guild is None and ctx.author.bot != True:
            await ctx.send("You Dumb stupid you are not allowed to use this command in dms")
        else:
            # checks if the channel the command was sent from is nsfw
            if (ctx.channel.nsfw):
                embed = getEmbedsFromLibraryQuery(prawnPath, category)[0]
                embed.set_footer(
                    text="Requested by: " + ctx.author.nickname,
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=embed)
            else:
                embed = dis.Embed(
                    title="Sorry",
                    description=f"I'm sorry {ctx.author.nickname}, /nsfw can only be used in an NSFW channel",
                )
                embed.set_footer(
                    text=f"Porn Requested by: {ctx.author.nickname}",
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=embed)

def setup(bot):
    Meme(bot)