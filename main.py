import discord
from discord.ext import commands 
from discord import app_commands
from collections import deque
import logging 
from dotenv import load_dotenv
import os
import random
import datetime
import asyncio


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)
bot.remove_command('help')
new_role = "Member"

@bot.event
async def on_ready():
    print(f"We are ready to go in. {bot.user.name}")

#------Welcome & getting to know------#

#message send when the bot join
@bot.event
async def on_guild_join(guild):
    channel = None

    for ch in guild.text_channels:
        if ch.permissions_for(guild.me).send_messages:
            channel = ch
            break
    if channel is None:
        return
    embed = discord.Embed(
        title="👋 Hi! I'm Nyle!",
        description=(
            f"Thanks for adding me to **{guild.name}**!\n"
            "My prefix is `?`\n"
            "I'm ready to help. Use `?help` to see all my commands."
        ),
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Your server assistant")
    await channel.send(embed=embed)

#sending message to the user itself in dm
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}")

#saying Hi to the member
@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

#assigning role
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=new_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned the role '{new_role}'!")
    else:
        await ctx.send(f"There is no role available.")

#removing role
@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=new_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been removed from the role '{new_role}'!")
    else:
        await ctx.send(f"You do not have a role to remove.")

#getting to know the user info
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title="User Information",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(
        name="Username",
        value=member.name,
        inline=True
    )
    embed.add_field(
        name="Display Name",
        value=member.display_name,
        inline=True
    )
    embed.add_field(
        name="Account Created",
        value=discord.utils.format_dt(member.created_at, style="F"),
        inline=False
    )
    embed.add_field(
        name="Joined Server",
        value=discord.utils.format_dt(member.joined_at, style="F"),
        inline=False
    )
    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    embed.add_field(
        name=f"Roles ({len(roles)})",
        value=", ".join(roles) if roles else "No roles",
        inline=False
    )
    embed.set_footer(
        text=f"Requested by {ctx.author.display_name}"
    )
    await ctx.send(embed=embed)

#getting to know the server info
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"{guild.name} - Server Information",
        color=discord.Color.blurple()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(
        name="Server Owner",
        value=guild.owner.mention,
        inline=True
    )
    embed.add_field(
        name="Members",
        value=guild.member_count,
        inline=True
    )
    embed.add_field(
        name="Channels",
        value=len(guild.channels),
        inline=True
    )
    embed.add_field(
        name="Roles",
        value=len(guild.roles),
        inline=True
    )
    embed.add_field(
        name="Created",
        value=discord.utils.format_dt(guild.created_at, style="F"),
        inline=False
    )
    embed.set_footer(
        text=f"Requested by {ctx.author.display_name}"
    )
    await ctx.send(embed=embed)

#------Restrictions------#

#restricted words
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bad_words = [
    "shit",
    "fuck",
    "bitch",
    "asshole",
    "bastard",
    "damn",
    "hell",
    "crap",
    "dick",
    "piss",
    "bullshit",
    "wtf",
    "stfu",
    "motherfucker",
    "fucking",
    "fucker",
    "fucked",
    "dumbass",
    "jackass",
    "smartass",
    "dipshit",
    "prick",
    "jerk",
    "moron",
    "idiot",
    "sonofabitch",
    "dammit",
    "goddamn",
    "arse",
    "arsehole",
    "bollocks",
    "bugger",
    "bloody",
    "wanker",
    "twat",
    "slut",
    "whore",
    "douchebag",
    "douche",
    "scumbag",
    "shithead",
    "shitface",
    "asshat",
    "asswipe",
    "crappy",
    "fucker",
    "lee",
    "mmsp",
    "nlmt",
    "kmkl",
    "nigga",
    "nigger",
    "nigera"
    "nihha"
]
    
    for word in bad_words:
             if word in message.content.lower():
                 await message.delete()
                 await message.channel.send(f"{message.author.mention} Please refrain from using inappropriate language.")
                 break
    await bot.process_commands(message)

#Lists of commands
@bot.command()
async def help(ctx):
    embed = discord.Embed(
            title =f"Here are the command lists!", color=discord.Color.blurple())
    embed.add_field(

        name="🎮 Games",

        value=(
            "`?guess` — play a guessing game\n"
            "`?ttt` — play tic tac toe"
        ),
        inline=False
    )
    embed.add_field(
        
                name="🛠️ Utility",
        
                value=(
                    "`?assign` - assign a role\n"
                    "`?unassign` — remove role\n"
                    "`?serverinfo` — server info\n"
                    "`?userinfo1` — user info\n"
                    "`?poll` — make a poll"  
                ),
                inline=False
            )
    embed.add_field(
        
                name="🛡️ Moderations",
        
                value=(
                    "`?timeout @user #time_in_min #reason` — assign a role\n"
                    "`?ban @user #reason` — remove role\n"
                    "`?kick @user #reason` — server info\n"
                ),
                inline=False
            )

    help_message = await ctx.send(embed=embed)

#------Games------#

#guess_game
@bot.command()
async def guess(ctx):
     guess_number = random.randint(1, 100)
     await ctx.send("Choose a number between 1 and 100 and type 505 for hint!")
     for index in range(3):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        answer = await bot.wait_for("message", check=check)
        guess = int(answer.content)
        if guess == 505:
            await ctx.send(f"Hint: The number is between {max(1, guess_number - 10)} and {min(100, guess_number + 10)}")
        elif guess == guess_number:
            await ctx.send("Congratulations! You guessed the number!")
        elif guess > guess_number:
            await ctx.send("Your guess is too high!")
            await ctx.send(f"You have {2 - index} guess left.")
        elif guess < guess_number:
            await ctx.send("Your guess is too low!")
            await ctx.send(f"You have {2 - index} guess left.")
     await ctx.send(f"The number was {guess_number}. Better luck next time!")

#tic-tac-toe
games = {}
@bot.command()
async def ttt(ctx, opponent: discord.Member):

    if opponent == ctx.author:
        await ctx.send("❌ You can't play against yourself!")
        return

    if opponent.bot:
        await ctx.send("❌ You can't play against a bot!")
        return

    if ctx.channel.id in games:
        await ctx.send("❌ There is already a game running in this channel!")
        return

    games[ctx.channel.id] = {
        "player1": ctx.author,
        "player2": opponent, 
        "turn": ctx.author,
        "board": ["1️⃣", "2️⃣", "3️⃣",
                  "4️⃣", "5️⃣", "6️⃣",
                  "7️⃣", "8️⃣", "9️⃣"]
    }

    await send_board(ctx)


async def send_board(ctx):
    game = games[ctx.channel.id]

    board = game["board"]

    board_text = (
        f"{board[0]} │ {board[1]} │ {board[2]}\n"
        "─────────────\n"
        f"{board[3]} │ {board[4]} │ {board[5]}\n"
        "─────────────\n"
        f"{board[6]} │ {board[7]} │ {board[8]}"
    )

    if game["turn"] == game["player1"]:
        symbol = "❌"
    else:
        symbol = "⭕"

    embed = discord.Embed(
        title="🎮 Tic-Tac-Toe",
        description=board_text,
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Players",
        value=(
            f"❌ {game['player1'].mention}\n"
            f"⭕ {game['player2'].mention}"
        ),
        inline=True
    )

    embed.set_footer(
        text="Use ?move 1-9 to make your move"
    )

    await ctx.send(embed=embed)
    await ctx.send(f"Its your turn!{game['turn'].mention}")

@bot.command()
async def move(ctx, position: int):

    if ctx.channel.id not in games:
        await ctx.send(
            "❌ There is no Tic-Tac-Toe game running."
        )
        return

    game = games[ctx.channel.id]

    if ctx.author not in [
        game["player1"],
        game["player2"]
    ]:
        await ctx.send(
            "❌ You aren't part of this game!"
        )
        return

    if ctx.author != game["turn"]:
        await ctx.send(
            "❌ It's not your turn!"
        )
        return

    if position < 1 or position > 9:
        await ctx.send(
            "❌ Choose a number between **1 and 9**."
        )
        return

    index = position - 1

    if game["board"][index] in ["❌", "⭕"]:
        await ctx.send(
            "❌ That position is already taken!"
        )
        return

    if ctx.author == game["player1"]:
        symbol = "❌"
    else:
        symbol = "⭕"

    game["board"][index] = symbol

    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_combinations:

        if (
            game["board"][a] == symbol
            and game["board"][b] == symbol
            and game["board"][c] == symbol
        ):

            board_text = (
                f"{game['board'][0]} │ {game['board'][1]} │ {game['board'][2]}\n"
                "─────────────\n"
                f"{game['board'][3]} │ {game['board'][4]} │ {game['board'][5]}\n"
                "─────────────\n"
                f"{game['board'][6]} │ {game['board'][7]} │ {game['board'][8]}"
            )

            embed = discord.Embed(
                title="🏆 Tic-Tac-Toe — Game Over!",
                description=board_text,
                color=discord.Color.green()
            )

            embed.add_field(
                name="Winner",
                value=f"🎉 {ctx.author.mention} **wins!**",
                inline=False
            )

            await ctx.send(embed=embed)

            del games[ctx.channel.id]
            return

    if all(
        space in ["❌", "⭕"]
        for space in game["board"]
    ):

        board_text = (
            f"{game['board'][0]} │ {game['board'][1]} │ {game['board'][2]}\n"
            "─────────────\n"
            f"{game['board'][3]} │ {game['board'][4]} │ {game['board'][5]}\n"
            "─────────────\n"
            f"{game['board'][6]} │ {game['board'][7]} │ {game['board'][8]}"
        )

        embed = discord.Embed(
            title="🤝 Tic-Tac-Toe — Draw!",
            description=board_text,
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Result",
            value="Nobody wins this time!",
            inline=False
        )

        await ctx.send(embed=embed)

        del games[ctx.channel.id]
        return

    if game["turn"] == game["player1"]:
        game["turn"] = game["player2"]
    else:
        game["turn"] = game["player1"]

    await send_board(ctx)

@bot.command()
async def end(ctx):

    if ctx.channel.id not in games:
        await ctx.send("❌ There is no Tic-Tac-Toe game running.")
        return

    game = games[ctx.channel.id]

    if ctx.author not in [game["player1"], game["player2"]]:
        await ctx.send("❌ You aren't part of this game!")
        return

    if "end_requests" not in game:
        game["end_requests"] = set()

    if ctx.author in game["end_requests"]:
        await ctx.send(
            "⚠️ You already requested to end the game. "
            "Waiting for the other player."
        )
        return

    game["end_requests"].add(ctx.author)

    if len(game["end_requests"]) == 2:

        embed = discord.Embed(
            title="🛑 Tic-Tac-Toe — Game Ended",
            description="Both players agreed to end the game.",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Result",
            value="🤝 The game ended by mutual agreement.",
            inline=False
        )

        await ctx.send(embed=embed)

        del games[ctx.channel.id]

    else:
        await ctx.send(
            f"🛑 {ctx.author.mention} wants to end the game.\n"
            f"Waiting for the other player to type `?end`."
        )
#poll
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title = question, description="Choose one!", color=discord.Color.blurple())
    embed.set_footer(text="Poll ends in 10 mins")
    poll_message = await ctx.send(embed=embed)

    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
    await asyncio.sleep(600)

    poll_message = await ctx.channel.fetch_message(poll_message.id)

    yes_votes = 0
    no_votes = 0

    for reaction in poll_message.reactions:

        if str(reaction.emoji) == "👍":
            yes_votes = reaction.count - 1

        elif str(reaction.emoji) == "👎":
            no_votes = reaction.count - 1

    if yes_votes > no_votes:
        result = "🏆 **YES wins!**"
        color = discord.Color.green()

    elif no_votes > yes_votes:
        result = "🏆 **NO wins!**"
        color = discord.Color.red()

    else:
        result = "🤝 **It's a tie!**"
        color = discord.Color.gold()

    result_embed = discord.Embed(
        title="📊 Poll Results",
        description=f"**{question}**",
        color=color
    )

    result_embed.add_field(
        name="👍 Yes",
        value=f"{yes_votes} vote(s)",
        inline=True
    )

    result_embed.add_field(
        name="👎 No",
        value=f"{no_votes} vote(s)",
        inline=True
    )

    result_embed.add_field(
        name="Result",
        value=result,
        inline=False
    )

    result_embed.set_footer(text="Poll closed after 10 minutes.")

    await poll_message.edit(embed=result_embed)

#------Music------#



#------Moderations------#

#deleting messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{ctx.author.mention} Deleted {amount} messages.", delete_after=3)

#time out
@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
    if member == ctx.author:
        return await ctx.reply("You can't timeout yourself.")
    
    if member == ctx.guild.me:
        return await ctx.reply("I can't timeout myself.")

    try:
        await member.send(
            f"🔨 **You have been timed out in {ctx.guild.name}**\n\n"
            f"**Reason:** {reason}\n"
            f"**Duration:** {minutes} minutes\n"
        )
    except discord.Forbidden:
        pass 

    duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)

    embed = discord.Embed(
        title="Member Timed Out",
        description=f"{member.mention} has been timed out.",
        color=discord.Color.orange()
    )

    embed.add_field(name="Duration", value=f"{minutes} minutes")
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=ctx.author.mention)

    await ctx.reply(embed=embed, delete_after = 10)

#kicking
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    if member == ctx.author:
        return await ctx.reply("You can't kick yourself.")
    
    if member == ctx.guild.me:
        return await ctx.reply("I can't kick myself.")

    try:
        await member.send(
            f"🔨 **You have been kicked out in {ctx.guild.name}**\n\n"
            f"**Reason:** {reason}\n"
        )
    except discord.Forbidden:
        pass 

    await member.kick(reason=reason)

    embed = discord.Embed(
        title="Member has been kicked",
        description=f"{member.mention} has been kicked out.",
        color=discord.Color.orange()
    )

    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=ctx.author.mention)

    await ctx.reply(embed=embed, delete_after = 10)

#banning
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if member == ctx.author:
        return await ctx.reply("You can't ban yourself.")
    
    if member == ctx.guild.me:
        return await ctx.reply("I can't ban myself.")

    try:
        await member.send(
            f"🔨 **You have been banned from {ctx.guild.name}**\n\n"
            f"**Reason:** {reason}\n"
        )
    except discord.Forbidden:
        pass 

    await member.ban(reason=reason)

    embed = discord.Embed(
        title="Member has been banned",
        description=f"{member.mention} has been banned out.",
        color=discord.Color.orange()
    )

    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=ctx.author.mention)

    await ctx.reply(embed=embed, delete_after = 10)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
