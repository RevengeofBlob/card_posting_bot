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
    images = []
    images = soup.find_all("img")
    img_url = images[20]["src"]
    print(images[20]["src"])

    img_data = requests.get(img_url).content
    with open("image.jpg", "wb") as f:
        f.write(img_data)

@bot.command("getcard")
async def get_card(ctx, card_wanted):
    pass

bot.run(TOKEN)