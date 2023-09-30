import os
import sys
import discord     # requires pip install discord.py
import time

# config
bot_token = "[bot token]"
server_id = [server id number]
channel_with_joins_id = [id of the channel where join messages appear] 


intents = discord.Intents.default()
intents.messages = True
intents.members = True                              # requires "privileged gateway intents" -> "server members intent" on the settings -> bot tab in the left side menu in the discord developer portal 
discord_bot = discord.Client(intents=intents)


os.system("cls" if os.name == "nt" else "clear")
print("Server join statistics")
print("----------------------")
print("\nConnecting to server...")


@discord_bot.event
async def on_ready():   
    join_data = {}  # dictionary with join date as key and usernames as values
    total_members = 0
    guild = discord_bot.guilds[0]

    print(f"{discord_bot.user} has slid into {guild}! ^_^\n")
    await discord_bot.wait_until_ready()
    channel = await discord_bot.fetch_channel(channel_with_joins_id)


    for member in guild.members:
        date = member.joined_at.strftime("%Y-%m-%d")
        if date not in join_data:
            join_data[date] = []
        if member.display_name not in join_data[date]:
            join_data[date].append(member.display_name)
            total_members += 1
    print(str(total_members) + " total users currently on the server.")


    current_channel_name = str(channel)
    print("\nSearching through " + current_channel_name + " for join messages.")
    print(". = existing user   * = user no longer on server")
    current_year = 0
    start_time = time.time()
    async for message in channel.history(limit=None):
        if message.type == discord.MessageType.new_member:
            date = message.created_at.strftime("%Y-%m-%d")
            year = message.created_at.strftime("%Y")

            if year != current_year:
                current_year = year
                print("\n" + year + ": ", end ="", flush=True)
            if date not in join_data:
                join_data[date] = []
            if message.author.display_name in join_data[date]:
                print(".", end="", flush=True)
            if message.author.display_name not in join_data[date]:
                join_data[date].append(message.author.display_name)
                print("*", end="", flush=True)          

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time / 60)
    seconds = int(elapsed_time % 60)
    print("\n\n#" + current_channel_name + ": " + str(sum([len(users) for users in join_data.values()])) + " join messages, retrieval time " + str(minutes) + "min " + str(seconds) + "s.")


    print("\n\nRemoving bots and bot-like people from the list: ", end="", flush=True)
    dates_to_remove = []    #remove dates from list if they contain no users after this
    for date, users in join_data.items():
        users_copy = users.copy()
        for username in users_copy:
            if 'bot' in username.lower():
                print(username + "  ", end ="", flush=True)
                users.remove(username)
        if not users:
            dates_to_remove.append(date)
    for date in dates_to_remove:
        del join_data[date]

    join_data = {date: join_data[date] for date in sorted(join_data)}

    total_joins = sum(len(users) for users in join_data.values())
    print("\n\nA total of " + str(total_joins) + " users have joined " + str(guild) + ".") 

    with open("join_log.txt", "w") as f:
        for date, users in join_data.items():
            f.write(f"{date},{len(users)},{','.join(users)}\n")
    print("\n\njoin_log.txt written  ^ _^ _b\n\n")


    await discord_bot.close()


# bot startup command
try:
    discord_bot.run(bot_token)
except:
    print("Error connecting to discord (probably no network or bot permissions)")
    sys.exit(1)
