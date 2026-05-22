import discord
import sqlite3
from discord.ext import commands
from discord import app_commands

class LogChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('bot.database.db')
async def setup(bot):
    await bot.add_cog(LogChannel(bot))