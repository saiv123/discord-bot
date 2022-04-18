from typing_extensions import Self
import dis_snek as dis

import libraries.prawn as prawn
from libraries.helperFunctions import isOwner, msgReturn
import libraries.imgutils as imgutils

import time, datetime
from datetime import date
from datetime import datetime

class Admin(dis.Scale):
    def __init__(self, bot: dis.Snake):
        self.bot: dis.Snake = bot
    
    @dis.slash_command(name="userinfo", description="Pull a user's info. Admin only")
    @dis.slash_option(
        "user",
        "ping user",
        dis.OptionTypes.USER,
        True
    )
    async def userinfo(self, ctx: dis.InteractionContext, member: dis.Member=None):
        if not ctx.author.guild_permissions.ADMINISTRATOR and not isOwner(ctx):
            await ctx.send(
                f"You must be an owner or a server administrator", hidden=True
            )
            return
        roles = [role for role in member.roles[1:]]
        embed = dis.Embed(
            title="User information",
            color="#FFD700",
            timestamp=datetime.fromtimestamp(time.time()),
        )
        embed.set_author(name=member.nick, icon_url=member.user.avatar.url)
        embed.set_thumbnail(url=member.user.avatar.url)
        embed.set_footer(
            text="Info Requested by: " + ctx.author.nick, icon_url=ctx.author.avatar.url
        )

        # this checks if the user has no roles it will say they have no roles
        listRoles = "User has no roles"
        if len(roles) != 0:
            listRoles = " ".join([role.mention for role in roles])

        fields = [
            ("Name", member.display_name, False),
            (f"Roles ({len(roles)})", listRoles, False),
            ("Created at", member.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
            ("Joined at", member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

        @dis.slash_command(name="kick", description="Kick a user. Admin only")
        @dis.slash_option(
            "user",
            "ping user",
            dis.OptionTypes.USER,
            True
        )
        async def kick(self, ctx: dis.InteractionContext, member: dis.Member=None):
            perms = ctx.author.guild_permissions
            if not(perms.ADMINISTRATOR or perms.KICK_MEMBERS):
                await ctx.send(f"*One of us* doesn't have the permissions to do that...")
                return
            
            if member == None:
                await ctx.send("You need to ping someone from this server to kick")
                return
            
            if (not dis.Permission.KICK_MEMBERS in ctx.guild.get_member(self.bot.user.id).guild_permissions):
                await ctx.send("I don't have the permissions to do that")
                return
            
            #creating cankick variable
            cankick = True
            cankick = (cankick and member.roles[-1] < ctx.author.roles[-1]) #requires a lesser role
            cankick = cankick and (not member.guild_permissions.administrator or member.bot) # can't kick admins (but can kick bot admins)
            if ctx.author.id == ctx.guild._owner_id:
                cankick = True #bypass for owners just in case
            cankick = (cankick and member.id != ctx.author.id) #can't kick self

            if not cankick:
                await ctx.send(f"You cannot kick {member.user.mention} \nthey have permissions higher than or equal to yours.")
                return
            
            msg = msgReturn("Kick")
            await ctx.send(msg.format(member.user.username))
            print("Kicking")
            await member.kick()
        
        @dis.slash_command(name="ban", description="Ban a user. Admin only")
        @dis.slash_option(
            "user",
            "ping user",
            dis.OptionTypes.USER,
            True
        )
        async def ban(self, ctx: dis.InteractionContext, member: dis.Member=None):
            perms = ctx.author.guild_permissions
            if not(perms.ADMINISTRATOR or perms.BAN_MEMBERS):
                await ctx.send(f"*One of us* doesn't have the permissions to do that...")
                return
            
            if member == None:
                await ctx.send("You need to ping someone from this server to ban")
                return
            
            if (not dis.Permission.BAN_MEMBERS in ctx.guild.get_member(self.bot.user.id).guild_permissions):
                await ctx.send("I don't have the permissions to do that")
                return
            
            #creating canban variable
            canban = True
            canban = (canban and member.roles[-1] < ctx.author.roles[-1]) #requires a lesser role
            canban = canban and (not member.guild_permissions.ADMINISTRATOR or member.bot) # can't ban admins (but can ban bot admins)
            if ctx.author.id == ctx.guild._owner_id:
                canban = True
            canban = (canban and member.id != ctx.author.id) #can't ban self

            if not canban:
                await ctx.send(f"You cannot ban {member.user.mention} \nthey have permissions higher than or equal to yours.")
                return
            
            msg = msgReturn("Ban")
            await ctx.send(msg.format(member.user.username))
            print("Banning")
            await member.ban()
        
            ####################################################
            ################ OWNER COMMANDS ####################
            ####################################################

            #create off command
            @dis.slash_command(name="off", description="Turns the bot off. Owner only")
            async def off(self, ctx: dis.InteractionContext):
                if not isOwner(ctx):
                    await ctx.send(msgReturn("notOwner"))
                    return
                await ctx.send(msgReturn("off"))
                await self.bot.stop()
                quit(0)
            
            #create servers command
            @dis.slash_command(name="servers", description="Lists all servers the bot is in. Owner only")
            async def servers(self, ctx: dis.InteractionContext):
                if not isOwner(ctx):
                    await ctx.send(msgReturn("notOwner"))
                    return
                msg = ""
                guilds = await self.bot.guilds
                msg = str(len(guilds)) + " servers:\n"
                for guild in guilds:
                    msg += guild.name + "\n"
