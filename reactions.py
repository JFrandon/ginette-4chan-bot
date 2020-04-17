from functools import wraps
from discord.ext.commands.context import Context
from discord.ext.commands.converter import MessageConverter
from discord.message import Message
import disbot

class FakeMessage(Message):
    def __init__(self):
        self._state = None


class Emoji:
    wastebasket = "\U0001F5D1"

    @staticmethod
    def get_number(number):
        return chr(0x30+number)+"\U000020E3"



def get_trashcan_listener(bot):
    ctx = Context(bot=bot, prefix="", message=FakeMessage())
    async def trashcan_listener(payload):
        message_id = payload.message_id
        channel_id = payload.channel_id
        message = await MessageConverter().convert(ctx,f"{channel_id}-{message_id}")
        if payload.member.bot or message.author.id != ctx.bot.user.id:
            return
        if payload.emoji.name == Emoji.wastebasket:
            await message.delete()
    return trashcan_listener


async def register_post_reactions(ctx, message, board, links):

    async def links_handler(reaction, user):
        if user.bot or reaction.message.id != message.id:
            return
        reac_no = int(reaction.emoji[0]) if '0' <= reaction.emoji[0] <= '9' else -1
        if len(links) > reac_no > -1:
            await disbot.post(ctx, board, links[0], links[reac_no])

    async def on_message_delete(msg):
        if message.id == msg.id:
            ctx.bot.remove_listener(on_message_delete)
            ctx.bot.remove_listener(links_handler)
    for i in range(min(len(links), 10)):
        await message.add_reaction(Emoji.get_number(i))
    ctx.bot.add_listener(links_handler, "on_reaction_add")
    ctx.bot.add_listener(on_message_delete, "on_message_delete")


def with_reactions(post=False):
    def decorator(func):
        @wraps(func)
        async def decorated(ctx, *args, **kwargs):
            message, *links = await func(ctx, *args, **kwargs)
            await message.add_reaction(Emoji.wastebasket)
            if post:
                await register_post_reactions(ctx, message, links.pop(0), *links)
        return decorated
    return decorator



