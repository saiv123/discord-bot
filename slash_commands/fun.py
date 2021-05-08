import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import isOwner, splitLongStrings, add_to_embed
from libraries.helperFunctions import checkAuthSerers
from libraries.helperFunctions import RgbToHex, HexToRgb
import random
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

def setup(bot):
    bot.add_cog(fun_commands(bot))

class fun_commands(commands.Cog):
    SPACE_LEN_HARD_CAP = 4000
    MAXROLLS = 20
    MAXSIDES = 100
    SHOULDI_PHRASES = [
        'Yes! Go $',
        'No, it won\'t work.',
        'Hmmm, $ might be a fine idea',
        'Unclear, consider rewording "/"',
        'I don\'t know, ask someone else about $'
    ]

    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='space',
        description='Spread a message',
        options=[
            create_option(
                name='message',
                description='What\'s gotta be spread',
                option_type=3,
                required=True
            ),
            create_option(
                name='amount',
                description='What\'s gotta be spread',
                option_type=4,
                required=False
            ),
        ]
    )
    async def space(self, ctx: SlashContext, message:str='', amount:int=1):
        exp_len = (len(message)-1)*amount + len(message)
        if not isOwner(ctx) and exp_len >= SPACE_LEN_HARD_CAP:
            await ctx.send('That message would be {0} characters, waaaay higher than the limit of {1}. Chill.'.format(exp_len, SPACE_LEN_HARD_CAP))
            return

        to_send = (' '*max(1, amount)).join(message)
        for message in splitLongStrings(to_send):
            await ctx.send(message)

    # TODO: add cooldown of 60s after 3 calls
    @cog_ext.cog_slash(name='color',
        description='Get information about a color',
        options=[
            create_option(
                name='input',
                description='A color as hex, rgb, or cmyk',
                option_type=3,
                required=True
            )
        ],
    )
    async def color(self, ctx: SlashContext, input:str=''):
        try:
            color_dict = apis.getColor(input)
            embed = apis.colorDictToEmbed(color_dict)
            embed.set_author(name="[See It Here]",url=color_dict['url'])
            embed.set_footer(text='Color picked by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("The given color is incorrect. Enter it in Hex, RGB, or CMYK form")

    @cog_ext.cog_slash(name='roll',
        description='Roll a dice',
        options=[
            create_option(
                name='dice',
                description='The type of dice or compound dice',
                option_type=3,
                required=False
            )
        ],

    )
    async def roll(self, ctx: SlashContext, dice:str='1d6'):
        if isOwner(ctx): ctx.defer() # I solemnly swear that I am up to no good

        dice = dice.upper()
        r_data = []

        print(dice)

        async def senderr(msg=''):
            msg = f'\n{msg}' if len(msg) > 0 else ''
            embed = discord.Embed(title='Input was Invalid', description=f'The command was used incorrectly it is used like `/roll` or `/roll 2d4`{msg}')
            embed.set_footer(text=f'Command used inproperly by: {ctx.author.name} (args: {dice})', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        def rollone(rolls, sides):
            total, txt = 0, ""
            for i in range(rolls):
                x = random.randint(1,sides)
                txt += f'{x}, '
                total += x
            return total, txt[:-2] if rolls > 0 else ""

        if(dice.find('D') == -1):
            try:
                r_data = [int(dice), 6]
            except ValueError:
                await senderr()
                return
        else:
            try:
                r_data = [int(x) for x in dice.split('D')]
            except ValueError:
                await senderr()
                return

        dice = 'd'.join([str(x) for x in r_data])
        grand_total, msg = 0, ''
        while len(r_data) > 1:
            rolls, sides = r_data[:2]

            if isOwner(ctx) or (0 < rolls <= MAXROLLS and 1 < sides <= MAXSIDES):
                total, out = rollone(rolls, sides)
                grand_total += total

                out = f'{rolls}d{sides}: {out}'

                # add dice total on if this isn't the last iteration
                if len(r_data) > 2 and rolls > 1: out = f'{out} (total: {total})'

                # add to msg with fenceposting
                msg = f'{msg}\n{out}' if len(msg) > 0 else out

                # shorten list
                r_data.pop(0)
                r_data[0] = total
            else:
                await senderr(f'{msg}\nYou have reached the limits. Make sure you roll less than {MAXROLLS} dice and each dice has less than {MAXSIDES} sides')
                return

        embed = discord.Embed(title=str(dice), description=f'{msg}\n\nTotal: {total}', colour=imgutils.randomSaturatedColor())
        embed.set_footer(text=f'{dice} was rolled by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    ################################
    ###Commands to make you unsad###
    ################################

    #up date to how the command will work, it will be limited to onnce ever 24 hours, but will always send the quote even if it does join the vc
    #play / do something depending on if the user is in a voice channel or not
    @cog_ext.cog_slash(name='sad', description='Makes you unsad' )
    async def sad(self, ctx: SlashContext):
        user = bot.get_user(ctx.author.id)
        await user.send("Hey i see you have used the sad command, you are loved just know that :heart:")
        if checkAuthSerers(ctx):
            try:
                channel = ctx.author.voice.channel
                await channel.connect()

                #sends muic
                embed = add_to_embed('Time to unsad yourself','Music you can listen too:\n[Sad playlist 1](https://www.youtube.com/playlist?list=PLzSGJo-pe00ka90V3cFrEjCCJKROnHCMj)\n[Sad Playlist 2](https://www.youtube.com/playlist?list=PLzSGJo-pe00nNRlyDb8eJ4zSRXnAtevO6)\nHope you feel better from Sai.')[0]
                embed.set_footer(text='Unsading ' + ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await ctx.send("https://tenor.com/view/hug-virtual-hug-hug-sent-gif-5026057")

                #leaving the voice channel
                await ctx.voice_client.disconnect()

            except AttributeError as e:
                #this is what it will do if user is not in vc
                print("user is not in a voice channel, reverting to text for unsadening user")
                quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
                quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
                await ctx.send(embed=quote)
        else:
            #this is what it will do if user is not in trusted server
            quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
            quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
            await ctx.send(embed=quote)

    @cog_ext.cog_slash(
        name='shouldI',
        description='Ask my a should I question and i will tell you the answer.',
        options=[
            create_option(
                name = 'msg',
                description = 'Ask a question!',
                option_type = 3,
                required = True
            )
        ]
    )
    async def shouldI(self, ctx: SlashContext, msg: str):
        msg = " "+msg+" "
        # msg = ' '.join(msg)
        phrases = ['Yes! Go $','No, it won\'t work.','Hmmm, $ might be a fine idea','Unclear, consider rewording "/"','I don\'t know, ask someone else about $']
        embed = discord.Embed(title='Should I...', description='{}\n{}'.format(msg, random.choice(phrases).replace('/', msg)))
        embed.set_footer(text='Asked by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)