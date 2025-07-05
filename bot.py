import discord  # type: ignore
import requests  # type: ignore
import json
import random
import asyncio

def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = json.loads(response.text)
    return json_data['url']

hey_responses = [
    "Hey", "Yo", "Sup", "What's up", "How's it going", "You good?",
    "Wassup", "Hey there", "What's new", "How you been", "All good?",
    "Long time no see", "Glad you’re here", "Look who showed up", "You made it",
    "There you are", "What's happening", "Everything chill?", "What's the move",
    "Nice to see you", "What's good", "How's life", "Just in time", "What’s the vibe",
    "Ayy you", "You around?", "Back again?", "Hey hey", "What’s up with you", "Here we go"
]

class MyClient(discord.Client):
    def __init__(self, *, intents):
        super().__init__(intents=intents)
        self.last_hey_response = None
        self.hello_tasks = {}  # Track per-channel hello wait tasks

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        msg = message.content.lower()
        channel_id = message.channel.id

        # Cancel any pending hello task if someone speaks
        if channel_id in self.hello_tasks:
            self.hello_tasks[channel_id].cancel()
            del self.hello_tasks[channel_id]

        if msg.startswith('hello'):

            # Start 60s wait to respond with "JARA.COM"
            async def wait_for_reply():
                try:
                    await asyncio.sleep(60)
                    await message.channel.send("JARA.COM")
                except asyncio.CancelledError:
                    pass  # Task was cancelled because someone responded

            task = asyncio.create_task(wait_for_reply())
            self.hello_tasks[channel_id] = task

        elif msg.startswith('hey'):
            response = random.choice(hey_responses)
            while response == self.last_hey_response and len(hey_responses) > 1:
                response = random.choice(hey_responses)
            self.last_hey_response = response
            await message.channel.send(response)

        elif msg.startswith('$meme'):
            await message.channel.send(get_meme())

        elif 'wednesday' in msg:
            await message.channel.send("https://www.thewrangleronline.com/wp-content/uploads/2017/09/wednesday-frog-900x600.jpg")

        elif 'sus' in msg:
            await message.channel.send("https://media.tenor.com/ZXvjz2NYgZkAAAAC/among-us.gif")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('N/A')  # Replace with your actual bot token
