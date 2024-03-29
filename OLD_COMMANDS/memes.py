import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import getEmbedsFromLibraryQuery


def setup(bot):
    bot.add_cog(memes(bot))


# TODO: autorun updateReddit.sh when command is ran
class memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    nsfw_meme_options = [
        {"name": "query", "description": "v", "type": 3, "required": False}
    ]
    @cog_ext.cog_slash(
        name="meme",
        description="Get a meme!",
        options=nsfw_meme_options,
    )
    async def meme(self, ctx: SlashContext, query: str = ""):
        memePath = "ClassWork/"
        embed = getEmbedsFromLibraryQuery(memePath, query)[0]
        embed.set_footer(
            text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    # TODO: add cooldown of 60s for each 3 uses
    @cog_ext.cog_slash(
        name="nsfw",
        description="Get some nono pics",
        options=nsfw_meme_options,
    )
    async def nsfw(self, ctx: SlashContext, query: str = ""):
        prawnPath = "MyHomework/"
        # checks of user is trying to get past the nsfw filter
        if ctx.guild is None and ctx.author != self.bot.user:
            await ctx.send(
                "You Dumb stupid you are not allowed to use this command in dms"
            )
        else:
            if (
                ctx.channel.is_nsfw()
            ):  # checks if the channel the command was sent from is nsfw
                embed = getEmbedsFromLibraryQuery(prawnPath, query)[0]
                embed.set_footer(
                    text="Requested by: " + ctx.author.name,
                    icon_url=ctx.author.avatar_url,
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Sorry",
                    description=f"I'm sorry {ctx.author.name}, /nsfw can only be used in an NSFW channel",
                )
                embed.set_footer(
                    text=f"Porn Requested by: {ctx.author.name}",
                    icon_url=ctx.author.avatar_url,
                )
                await ctx.send(embed=embed)
