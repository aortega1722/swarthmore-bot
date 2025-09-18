import os
import discord
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = 688994932815429697  

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

CATEGORIES = {
    "Miscellaneous": "https://classifieds.swarthmore.edu/category/miscellaneous",
    "Off-Campus Jobs": "https://classifieds.swarthmore.edu/category/off-campus-jobs"
}

async def check_classifieds():
    seen_posts = set()
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        for category, url in CATEGORIES.items():
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")

            posts = soup.find_all("h3", class_="entry-title")  
            for post in posts:
                title = post.get_text(strip=True)
                link = post.find("a")["href"]

                if title not in seen_posts:
                    seen_posts.add(title)
                    await channel.send(f"📢 New {category} post:\n**{title}**\n🔗 {link}")

        await asyncio.sleep(300)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(check_classifieds())

# Wrap client.run in try/except to catch errors
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Bot crashed with error: {e}")
