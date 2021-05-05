import discord
import lyricsgenius as LyrGen
from PyLyrics import *
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from bot import Gen

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils
from libraries.helperFunctions import add_to_embed


class songs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    song_options = [
        {
            "name":"song",
            "description":"The title of the song",
            "type": 3,
            "required": True
        }
    ]
    @cog_ext.cog_slash(name='song', description='Get song lyrics', options=song_options)
    async def songs(self, ctx: SlashContext, song:str=''):
        ctx.defer()
        try:
            #splitting the stream to check if the input has a artist if not add by . to earch for the song name
            #song[1] = artist
            #song[0] = song
            if ' by ' not in str(song): song = str(song) + ' by '
            song = str(song).split(" by ")
            songInfo = PyLyrics.getLyrics(song[1], song[0])
            embed = discord.Embed(title=song[0].title(), colour = imgutils.randomSaturatedColor())

            # Create and send embed
            for e in add_to_embed(embed, songInfo.lyrics):
                e.set_footer(text='Song Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=e)
        except AttributeError as e:
            print(e)
            embed = discord.Embed(title='Error in Song', description='The command was either used incorrectly or the song was not found\nCommand is used as follows: <b>/song songTitle by songArtist</b>')
            embed.set_footer(text='Song Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(songs(bot))
