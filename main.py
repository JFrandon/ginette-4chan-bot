import discord, requests, random, json, time, webbrowser
from disbot import *
from discord.ext import commands

token = 'Your Token'


def main():
    bot = commands.Bot(command_prefix='G.')
    bot.add_listener(on_ready)
    bot.add_command(echo)
    bot.add_command(help)
    bot.add_command(post)
    bot.run(token)


if __name__ == '__main__':
    main()
