from chan import Chan, ChanError
from discord.ext import commands
import discord
from discord import Embed
from html2text import html2text
import time

chan = Chan()
bot = commands.Bot(command_prefix='G.')

HELPSTRING = """Ginette Bot (JFrandon Edition [original code by RF-Studio]):
Prefix: G.
Valid Commands:
    help: displays this message
    echo <string>: displays a the provided sting
    post: displays a random post from 4chan
    post <board>: displays a random post from the specified 4chan board
    info <board>: get title and description of the specified 4chan board
    info : get url and title of every 4chan board
"""


@commands.command()
async def echo(ctx, *args):
    print(get_time()+'| echo requested : ' + args)
    message = await ctx.send(" ".join(args))
    await message.add_reaction("\U0001F5D1")


@commands.command()
async def hp(ctx):
    print(get_time()+'| Help requested')
    message = await ctx.send(HELPSTRING)
    await message.add_reaction("\U0001F5D1")


@commands.command()
async def post(ctx, b="", t="", p=""):
    try:
        print(get_time()+f"| Post {p} requested on board {b} thread {t} ")
        display_post = chan.get_post(b, t, p)
        message = await ctx.send(f"{display_post.get_uri()} ```{html2text(display_post.get_text())[:1500]}```{display_post.get_img()}")
        await message.add_reaction("\U0001F5D1")
    except ChanError as e:
        await ctx.send(e.message)


@commands.command()
async def info(ctx, arg=""):
    print(get_time() + "| Board " + arg + " info requested")
    try:
        message = await ctx.send("```"+html2text(chan.get_info(arg))+"```")
        await message.add_reaction("\U0001F5D1")
    except ChanError as e:
        await ctx.send(e.message)


def get_time():  # getting time
    try:
        t = time.strftime("%Y-%m-%d | %H:%M:%S | ")
        return t
    except TimeoutError:
        print("Error getting time | TIME OUT | ")


@bot.event
async def on_reaction_trash(reaction, user):
    reaction.message.on_reaction_add()
    print("delete")
