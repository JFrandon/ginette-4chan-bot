from chan import Chan, ChanError
from discord.ext import commands
from discord import Embed
from html2text import html2text
from datetime import datetime

chan = Chan()

HELPSTRING = """Ginette Bot (JFrandon Edition [original code by RF-Studio]):
Prefix: G.
Valid Commands:
    help: displays this message
    echo <string>: displays a the provided sting
    post: displays a random post from 4chan
    post <board>: displays a random post from the specified 4chan board
    info <board>: get title and description of the specified 4chan board
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
        await ctx.send(f"{html2text(display_post.get_text())[:250]}{display_post.get_img()}")
    except ChanError as e:
        await ctx.send(e.message)


@commands.command()
async def info(ctx, arg=""):
    try:
        print(get_time()+"| Board " + arg + " info requested")
        await ctx.send(html2text(chan.get_board(arg).get_info()))
    except ChanError as e:
        await ctx.send(e.message)


class TimeError(Exception):
    message = "Error getting time"


def get_time():  # getting time
    try:
        t = str(datetime.now())
        nt = ""
        for i in range(19):
            nt += t[i]
    except TimeError as e:
        print(e.message)
