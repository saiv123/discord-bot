import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


from libraries.helperFunctions import isOwner, add_to_embed
from libraries.helperFunctions import gen_rps_matrix, format_matrix, list_god

RPS_HARD_CAP = 6

def setup(bot):
    bot.add_cog(rps_commands(bot))

class rps_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='rps',
        description='Play rock-paper-scissors',
        options=[
            create_option(
                name='level',
                description='Add more symbols to the classic game',
                option_type=4,
                required=False
            )
        ]
    )
    async def rps(self, ctx: SlashContext, *, level=1,guild_ids = [648012188685959169]):
        if level > RPS_HARD_CAP and not isOwner(ctx):
            msg = add_to_embed('Level too high!', f'Sorry, but even though the code for it exists, why would you ever want to play rps-{level*2+1}???')[0]
            msg.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=msg, hidden=True)
            return

        ctx.defer()
        symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']
        
        # Extend symbol names if necessary
        for i in range(len(symbol_names), level*2+5):
            symbol_names.append('item'+str(i))

        # Generate matrix
        matrix = gen_rps_matrix(level)

        # Ask for user choice
        color = None

        embed = add_to_embed(f'{ctx.author.name}\'s RPS','Pick an option:\nrules'+'\n'.join(symbol_names[:level*2+1]))[0]
        color = embed.color
        await ctx.send(embed=embed)


        # Get user choice
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check,timeout=1*60)
        except:
            embed = add_to_embed(f'{ctx.author.name}\'s RPS','Awww, don\'t leave me hangin\'')[0]
            embed.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return
        freeform = msg.content.lower().replace(' ','_').replace('\n','')

        # Process winner
        mlo = getClosestFromList(['rules']+symbol_names,freeform)
        output = ''
        if 'rules' in mlo:
            output = ' \n'.join(format_matrix(matrix, symbol_names))
        elif distance(freeform, mlo) >= len(freeform)*0.3: #If the most likely option is more than 30% wrong, hassle
            output = 'No option recognized! Your choices are: '+'\n'.join(['rules']+symbol_names[:level*2+1])
        else:
            choice = symbol_names.index(getClosestFromList(symbol_names, freeform))
            computer_choice = random.randint(0, len(matrix[0])-1)

            winner = matrix[choice][computer_choice]
            if winner == 0:
                output = "Its a draw! Better luck next time"
            elif winner == 1:
                output = "You win. Nice job. 🥳"
            elif winner == 2:
                output = "I win ;) Better luck next time"
            output = output+"\n\nYou chose "+ symbol_names[choice]+"\nI chose "+symbol_names[computer_choice]

        embed = add_to_embed(f'{ctx.author.name}\'s RPS', output)[0]
        if color != None: embed.color = color
        embed.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='rpsc',
        description='Play rock-paper-scissors',
        options=[
            create_option(
                name='user',
                description='Ping who you want to challenge',
                option_type=6,
                required=False
            ),
            create_option(
                name='level',
                description='Add more symbols to the classic game',
                option_type=4,
                required=False
            )
        ],

    )
    async def rpsc(self, ctx: SlashContext, user:discord.User=None, level:int=1, guild_ids = [648012188685959169]):
        if level > RPS_HARD_CAP and not isOwner(ctx):
            msg = add_to_embed('Level too high!', f'Sorry, but even though the code for it exists, why would you ever want to play rps-{level*2+1}???')[0]
            msg.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=msg, hidden=True)
            return

        symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']
        ctx.defer()

        # Extend symbol names if necessary
        for i in range(len(symbol_names),level*2+5):
            symbol_names.append('item'+str(i))

        # Generate matrix
        matrix = gen_rps_matrix(level)

        msg = 'You are challenging '+user.name+' to rock-paper-scissors'
        if level > 1:
            msg = msg+'-'+str(level*2+1)

        embed = add_to_embed(f'Your challenge to {user.name}',msg+'\nCheck your DMs!')[0]
        embed.set_footer(text='Challenge sent by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        def get_check(user):
            def check(msg):
                return msg.author == user and msg.channel == user.dm_channel
            return check

        async def get_response(_user, title='RPSC', timeout=10*60, opener=''):
            choice = symbol_names[0]
            i = 0
            while i < 3:
                i += 1
                for msg in add_to_embed(title, f'{opener}Your choices are '+', '.join(symbol_names[:2*level+1]+['rules','abort'])):
                    await _user.send(embed=msg)
                opener = ''

                try:
                    msg = await bot.wait_for('message', check=get_check(_user),timeout=timeout)
                except:
                    await _user.send(embed=add_to_embed(title, f'Awww, {_user.name} don\'t leave me hangin\'')[0])
                    return -1 # Abort challenge if you don't send an answer

                response = msg.content.lower().replace(' ','_').replace('\n','')
                choice = getClosestFromList(['abort','rules']+symbol_names,response.lower())
                if distance(response, choice) >= len(response)*0.3:
                    await _user.send(embed=add_to_embed(choice, 'No option recognized, try again'))

                if 'abort' in choice.lower():
                    return -1

                if 'rules' in choice.lower():
                    for msg in add_to_embed(title, ' \n'.join(format_matrix(matrix, symbol_names))):
                        await _user.send(embed=msg)
                    i -= 1
                else: # If neither rules or abort, it is correct
                    break
            return choice


        # Get your response
        your_choice = await get_response(ctx.author, title=f'Your challenge to {user.name}')
        if your_choice == -1:
            await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', 'Challenge cancelled!')[0])
            await ctx.channel.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', 'Challenge cancelled!')[0])
            return
        your_choice = symbol_names.index(your_choice)
        await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}',f'You chose {symbol_names[your_choice]}')[0])

        # Get other person's response
        #await user.send(embed=add_to_embed('Rock-Paper-Scissors Challenge!', f'{ctx.message.author.name} has challenged you to rock-paper-scissors-'+str(level*2+1) if level > 1 else '')[0])
        enemy_choice = await get_response(user, title=f'{ctx.author.name}\'s challenge', opener=f'{ctx.author.name} has challenged you to rock-paper-scissors-'+str(level*2+1) if level > 1 else '')
        if enemy_choice == -1:
            embed = add_to_embed(f'{ctx.author.name}\'s challenge', 'Challenge cancelled!')[0]
            await user.send(embed=embed)
            await ctx.channel.send(embed=embed)
            await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', 'Challenge cancelled by opponent')[0])
            return
        enemy_choice = symbol_names.index(enemy_choice)
        await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', f'You chose {symbol_names[enemy_choice]}')[0])

        msg = ""

        # Display results
        msg = f'{ctx.author.name} chose {symbol_names[your_choice]}'
        msg += f'\n{user.name} chose {symbol_names[enemy_choice]}'

        winner = matrix[enemy_choice][your_choice]
        if winner == 0:
            await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.author.name,'You')+'\nThe bout ended in a draw')[0])
            await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', msg.replace(user.name,'You')+'\nThe bout ended in a draw')[0])
            msg += '\nThe bout ended in a draw'
        elif winner == 1:
            await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.author.name,'You')+'\nYou won 🥳')[0])
            await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', msg.replace(user.name,'You')+'\nYou lost.')[0])
            msg += f'\n{ctx.author.name} won! 🥳'
        elif winner == 2:
            await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.author.name,'You')+'\nYou lost')[0])
            await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', msg.replace(user.name,'You')+'\nYou won 🥳')[0])
            msg += f'\n{user.name} won. Nice job. 🥳'

        embed = add_to_embed(f'{ctx.author.name}\'s challenge to {user.name}', msg)[0]
        embed.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)