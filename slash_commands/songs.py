import discord
import lyricsgenius as LyrGen
from azlyrics import artists, songs, artists
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from secret import GenID

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
    @cog_ext.cog_slash(name='song', description='Get song lyrics', options=song_options, guild_ids=[648012188685959169])
    async def songs(self, ctx: SlashContext, song:str=''):
        Gen = LyrGen.Genius(GenID)
        ctx.defer()
        try:
            #splitting the stream to check if the input has a artist if not add by . to earch for the song name
            if ' by ' not in str(song): song = str(song) + ' by '
            song = str(song).split(" by ")
            songInfo = lyrics(song[0], song[1])
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
