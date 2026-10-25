import discord
from discord.ext import commands 
import logging 
from dotenv import load_dotenv
import os
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)
new_role = "Senior"

@bot.event
async def on_ready():
    print(f"We are ready to go in. {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}")

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
]
    
    for word in bad_words:
             if word in message.content.lower():
                 await message.delete()
                 await message.channel.send(f"{message.author.mention} Please refrain from using inappropriate language.")
                 break
    await bot.process_commands(message)

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

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

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=new_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned the role '{new_role}'!")
    else:
        await ctx.send(f"The role '{new_role}' does not exist.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)