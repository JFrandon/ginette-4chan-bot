from chan import Chan, ChanError
from discord.ext import commands
from discord import Embed
from html2text import html2text

chan = Chan()

HELPSTRING = """Ginette Bot (JFrandon Edition [original code by RF-Studio]):
Prefix: G.
Valid Commands:
    help: displays this message
    echo <string>: displays a the provided sting
    post: displays a random post from 4chan
    post <board>: displays a random post from the specified 4chan board
    disp <thread URL> : displays the thread your enter the URL
"""


@commands.command()
async def echo(ctx, *args):
    await ctx.send(" ".join(args))


@commands.command()
async def hp(ctx):
    await ctx.send(HELPSTRING)


@commands.command()
async def post(ctx, arg="", thread=""):
    try:
        poste = None
        if thread:
            poste = chan.get_random_reply(arg,thread)
        else:
            poste = chan.get_random_post(arg)
        await ctx.send(f"{html2text(poste.get_text())[:250]}{poste.get_img()}")
    except ChanError as e:
        await ctx.send(e.message)

@commands.command()
async def disp(ctx, *args):
    try:
        """get url and display it"""
    except ChanError as e:
        await ctx.send(e.message)

@commands.command()
async def info(ctx, arg=""):
    try:
        await ctx.send(f"Infos : {html2text(chan.get_board(arg).get_info())}")
    except ChanError as e:
        await ctx.send(e.message)