import os
import urllib.request
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default() #Discord bot permissions
intents.message_content = True

#Key symbol to identify command start and sets bot permissions
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    """
    Sets the Admin user to the provided ID
    """

    url = "https://chronicles-of-arcane.play.carde.io/cards"
    
    global web_html

    try:
        response = urllib.request.url(url)
        web_html = response.read().decode('UTF-8')
        print(web_html)
    except Exception as e:
        print(f"Exception Occurd: {e}")

    # with open("test.html", "w") as file:
    #     file.write(web_html)

@bot.command("getcard")
async def get_card(ctx, card_wanted):
    pass

bot.run(TOKEN)