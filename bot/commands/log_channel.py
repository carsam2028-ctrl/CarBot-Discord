import discord
import sqlite3
import datetime
from typing import Optional
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

#Functions
def signature_print():
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + " [CarBot] "

class LogChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS logging
                         (id text PRIMARY KEY, log_channel text, webhook text)''')

    @app_commands.command(name="log_channel", description="Sets log channel.")
    @app_commands.describe(channel="Where to set the logging channel, if none set it will use current channel as the log channel.")
    async def log_channel(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
        await interaction.response.defer()
        if channel is None:
            channel = interaction.channel
        webhook = await channel.create_webhook(name="CarBot Logging", avatar=None, reason="Logging Webhook")
        self.c.execute('''SELECT 1 FROM logging WHERE id=?''', (interaction.guild_id,))
        exist = self.c.fetchone()
        if exist:
            self.c.execute('''UPDATE logging SET log_channel=?, webhook=? WHERE id=?''',(str(channel.id), webhook.url, interaction.guild_id))
        else:
            self.c.execute('''INSERT INTO logging (log_channel, webhook, id) VALUES (?,?,?)''',(str(channel.id), webhook.url, interaction.guild_id))
        self.conn.commit()
        await interaction.followup.send(f"Logging channel set to **{channel}**!")
        print(signature_print() + f"Webhook made for logging: {webhook.url}")
async def setup(bot):
    await bot.add_cog(LogChannel(bot))