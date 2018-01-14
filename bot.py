#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import logging
import textwrap

from discord.ext import commands
import yaml

import util

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

async def longSay(self, fullMessage, useCodeBlocks=False):
    '''
    Allows the bot to send messages longer than the 2000 character limit imposed
    by Discord by sending the message as a series of (up to) 2000 character
    messages.
    Sends up to messageLimit messages.
    '''
    messageLimit = 10 # 2000 characters is too little, but 20000 is a lot
    # Creating a code block takes 7 characters
    characterLimit = 2000 - 7 if useCodeBlocks else 2000
    breakIndexes = range(0, len(fullMessage), characterLimit)
    messages = [fullMessage[i:i+characterLimit] for i in breakIndexes]
    if useCodeBlocks:
        messages = [util.markdownCodeBlock(message) for message in messages]
    for message in messages[:messageLimit]:
        await self.say(message)
    if len(messages) > messageLimit:
        await self.say(''.join((
            f'Exceeded message limit ({messageLimit}). ',
            f'{len(messages) - messageLimit} messages not sent.')))
commands.Bot.longSay = longSay

# load, unload, and reload are provided to aid in the development of the bot
# A developer can write their changes, then reload the module they changed
# without needing to restart the bot entirely by issuing `!reload <module>`

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
    # convenience function
    await unload(extension_name)
    await load(extension_name)

# Adds load, unload, and reload as commands to the bot
# The decorator is not applied when these functions are declared because
# reload makes use of both load and unload, which it would not be able to do if
# they were warpped by the decorator
for command in (load, unload, reload):
    bot.command(hidden=True)(command)

if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    with open('config.yaml', 'r') as configFile:
        config = yaml.load(configFile)

    bot.run(config['token'])
