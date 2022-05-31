import naff as dis

class Move(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot: dis.Client = bot
    
    @dis.slash_command(name="move", description="Moves you to Sai", scopes=[648012188685959169])
    async def move(self, ctx: dis.InteractionContext):
        canUse = False
        ListOfRoles = ctx.author.roles
        for x in ListOfRoles:
            if x.id == 648012394278158341 or x.id == 670071475914539022:
                canUse = True
        
        if canUse:
            user = ctx.guild.get_member(240636443829993473)
            try:
                channel = ctx.author.voice.channel
                otherchannel = user.voice.channel
                # move logic
                if channel.id == otherchannel.id:
                    await ctx.send("You both are in the same channel cant move you.", ephemeral=True)
                else:
                    await ctx.author.move(otherchannel.id)
                    await ctx.send("Boop Found him moving you to the vc Sai is in.", ephemeral=True)
            except e:
                # this is what it will do if user is not in vc
                await ctx.send("Sorry but you have to be in a vc to use this command\nOr Sai is not in a VC", ephemeral=True)
        else:
            await ctx.send("You are not permitted to use this command!!", ephemeral=True)
def setup(bot):
    Move(bot)