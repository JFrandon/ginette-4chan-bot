from chan import Chan, ChanError
from discord.ext import commands
from discord import Embed
from html2text import html2text
import time

chan = Chan()

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
    await ctx.send(" ".join(args))


@commands.command()
async def hp(ctx):
    print(get_time()+'| Help requested')
    await ctx.send(HELPSTRING)


@commands.command()
async def post(ctx, arg=""):
    try:
        print(get_time()+"| Post requested on board : " + arg)
        display_post = chan.get_random_post(arg)
        await ctx.send(f"```{html2text(display_post.get_text())[:500]}```{display_post.get_img()}")
    except ChanError as e:
        await ctx.send(e.message)


@commands.command()
async def info(ctx, arg=""):
    print(get_time() + "| Board " + arg + " info requested")
    try:
        await ctx.send("```"+html2text(chan.get_info(arg))+"```")
    except ChanError as e:
        await ctx.send(e.message)


def get_time():  # getting time
    try:
        t = time.strftime("%Y-%m-%d | %H:%M:%S | ")
        return t
    except TimeoutError:
        print("Error getting time | TIME OUT | ")
