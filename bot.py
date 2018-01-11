#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import itertools as it
import logging
import random
import regex
import textwrap

import discord
from discord.ext import commands

from util import * # Be mindful of namespace collisions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler(
    filename=f'{__name__}.log',
    encoding='utf-8',
    mode='w'
))

description = 'Multipurpose Discord chat/voice bot'
bot = commands.Bot(commands_prefix='!', description=description)

@bot.event
async def on_ready():
    print(textwrap.dedent(
        f'''
        Logged in as:
        {bot.user.name}
        {bot.user.id}
        -------------
        '''
    ))

@bot.command()
@static_vars('NdN'=regex.compile(r'\d+d\d+'))
async def roll(dice: str):
    '''Rolls dice using NdN format'''
    if (regex.fullmatch(NdN, dice) is None):
        await bot.say('Error: Format must be NdN')
        return
    numRolls, limit = map(int, dice.split('d'))
    results = ', '.join(str(random.randint(1, limit)) for x in range(numRolls))
    await bot.say(results)
    
@bot.command()
async def ping():
    await bot.say("Pong!")

@bot.command()
async def echo(*, message: str):
    await bot.say(message)

bot.run("NDAxMDU5MDUyMTMxNDUwODkw.DTk2cQ.Xw0N-jhlfp406gGQrcRi2lgNEpg")
