#Imports
import os
import datetime
import discord
import dotenv
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
load_dotenv()


#Variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.message_content = True

#Functions
def signature_print():
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + " [CarBot] "

#Bot Startup
class CarBot(commands.Bot):
    async def setup_hook(self):
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                await self.load_extension(f'commands.{filename[:-3]}')
                print(signature_print() + f'Loaded extension: {filename}')

    async def on_ready(self):
        print(signature_print() + f'Logged on as {self.user}!')
        await self.tree.sync()
        print(signature_print() + 'Synced Commands Globally!')
        await self.tree.sync(guild=discord.Object(id=1504288510650093570))
        print(signature_print() + 'Synced Commands in Home Server!')
        await self.change_presence(activity=discord.Game(name="In Development"))
        print(signature_print() + f"{self.user.name} presence set!")

bot = CarBot(command_prefix='CB!', intents=intents)

#Error Handler
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    err_msg = ""
    print(signature_print() + f"Error: {str(error)}")
    if isinstance(error, app_commands.MissingPermissions):
        err_msg = "You do not have the necessary permission(s) for this command."
    elif isinstance(error, app_commands.BotMissingPermissions):
        err_msg = "Bot does not have required permission(s)."
    elif isinstance(error, discord.HTTPException):
        err_msg = "An HTTP Exception has occurred, try again."
    elif isinstance(error, discord.HTTPException) and error.status == 429:
        err_msg = "We are being rate limited, please try again after a couple seconds."
    elif isinstance(error, discord.Forbidden):
        err_msg = "Bot does not have required permission(s)."
    else:
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original
            err_msg = "An error has occurred, please try again."
        else:
            err_msg = f"A fatal error has occurred: {str(error)}"


    if interaction.response.is_done():
        await interaction.followup.send(f"{err_msg}", ephemeral=True)
    else:
        await interaction.response.send_message(f"{err_msg}", ephemeral=True)

#Commands moved to "commands" folder and are handled as cogs

#Runs Bot
bot.run(DISCORD_TOKEN)
