from chan import Chan, ChanError
from reactions import with_reactions, register_post_reactions
from discord.ext import commands
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
@with_reactions()
async def echo(ctx, *args):
    print(get_time()+'| echo requested : ' + " ".join(args))
    return await ctx.send(" ".join(args))


@commands.command()
@with_reactions()
async def hp(ctx):
    print(get_time()+'| Help requested')
    return await ctx.send(HELPSTRING)


@commands.command()
@with_reactions(True)
async def post(ctx, b="", t="", p=""):
    try:
        print(get_time()+f"| Post {p} requested on board {b} thread {t} ")
        display_post = chan.get_post(b, t, p)
        message = await ctx.send(f"{display_post.get_uri()} ```{html2text(display_post.get_text())[:1500]}```"
                                 f"{display_post.get_img()}")
        #await register_post_reactions(ctx, message, display_post)
        return message, display_post.board, display_post.get_links()
    except ChanError as e:
        return await ctx.send(e.message)


@commands.command()
@with_reactions()
async def info(ctx, arg=""):
    print(get_time() + "| Board " + arg + " info requested")
    try:
        return await ctx.send("```"+html2text(chan.get_info(arg))+"```")
    except ChanError as e:
        return await ctx.send(e.message)


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
