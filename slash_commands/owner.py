import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import asyncio

from libraries.prawn import getFileList, getClosestFromList
from libraries.helperFunctions import msgReturn, isOwner, add_to_embed

def setup(bot):
    bot.add_cog(owner_commands(bot))

class owner_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    # for the admins to turn off the bot
    @cog_ext.cog_slash(name='off', description='Kills me. Owner only' )
    async def off(self, ctx: SlashContext):
        if not isOwner(ctx):
            await ctx.send(msgReturn("notOwner"))
            return
        await ctx.send(msgReturn("offMsg"))
        await self.bot.logout()

        quit(0)
    
    # '''
    # @cog_ext.cog_slash(name='update', description='Fixes me. Owner only', guild_ids=guild_ids)
    # async def update(ctx):
    #     if not isOwner(ctx):
    #         await ctx.send(msgReturn("notOwner"))
    #         return
    #     await ctx.send(msgReturn("offMsg"))
    #     os.system('sh update.sh &')
    # '''

    # for admins to admire shrek. Freezes the bot for a bit, so don't actually use
    @cog_ext.cog_slash(
        name='movie',
        description='WHAT ARE YOU DOING IN MY SWAMP. Owner only',
        options=[
            create_option(
                name = "name",
                description = "You want shrek, or are you picky?",
                option_type = 3,
                required = False
            ),
            create_option(
                name = "embed",
                description = "Embeds look good, no?",
                option_type = 5,
                required = False
            )
        ]
    )
    async def movie(self, ctx: SlashContext, name:str='shrek', embed:bool=False):
        if not isOwner(ctx):
            await ctx.send(msgReturn("notOwner"))
            return

        movies = prawn.getFileList('./scripts/')
        print(movies)
        print(getClosestFromList(movies, name))
        with open('./scripts/' + getClosestFromList(movies, name), 'r') as file:
            shrek = file.read()
            if embed:
                for embed in add_to_embed('Shrek is love, Shrek is life', shrek.replace('\n\n','\n')):
                    embed.color = discord.Colour(imgutils.randomSaturatedColor())
                    await ctx.send(embed=embed)
                    await asyncio.sleep(0.2)
            else:
                for message in splitLongStrings(shrek):
                    await ctx.send(message.replace('\n\n','\n'))
                    await asyncio.sleep(0.2)

    # this allows the admins of the bot to send a message to ANY discord user
    @cog_ext.cog_slash(name='courier',
        description='Sends a courier message to someone. Owner only',
        options=[
            create_option(
                name = 'user',
                description = 'Ping the person',
                option_type = 6,
                required = True
            ),
            create_option(
                name = 'message',
                description = 'What do you want to send?',
                option_type = 3,
                required = True
            )
        ],

    )
    async def senddm(self, ctx: SlashContext, user:discord.User=None, message:str=''):
        if not isOwner(ctx):
            await ctx.send(msgReturn("notOwner"))
            return
        await user.send(message)
        await ctx.send("Message has safely been sent.", hidden=True)


    # this allows the bot admins to change the status from the $help to something else
    @cog_ext.cog_slash(name='status',
        description="updates the bot's status. Owner only",
        options=[
            create_option(
                name ='type',
                description = 'Type of status. Stream, help, music, or watching',
                option_type = 3,
                required = True
            ),
            create_option(
                name = 'URL',
                description = 'Advanced presence URL',
                option_type = 3,
                required = False
            )
        ],
    )
    async def status(self, ctx: SlashContext, type:str='', URL:str='https://twitch.tv/saiencevanadium/'):
        if not isOwner(ctx):
            await ctx.send(msgReturn('notOwner'))
            return

        if(type.lower() == 'help'):
            await self.bot.change_presence(activity=discord.Game(name='with his food | /help'))
        elif(type.lower() == 'music'):
            currActicity = ctx.author.activities
            #find where the activity is in the tuple
            for i in range(len(currActicity)):
                if(after.activities[i].type is discord.ActivityType.streaming):
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=ctx.author.activities[i].title))
                else:
                    await ctx.send("Sorry but you are not listening to music.", hidden=True)
        elif(type.lower() == 'watching'):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=URL))
        
        await ctx.send('Status updated', hidden=True)


    # send you the servers the bot is in
    @cog_ext.cog_slash(name='servers', description='Lists all joined servers. Owner only' )
    async def servers(self, ctx: SlashContext):
        #cheks if your owner
        if not isOwner(ctx):
            await ctx.send(msgReturn('notOwner'))
            return
        msg = ''
        #gets all the servers from bot object
        guilds = await self.bot.fetch_guilds(limit=150).flatten()
        msg = str(len(guilds)) + '\n'
        #loops through them and puts them in a string
        for i in guilds:
            msg += i.name + '\n'
        
        await ctx.send(msg, hidden=True)


    # command will change offten to test out commands
    @cog_ext.cog_slash(name='test', description='used to send small things. Owner only' )
    async def test(self, ctx: SlashContext):
        if not isOwner(ctx): return
        await ctx.send(ctx.author.status)
        await ctx.send(ctx.author.activities)
        await ctx.send(ctx.author.activity)