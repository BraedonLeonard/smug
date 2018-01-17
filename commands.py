import random
import re
import os

from pyfiglet import Figlet
from discord.ext import commands

import util

class Commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        await self.bot.say('pong!')

    @commands.command()
    async def echo(self, *, message: str):
        ''' echoes a message '''
        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def ninja(self, context, *, message: str):
        ''' Like echo, but deletes the message that issued the command '''
        await self.bot.delete_message(context.message)
        await self.bot.say(message)

    @commands.command()
    async def swapIcon(self):
        '''
        Changes the profile picture randomly. Uses the images found in the
        directory specified in the config file.
        '''
        iconsDirectory = util.config['profile_picture_directory']
        iconsPath = os.path.join(util.basePath, iconsDirectory)
        items = (os.path.join(iconsPath, x) for x in os.listdir(iconsPath))
        files = tuple(x for x in items if os.path.isfile(x))
        with open(random.choice(files), 'rb') as iconFile:
            await self.bot.edit_profile(avatar=iconFile.read())
        await self.bot.say('Profile picture changed!')

    @commands.command()
    async def figlet(self, *, message: str):
        ''' echoes a message with figlet '''
        await self.bot.say(util.markdownCodeBlock(Figlet().renderText(message)))

    @commands.command()
    async def roll(self, dice: str='1d6'):
        ''' Rolls dice using NdN format '''
        if (re.fullmatch(util.NdN, dice) is None):
            await self.bot.say('Error: Format must be NdN')
            return
        numRolls, limit = map(int, dice.split('d'))
        results = (str(random.randint(1, limit + 1)) for x in range(numRolls))
        await self.bot.longSay(', '.join(results))

def setup(bot):
    bot.add_cog(Commands(bot))
