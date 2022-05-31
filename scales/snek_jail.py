import naff as dis

import libraries.database as database
from libraries.helperFunctions import isOwner, ownerId

db = database.Database("userids.db")

DBchannels = database.Configuration("Server_VCs", {
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


class Jail(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot: dis.Client = bot
    
    @dis.listen(dis.events.VoiceStateUpdate)
    async def moveUser(event: dis.events.VoiceStateUpdate):
        if event.after != None and check_user(event.after._guild_id, event.after.member.id):
            voiceID = DBchannels.get(event.after._guild_id, 'vc_id')
            await event.after.member.move(voiceID)
    
    @dis.slash_command(name="jail", description="Jail a user")
    @dis.slash_option(
        "user",
        "Who going to Brazil",
        dis.OptionTypes.USER,
        True,)
    async def jail(self, ctx: dis.InteractionContext, user: dis.Member):
        if ctx.author.id == ctx.guild._owner_id or isOwner(ctx):
            if DBchannels.get(ctx.guild.id, 'vc_id') == 0:
                await ctx.send("No voice channel set for this server")
            elif user.bot:
                await ctx.send("Bots can't be jailed")
            elif user.id == ctx.guild._owner_id or user.id in ownerId:
                await ctx.send("Sorry but you can not jail this person they have an infinite use get out of jail free card in this server.", ephemeral=False)
            elif check_user(ctx.guild_id, user.id):
                await ctx.send("This user is already in jail", ephemeral=False)
            else:
                add_user(ctx.guild_id, user.id)
                await ctx.send(F"You have banished {user.user.mention} to <#{str(DBchannels.get(ctx.guild.id, 'vc_id'))}>", ephemeral=False)
        else:
            await ctx.send("You don't have the power to do that", ephemeral=False)
    
    @dis.slash_command(name="unjail", description="Unjail a user")
    @dis.slash_option(
        "user",
        "Who's being released from Brazil",
        dis.OptionTypes.USER,
        True,)
    async def unjail(self, ctx: dis.InteractionContext, user: dis.Member):
        if ctx.author.id == ctx.guild._owner_id or isOwner(ctx):
            if DBchannels.get(ctx.guild.id, 'vc_id') == 0:
                await ctx.send("No voice channel set for this server")
            elif check_user(ctx.guild_id, user.id):
                remove_user(ctx.guild_id, user.id)
                await ctx.send(F"You have released {user.user.mention} from jail", ephemeral=False)
            else:
                await ctx.send(f"{user.user.mention}is not in jail at the moment", ephemeral=False)
        else:
            await ctx.send("You don't have the power to do that", ephemeral=False)
    
    @dis.slash_command(name="setjail", description="Set the voice channel for the jail")
    @dis.slash_option(
        "channel",
        "The voice channel to be used for the jail",
        dis.OptionTypes.CHANNEL,
        dis.ChannelTypes.GUILD_VOICE,
        True,)
    async def setjail(self, ctx: dis.InteractionContext, channel: dis.channel.VoiceChannel):
        if ctx.author.id == ctx.guild._owner_id or isOwner(ctx):
            DBchannels.set(ctx.guild.id, 'vc_id', channel.id)
            await ctx.send(f"The jail channel has been set to {channel.mention}", ephemeral=False)
        else:
            await ctx.send("You don't have the power to do that", ephemeral=False)

def setup(bot):
    Jail(bot)