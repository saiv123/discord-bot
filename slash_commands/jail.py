import libraries.database as database

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import isOwner, ownerId

db = database.Database("userids.db")

channels = database.Configuration("Server_VCs", {
    "vc_id": 0
}, db.path)

# server_id = 99999
# channels.get(server_id, 'vc_id')
# channels.set(server_id, 'vc_id', vc_id) #ON THE SET COMMAND FOR VC RUN THIS


def get_table(server_id: int):
    server_name = f"Server_{server_id}"
    try:
        table_id = [x.name for x in db.fetch_tables()].index(server_name)
        return db.fetch_tables()[table_id]
    except ValueError:
        return db.create_table(server_name, {
            'user_id': int
        })

def add_user(server_id: int, user_id: int):
    table = get_table(server_id)
    user_id = str(user_id)
    table.add_entry({'user_id': user_id})

def remove_user(server_id: int, user_id: int):
    table = get_table(server_id)
    user_id = str(user_id)
    table.remove_entry(f'user_id={user_id}')

def check_user(server_id: int, user_id: int):
    table = get_table(server_id)
    user_id = str(user_id)
    return len(table.fetch_entries(f'user_id={user_id}')) > 0

if __name__ == '__main__':
    table = get_table(1)
    print(table.fetch_columns())
    add_user(1, 69)
    add_user(1, 70)
    add_user(1, 69)
    print(table.fetch_entries())
    print(f'69 in table: {check_user(1, 69)}')
    remove_user(1, 69)
    print(table.fetch_entries())
    print(f'69 in table: {check_user(1, 69)}')

def setup(bot):
    bot.add_cog(jail(bot))


class jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    jail_options = [
        {"name": "user", "description": "Person to jail or unjail", "type": 6, "required": True}
    ]

    vc_options = [
        {"name": "voicechat", "description": "What vc do you want to make jail", "type": 7, "required": True}
    ]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after and check_user(member.guild.id, member.id):
            voiceID = channels.get(member.guild.id, 'vc_id')
            voiceChan = member.guild.get_channel(voiceID)
            await member.mover_to(voiceChan)

    @cog_ext.cog_slash(name="jail", options=jail_options, description="Put someone in jail")
    async def jail(self, ctx: SlashContext, user: discord.User = None):
        if ctx.author.id == ctx.guild.owner_id or isOwner(ctx):
            if channels.get(ctx.guild.id, 'vc_id')== 0:
                await ctx.send("You must set a vc to jail people to first")
            elif user.bot:
                await ctx.send("Sorry you cant jail a bot.", hidden=False)
            elif user.id == ctx.guild.owner_id or user.id in ownerId:
                await ctx.send("Sorry but you can not jail this person they have an infinite use get out of jail free card in this server.", hidden=False)
            elif check_user(ctx.guild.id, user.id):
                await ctx.send("This user is already in jail", hidden=False)
            else:
                add_user(ctx.guild.id, user.id)
                await ctx.send("You have banished "+user.mention+" to <#"+str(channels.get(ctx.guild.id, 'vc_id'))+">", hidden=False)
        else:
            await ctx.send("You do not have permitions to use this command", hidden=False)

    @cog_ext.cog_slash(name="unjail", options=jail_options, description="Remove someone from jail")
    async def unjail(self, ctx: SlashContext, user: discord.User = None):
        if ctx.author.id == ctx.guild.owner_id or isOwner(ctx):
            if channels.get(ctx.guild.id, 'vc_id')== 0:
                await ctx.send("You must set a vc to unjail people from first")
            elif check_user(ctx.guild.id, user.id):
                remove_user(ctx.guild.id, user.id)
                await ctx.send("You have unjailed "+user.mention, hidden=False)
            else:
                await ctx.send(user.mention+"is not in jail at the moment", hidden=False)
        else:
            await ctx.send("You do not have permitions to use this command", hidden=False)

    @cog_ext.cog_slash(name="jailvc", options=vc_options, description="Set the jail vc")
    async def jailvc(self, ctx: SlashContext, vc: discord.Channel = None):
        if ctx.author.id == ctx.guild.owner_id or isOwner(ctx):
            vcID = vc.id
            channels.set(ctx.guild.id, 'vc_id', vcID)
            await ctx.send("Channel set to <#"+srt(vcID)+">")
        else:
            await ctx.send("You do not have permitions to use this command", hidden=False)
