import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import isOwner, msgReturn

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