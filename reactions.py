from functools import wraps
import disbot


class Emoji:
    wastebasket = "\U0001F5D1"

    @staticmethod
    def get_number(number):
        return chr(0x30+number)+"\U000020E3"


def get_trashcan_listener(message, ctx):
    async def on_reaction_add(reaction, user):
        if user.bot or reaction.message.id != message.id:
            return
        if reaction.emoji == Emoji.wastebasket:
            await message.delete()
            try:
                await ctx.message.delete()
            except TypeError as e:
                pass
            ctx.bot.remove_listener(on_reaction_add)
    return on_reaction_add


async def register_post_reactions(ctx, message, board, links):

    async def links_handler(reaction, user):
        if user.bot or reaction.message.id != message.id:
            return
        reac_no = int(reaction.emoji[0])
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
            ctx.bot.add_listener(get_trashcan_listener(message, ctx), "on_reaction_add")
            if post:
                await register_post_reactions(ctx, message, links.pop(0), *links)
        return decorated
    return decorator



