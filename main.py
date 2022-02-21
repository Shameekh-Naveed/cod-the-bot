import os,random
import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
from speech_recognition_module import recognize_speech
from RPS import RPS
import youtube_dl
from youtubesearchpython import VideosSearch
import json
from requests import get


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!",intents=intents)

#------------Bot Starting--------------------------
@client.event
async def on_ready():
    guilds = client.guilds
    print(
        f'{client.user} is connected to the following guild:\n'
        # f'{guild.name}(id: {guild.id})'
    )
    for guild in guilds:
        print(f"{guild.name}")

#--------- Hello command to display a list of available commands-----------------
@client.command()
async def hello(ctx):
    username = str(ctx.author).split("#")[0]
    embedVar = discord.Embed(title="List of Avaiable Commands", description='''Here is a list of currently available commands:
                   
**General Interaction with the Bot:**
    !hello - display a list of available commands
    !bye - a nice lil goodbye message from CodTheBot
    !listen - listens to your audio, converts it into text and sends it to the server
    
**Rock, Papers, Scissors Commands:**
    !playRPS - play a Rock, Paper, Scissors game
    
**TicTacToe Commands:**
    !tictactoe @user1 @user2 - runs a tictactoe game between the tagged users
    !place *n* - marks your choice at the nth value box
    
**Music Commands:**
    !join - CodTheBot joins the vc
    !play *songname* - plays the desired song
    !pause - pause the song
    !resume - resume the song
    !disconnect - CodTheBot leaves the vc
    
**Memes Commands:**
    !meme - displays a random meme from reddit''',color=0xFF0000)

    await ctx.send(f"Hello I am CODtheBOT. You must be {username}")
    await ctx.send(embed=embedVar)
                        
                                     
 #----------------- Bye Command---------------------------------------
@client.command()
async def bye(ctx):
    username = str(ctx.author).split("#")[0]
    

    await ctx.send(f'See you later {username}!')


#----------------Listen Command to listen to audio ,convert it to text and send it to server---
@client.command()
async def listen(ctx):
    username = str(ctx.author).split("#")[0]

    msg = await ctx.send(f'Go on I am listening')
    text = recognize_speech()
    await msg.edit("Hey Everyone!")
    await ctx.send(f'{username} said: {text}')    


#--------------------Rock Paper Scissors Game--------------
@client.command()
async def playRPS(ctx):
    username = str(ctx.author).split("#")[0]
    



    await ctx.send(f'Hey {username} Lets Play. Make your choice')


    button_Rock = Button(emoji="✊")
    button_Paper = Button(emoji="✋")
    button_Scissor = Button(emoji="✌")
    
    async def btn_rock_callback(interaction, custom_id="rock"):


        user2, field, game_stat = RPS(custom_id)

        embedVar = discord.Embed( description=f"You chose Rock\nI choose {user2}", color=0x00ff00)
        await interaction.response.edit_message(content=field, embed=embedVar, view=None)


        embedVar = discord.Embed(title=game_stat["message"], description=game_stat["description"], color=game_stat["color"])
        await ctx.send(embed=embedVar)

    async def btn_paper_callback(interaction, custom_id="paper"):


        user2, field, game_stat = RPS(custom_id)

        embedVar = discord.Embed( description=f"You chose Paper\nI choose {user2}", color=0x00ff00)
        await interaction.response.edit_message(content=field, embed=embedVar, view=None)


        embedVar = discord.Embed(title=game_stat["message"], description=game_stat["description"], color=game_stat["color"])
        await ctx.send(embed=embedVar)

    async def btn_scissor_callback(interaction, custom_id="scissor"):


        user2, field, game_stat = RPS(custom_id)

        embedVar = discord.Embed( description=f"You chose Scissors\nI choose {user2}", color=0x00ff00)
        await interaction.response.edit_message(content=field, embed=embedVar, view=None)


        embedVar = discord.Embed(title=game_stat["message"], description=game_stat["description"], color=game_stat["color"])
        await ctx.send(embed=embedVar)


    view_var = View()
    view_var.add_item(button_Rock)
    view_var.add_item(button_Paper)
    view_var.add_item(button_Scissor)

    start_field= ":right_fist:      :left_fist:"
    await ctx.send(start_field,view=view_var)
    button_Rock.callback = btn_rock_callback
    button_Paper.callback = btn_paper_callback
    button_Scissor.callback = btn_scissor_callback
    
#----------Tic Tac Toe Game------------------------------------------
@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global player1
    global player2
    global turn
    global game_over
    game_over = True
    global count

    if game_over:
        global board
        board = [":white_large_square:"]*9
        game_over = False
        count = 0

        player1 = p1
        player2 = p2

        #Print blank board
        line = ""
        for x in range(len(board)):
            if x==2 or x==5 or x==8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
        #Determine who goes first
        num = random.randint(1,2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        else:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress. Please finish it.")

#----------------Tic Tac Toe Placement Handling ----------------------

@client.command()
async def place(ctx, position: int):
    global turn
    global count


    def checkwin(winning_conditions, mark,board):
        global game_over
        for condition in winning_conditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                game_over = True


    winning_conditions = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6],
]

    if not game_over:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            else:
                mark = ":o2:"
            if 0 < position < 10 and board[position-1] == ":white_large_square:":
                board[position-1] = mark
                count += 1
                     # will try to make this into a function
                line = ""
                for x in range(len(board)):
                    if x==2 or x==5 or x==8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                checkwin(winning_conditions, mark,board)
                if game_over:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    await ctx.send("It's a tie!")
                #Switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1

            else:
                await ctx.send("Please choose an integer between 1 and 9 and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game first.")
        

#----------------Tic Tac Toe Error Handling ----------------------

@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention two players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players i.e. <@playerid>")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


#---------------------------------Music player---------------------------------------


@client.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        
@client.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()
    
@client.command()
async def play(ctx,url):
    ctx.voice_client.stop()
    # FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    # 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}
    vc = ctx.voice_client
    
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        url = VideosSearch(url, limit = 2)
        y=url.result()
        x=y['result'][0]['link']
        print(x)
        info = ydl.extract_info(x, download = False)
        url2 = info ['formats'][0]['url']
        print (url2)
        source = await discord.FFmpegOpusAudio.from_probe(url2)# **FFMPEG_OPTIONS)
        vc.play(source)
        embed_var=discord.Embed(title="Now playing - ", description=y['result'][0]['title'], color=0x00FF00)
        embed_var.set_image(url=y['result'][0]['thumbnails'][0]['url'])
        await ctx.send(embed=embed_var)
        

@client.command()
async def pause(ctx):
    ctx.voice_client.pause()
    await ctx.send("Paused ⏸️")

@client.command()
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.send("Resumed ▶️")
    
    
#----------------- Random Meme Gennerator-----------------------------
    
@client.command()
async def meme(ctx): 
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content)
    meme = discord.Embed(title=f"{data['title']}", color = 0x00FF00)
    meme.set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)
    

client.run(TOKEN)



