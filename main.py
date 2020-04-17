from disbot import *
from discord.ext import commands
from reactions import get_trashcan_listener

token = 'Your Token'


def main():
    bot = commands.Bot(command_prefix='G.')
    @bot.event
    async def on_ready():
        print('Bot is ready...')
    bot.add_listener(get_trashcan_listener(bot),"on_raw_reaction_add")
    bot.add_command(echo)
    bot.add_command(hp)
    bot.add_command(post)
    bot.add_command(info)
    bot.run(token)


if __name__ == '__main__':
    main()
