import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import asyncio

import libraries.prawn as prawn
from libraries.helperFunctions import isOwner, msgReturn, add_to_embed, splitLongStrings
from libraries.prawn import getFileList, getClosestFromList
import libraries.imgutils as imgutils

import time, datetime
from datetime import date
from datetime import datetime

def setup(bot):
    bot.add_cog(admin_commands(bot))

class admin_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='userinfo',
        description="Pull a user's info. Admin only",
        options=[
            create_option(
                name='user',
                description='Ping the person',
                option_type=6,
                required=True
            )
        ],
    )
    async def userinfo(self, ctx: SlashContext, user:discord.User=None):
        if not ctx.author.guild_permissions.administrator and not isOwner(ctx):
            await ctx.send(f'You must be an owner or a server administrator', hidden=True)
            return
        x = ctx.guild.members
        roles = [role for role in user.roles[1:]]
        embed = discord.Embed(title="User information", colour=discord.Color.gold(), timestamp= datetime.fromtimestamp(time.time()))
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text='Info Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)

        #this checks if the user has no roles it will say they have no roles
        listRoles = "User has no roles"
        if len(roles) != 0:
            listRoles = " ".join([role.mention for role in roles])

        fields = [("Name", str(user), False),
            ("Status", user.raw_status, False),
            (f"Roles ({len(roles)})", listRoles , False),
            ("Created at", user.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
            ("Joined at", user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    #kick command
    @cog_ext.cog_slash(name='kick',
        description='Kicks someone. Admin only',
        options=[
            create_option(
                name='user',
                description='Ping the person',
                option_type=6,
                required=True
            )
        ],
    )
    async def kick(self, ctx: SlashContext, user:discord.User=None):
        perms = ctx.author.guild_permissions
        if not (perms.administrator or perms.kick_members):
            await ctx.send("*One of us* doesn't have the permissions to do that...")
            return

        if user == None:
            await ctx.send("You need to ping someone from this server to kick")
            return

        if not ctx.guild.get_member(bot.user.id).permissions_in(ctx.channel).kick_members or  ctx.guild.get_member(bot.user.id).roles[-1] <=  user.roles[-1]:
            await ctx.send("I don't have enough power to do that.")
            return

        canKick = True # I can't stand all these `if`s
        canKick = canKick and user.roles[-1] < ctx.author.roles[-1] # require a lesser role
        canKick = canKick and (not user.guild_permissions.administrator or user.bot) # can't kick admins (but can kick bot admins)
        if ctx.author.id == ctx.guild.owner_id: canKick = True # can't say no to the ownersv
        canKick = canKick and user.id != ctx.author.id # you can't kick yourself (even as an owner)

        if not canKick:
            await ctx.send("You cannot kick <@"+str(user.id)+"> \nthey have permissions higher than or equal to yours.")
            return

        # we can kick now
        msg = msgReturn("kick")
        await ctx.send(msg.format(user.name))
        print('Kicking')
        await user.kick()

    #banning command
    @cog_ext.cog_slash(name='ban',
        description='Bans someone. Admin only',
        options=[
            create_option(
                name='user',
                description='Ping the person',
                option_type=6,
                required=True
            )
        ],

    )
    async def ban(self, ctx: SlashContext, user:discord.User=None):
        perms = ctx.author.guild_permissions
        if not (perms.administrator or perms.ban_members):
            await ctx.send("*One of us* doesn't have the permissions to do that...")
            return

        if user == None:
            await ctx.send("You need to ping someone from this server to ban")
            return

        if not ctx.guild.get_member(bot.user.id).permissions_in(ctx.channel).kick_members or  ctx.guild.get_member(bot.user.id).roles[-1] <=  user.roles[-1]:
            await ctx.send("I don't have enough power to do that.")
            return

        canBan = True # I can't stand all these `if`s
        canBan = canBan and user.roles[-1] < ctx.author.roles[-1] # require a lesser role
        canBan = canBan and (not user.guild_permissions.administrator or user.bot) # can't ban admins (but can ban bot admins)
        if ctx.author.id == ctx.guild.owner_id: canBan = True # can't say no to the owners
        canBan = canBan and user.id != ctx.author.id # you can't ban yourself (even as an owner)

        if not canBan:
            await ctx.send("You cannot ban <@"+str(user.id)+"> \nthey have permissions higher than or equal to yours.")
            return

        # we can ban now
        msg = msgReturn("ban")
        await ctx.send(msg.format(user.name))
        print('Banning')
        await user.ban()


    ####################################################
    ################ OWNER COMMANDS ####################
    ####################################################

    # for the admins to turn off the bot
    @cog_ext.cog_slash(name='off', description='Kills me. Owner only')
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
                name = 'url',
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