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

async def load(extension_name: str):
    ''' loads an extension '''
    try:
        bot.load_extension(extension_name)
    except Exception as error:
        await bot.say(f'{type(error).__name__}\n{error}')
        return
    await bot.say(f'{extension_name} loaded')

async def unload(extension_name: str):
    ''' unloads an extension '''
    try:
        bot.unload_extension(extension_name)
    except Exception as error:
        await bot.say(f'{type(error).__name__}\n{error}')
        return
    await bot.say(f'{extension_name} unloaded')

async def reload(extension_name: str):
    ''' reloads an extension '''
    await unload(extension_name)
    await load(extension_name)

for command in (load, unload, reload):
    bot.command(hidden=True)(command)

if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    with open('config.yaml', 'r') as configFile:
        config = yaml.load(configFile)

    bot.run(config['token'])
