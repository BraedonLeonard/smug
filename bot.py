#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import logging
import textwrap
import yaml

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler(
    filename=f'{__name__}.log',
    encoding='utf-8',
    mode='w'
))

startup_extensions = ['commands']
description = 'Multipurpose Discord chat/voice bot'
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print(textwrap.dedent(
        f'''
        Logged in as:
        {bot.user.name}
        {bot.user.id}
        ------------------
        '''
    ))

if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    with open('config.yaml', 'r') as configFile:
        config = yaml.load(configFile)

    bot.run(config['token'])
