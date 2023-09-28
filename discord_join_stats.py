# Makes a .csv text file of how many people join a discord server per day.

import os
import sys
import discord     # requires pip install discord.py
import time

intents = discord.Intents.default()
intents.messages = True
discord_bot = discord.Client(intents=intents)

os.system('cls' if os.name == 'nt' else 'clear')

bot_token = "[bot token]"
owner_id = [bot owner id number]
server_id = [server id number]
channel_with_joins_id = [id of the channel where join messages appear] 

@discord_bot.event
async def on_ready():
    print(f'{discord_bot.user} on ilmestynyt serverille! ^_^\n')

    user = await discord_bot.fetch_user(owner_id)
    await discord_bot.wait_until_ready()
    print("Joinimisviestien nuuskinta in progress.\n")
    
    channel = await discord_bot.fetch_channel(channel_with_joins_id)
    current_channel_name = str(channel)
    join_data = {}  # dictionary with join date as key and usernames as values

    start_time = time.time()
    progress_indicator = 0 

    async for message in channel.history(limit=None):
        if message.type == discord.MessageType.new_member:
            date = message.created_at.strftime("%Y-%m-%d")
            
            if date not in join_data:
                join_data[date] = []
            
            join_data[date].append(message.author.display_name)
            
            # progress indicator
            print('.', end='', flush=True)
            progress_indicator += 1          
            if progress_indicator % 50 == 0:
                print()

    with open("join_log.txt", 'w') as f:
        for date, users in join_data.items():
            f.write(f"{date},{len(users)},{','.join(users)}\n")

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time / 60)
    seconds = int(elapsed_time % 60)
    time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print("\n#" + current_channel_name + ": " + str(sum([len(users) for users in join_data.values()])) + " messages, retrieval time " + str(minutes) + "min " + str(seconds) + "s.")
    
    print("\n\nKaiveltu'd ^ _^ _b\n\n")
    await discord_bot.close()


# bot startup command
try:
    discord_bot.run(bot_token)
except:
    print("Error connecting to discord (probably no network)")
    sys.exit(1)
