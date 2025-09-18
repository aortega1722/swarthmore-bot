import os
import discord
import asyncio
import requests
from bs4 import BeautifulSoup

# Get your bot token from environment variable
TOKEN = os.environ["TOKEN"]

# Channel ID where the bot will post
CHANNEL_ID = 688994932815429697  

# Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Categories to monitor
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

        await asyncio.sleep(300)  # check every 5 minutes

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(check_classifieds())

# Start the bot
client.run(TOKEN)
