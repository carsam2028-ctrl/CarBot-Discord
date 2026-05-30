import discord
import sqlite3
import datetime
import aiohttp
import os
from typing import Optional
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

#Functions
def signature_print():
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + " [CarBot] "
#Varibles
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

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
        avatar_webhook = await self.bot.user.avatar.read()
        if channel is None:
            channel = interaction.channel
        webhook = await channel.create_webhook(name="CarBot Logging", avatar=avatar_webhook,reason="Logging Webhook")
        self.c.execute('''SELECT webhook FROM logging WHERE id=?''', (interaction.guild_id,))
        exist = self.c.fetchone()

        if exist and exist[0]:
            webhook_old = exist[0]
            async with aiohttp.ClientSession() as session:
                webhook_old = discord.Webhook.from_url(webhook_old, client=self.bot, session=session, bot_token=DISCORD_TOKEN)
                await webhook_old.delete(reason="Duplicate/Old Webhook", prefer_auth=True)
            self.c.execute('''UPDATE logging SET log_channel=?, webhook=? WHERE id=?''',(str(channel.id), webhook.url, interaction.guild_id))
        else:
            self.c.execute('''INSERT INTO logging (log_channel, webhook, id) VALUES (?,?,?)''',(str(channel.id), webhook.url, interaction.guild_id))
        self.conn.commit()
        await interaction.followup.send(f"Logging channel set to **{channel}**!")
        print(signature_print() + f"Webhook made for logging: {webhook.url}")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        self.c.execute('''SELECT webhook FROM logging WHERE id=?''', (str(payload.guild_id),))
        vote = self.c.fetchone()

        if not vote:
            return

        webhook_url = vote[0]
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, client=self.bot, session=session)
            logs = f"Message deleted in <#{payload.channel_id}>"
            if payload.cached_message:
                logs += f"\nAuthor: {payload.cached_message.author}\nContent: {payload.cached_message.content}"
            else:
                logs += f"\nThat message must have not been cached, this feature is a WIP."
            await webhook.send(content=logs, username="CarBot Logging")


async def setup(bot):
    await bot.add_cog(LogChannel(bot))