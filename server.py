import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import time

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default() #Discord bot permissions
intents.message_content = True

#Key symbol to identify command start and sets bot permissions
bot = commands.Bot(command_prefix='!', intents = intents)

images = []

@bot.event
async def on_ready():
    """
    Sets the Admin user to the provided ID
    """

    url = "https://chronicles-of-arcane.play.carde.io/cards"
    
    global web_html

    try:
        driver.get(url)
    except Exception as e:
        print(f"Exception Occurd: {e}")

    old_height = driver.execute_script('return document.body.scrollHeight')
    new_height = None
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')

        if new_height == old_height:
            break
        old_height = new_height

    web_html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(web_html, "html.parser")
    for image_source in soup.find_all("img"):
        images.append(image_source["src"])

@bot.command("getcard")
async def get_card(ctx, card_wanted):
    card_wanted = card_wanted.replace(' ', '-')
    img_url = [string for string in images if card_wanted in string]
    print(img_url)

bot.run(TOKEN)