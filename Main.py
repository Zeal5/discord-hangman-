import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from random_word import randomword


load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
activity = discord.Game(name='hangman')
bot = commands.Bot(intents=intents,command_prefix='!',activity = activity, status = 'hangman')
secret_word = randomword
game_over = True


@bot.event
async def on_ready():
    print("Logged in as", bot.user.name)


@bot.command()
async def start(ctx):
    embed = discord.Embed(title = '****HangMan Bot****',color = 0xe97afa)
    embed.set_thumbnail(url='https://media.istockphoto.com/illustrations/simple-illustration-of-hangman-game-illustration-id1196954772?k=20&m=1196954772&s=612x612&w=0&h=nzsr9bCwxp9xW3dp-nBJeXE7TVGqnWtdJpbaXvEyl3E=')
    global game_over
    global guess_word
    global lives

    
    if game_over == True:
        lives = 7
        guess_word = ''
        embed.description = f'guess the {len(secret_word)} letter word'  
        embed.add_field(name='Word', value='-'*len(secret_word))
        await ctx.send(embed = embed)
        game_over = False
    else:
        in_game = discord.Embed(title='a game is already in progress')
        await ctx.send(embed=in_game)


@bot.command()
async def guess(ctx, alph):
    in_embed = discord.Embed(title = '****HangMan Bot****',color = 0xe97afa)
    in_embed.set_thumbnail(url='https://media.istockphoto.com/illustrations/simple-illustration-of-hangman-game-illustration-id1196954772?k=20&m=1196954772&s=612x612&w=0&h=nzsr9bCwxp9xW3dp-nBJeXE7TVGqnWtdJpbaXvEyl3E=')
    global lives
    global guess_letter
    global guess_word
    global game_over
    new_word = ''
    if game_over == False and len(alph) == 1 :
        guess_letter = ''
        guess_letter = alph
        if alph in guess_word:
            already_guessed = discord.Embed(title=f'{alph} has already been guessed')
            already_guessed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS82eoXDpbD_r7-JxUpKctCLe9J5kQuayAbXw&usqp=CAU')
            await ctx.send(embed=already_guessed)
            return

        elif alph in secret_word:
            in_embed.description=f"{guess_letter} is in the word" 
            guess_word += guess_letter           
            for i in secret_word:
                if i in guess_word:
                    new_word += i
                else:
                    new_word += '-'
            in_embed.add_field(name='Guess', value=new_word , )        

            await ctx.send(embed=in_embed)
            new_word = ''

        else:
            in_embed.description=f'{alph} is not in word'
            in_embed.add_field(name='LIVES LEFT',value=lives-1)
            await ctx.send(embed=in_embed)
            lives += -1
        if set(guess_word) == set(secret_word) :
            game_over = True
            game_won_embed = discord.Embed(title= 'Congratulations',color= 0x096310)
            game_won_embed.description= 'You have Won the Game'
            game_won_embed.set_thumbnail(url='https://image.shutterstock.com/image-vector/hangman-hangwoman-noose-knot-prevention-260nw-1669999099.jpg')
            await ctx.send(embed=game_won_embed )                     
        if lives <= 0:
            game_over = True
            game_loose_embed = discord.Embed(title= 'You Lost',color= 0xFF0000)
            game_loose_embed.set_thumbnail(url='https://t3.ftcdn.net/jpg/02/31/48/22/360_F_231482273_IItIStkPfg9p8EO0yuqC3WSyeys6hPaq.jpg')
            game_loose_embed.description= 'You have Lost the Game, better luck next time'
            await ctx.send(embed=game_loose_embed)

    elif len(alph) >1 :
        wrong_guess_embed=discord.Embed(title= 'you can only guess 1 letter at a time',color= 0xFF0000)
        await ctx.send(embed=wrong_guess_embed)

    else:
        start_embed = discord.Embed(title='No game in progress')
        start_embed.description='type !start to start new game'
        await ctx.send(embed=start_embed)
      
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):

        error_embed = discord.Embed(title='****GENIUS ERROR****')
        error_embed.description='u need to use atleast 1 letter after !guess'
        error_embed.set_thumbnail(url='https://i1.sndcdn.com/artworks-000477842853-3oivr6-t500x500.jpg')
        await ctx.send(embed=error_embed) 
     

bot.run(TOKEN)

