import discord
import os, os.path
from asyncio import sleep
from discord.errors import DiscordServerError, NotFound
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("CHAT")

db = None
guild = None
log = None
file_log = None

@client.event
async def on_ready():
    global db, guild, log, file_log
    guild = client.get_guild(747233433511788637)
    db = guild.get_channel(871179843264466995)
    log = guild.get_channel(871179925250506752)
    file_log = guild.get_channel(871180111582470154)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')
    await log.send('```DATABASE: Started {0.user}```'.format(client))
    await log.send(f'```DATABASE: Connected to database...```')

@client.command(help='Link Your Minecraft Account to Discord Database')
async def link(ctx, player):
    await ctx.send(f'```[!] {player}```')

async def link(player):
    pass

async def get_data(player):
    data = None
    f = open(f'./discord/data.txt', 'r').read()
    lines = f.splitlines()
    for i in range(len(lines)):
        if str(player) in lines[i]:
            data = lines[i].split(': ')
            split = data[1].split(', ')
            return split
    if not data:
        return False

@client.command(aliases=['data', 'search', 'stat', 'stats'], help='Find Data')
async def find(ctx, player):
    global db
    data = await get_data(player)
    if data:
        if len(data) == 8:
            await ctx.send(f'```[:L{data[0]}] {player} - {data[1]}{data[2]}{data[3]}{data[4]}{data[5]}{data[6]}\nLinked: {data[7]}```')
        else:
            await ctx.send(f'```[:L{data[0]}] {player} - {data[1]}{data[2]}{data[3]}{data[4]}{data[5]}{data[6]}```')
    else:
        await ctx.send(f'```DATABASE: No data for {player}```')

@client.command(aliases=['self'], help='Shows Your Stats')
async def me(ctx):
    global db
    player = ctx.message.author
    data = await get_data(player)
    if data:
        await ctx.send(f'```[:L{data[0]}] {player} - {data[1]}{data[2]}{data[3]}{data[4]}{data[5]}{data[6]}\nLinked: {data[7]}```')
    else:
        await ctx.send(f'```DATABASE: No data for {player}```')

async def modify_data(player, currency, action, num):
    global log
    data = None
    f = open(f'./discord/data.txt').read()
    lines = f.splitlines(True)
    if currency is 'level':
        index = 0
    if currency is 'gold':
        index = 1
    if currency is 'gem':
        index = 2
    if currency is 'medal':
        index = 3
    if currency is 'token':
        index = 4
    if currency is 'block':
        index = 5
    if currency is 'total':
        index = 6
    for i in range(len(lines)):
        if str(player) in lines[i]:
            data = get_data(player)
            if action == 'add':
                x = int(data[index]) + num
                await log.send(f'```DATABASE: Added {num} to {player}```')
            elif action == 'remove':
                x = int(data[index]) - num
                await log.send(f'```DATABASE: Removed {num} from {player}```')
            elif action == 'reset':
                x = 0
                await log.send(f'```DATABASE: Reset{player} to 0```')
            elif action == 'set':
                x = num
                await log.send(f'```DATABASE: Set {player} to {num}```')
            if x < 0:
                x = 0
            if currency is 'level':
                lines[i] = f'{player}: {x}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}\n'
            if currency is 'gold':
                lines[i] = f'{player}: {data[0]}, {x}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}\n'
            if currency is 'gem':
                lines[i] = f'{player}: {data[0]}, {data[1]}, {x}, {data[3]}, {data[4]}, {data[5]}, {data[6]}\n'
            if currency is 'medal':
                lines[i] = f'{player}: {data[0]}, {data[1]}, {data[2]}, {x}, {data[4]}, {data[5]}, {data[6]}\n'
            if currency is 'token':
                lines[i] = f'{player}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {x}, {data[5]}, {data[6]}\n'
            if currency is 'block':
                lines[i] = f'{player}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {x}, {data[6]}\n'
            if currency is 'total':
                lines[i] = f'{player}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {x}\n'
            with open(f'./discord/data.txt', 'w') as file:
                file.writelines(lines)

@client.command(help='test')
async def test(ctx):
    await ctx.send('```[!]```')

@client.event
async def on_message(message):
    global log
    if message.channel == log and message.author.id == 779111449343164418:
        if message.content.startswith('```[+]'): # ADD
            await log.send('done')
        elif message.content.startswith('```[-]'): # REMOVE
            await log.send('done')
        elif message.content.startswith('```[=]'): # SET
            await log.send('done')
        elif message.content.startswith('```[|]'): # RESET
            await log.send('done')
        elif message.content.startswith('```[R]'): # REGISTER FROM MC
            await log.send('done')
        elif message.content.startswith('```[L]'): # MC TO DISCORD LINK
            await log.send('done')
        elif message.content.startswith('```[N]'): # REGISTER FROM MC
            await log.send('done')
#            await register(player)
    await client.process_commands(message)

# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================

@client.command(help='Send Database File')
async def file(ctx):
    await ctx.send(file=discord.File(f'./discord/data.txt'))

@client.command(name='register', help='Registers a Player')
@commands.has_permissions(administrator=True)
async def _register(ctx, player):
    await register(player)
    await ctx.send(f'```DATABASE: Registered {player}```')

@client.command(name='unregister', help='Unregisters a Player')
@commands.has_permissions(administrator=True)
async def _unregister(ctx, player):
    await unregister(player)
    await ctx.send(f'```DATABASE: Unregistered {player}```')

@client.command(aliases=['dbload', 'loaddatabase', 'loaddb', 'load_database', 'load_db'], help='Database Load')
@commands.has_permissions(administrator=True)
async def databaseload(ctx):
    global db
    messages = await db.history().flatten()
    if messages == []:
        await db.send(file=discord.File(f'./discord/data.txt'))
        await log.send('```DATABASE: Loaded```', file=discord.File(f'./discord/data.txt'))
    await ctx.send('```DATABASE: Loaded```')

@client.command(aliases=['dbclear', 'cleardatabase', 'cleardb', 'clear_database', 'clear_db'], help='Clears the Database')
@commands.has_permissions(administrator=True)
async def databaseclear(ctx):
    global db
    await db.purge(limit=None)
    await ctx.send('```DATABASE: Cleared all files in #db```')

@client.command(help='Add')
@commands.has_permissions(administrator=True)
async def add(ctx, player, num : int):
    if num > 0:
        await modify_data(player, 'add', num)
        await ctx.send(f'```DATABASE: Added {num} to {player}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')

@client.command(help='Remove')
@commands.has_permissions(administrator=True)
async def remove(ctx, player, num : int):
    if num > 0:
        await modify_data(player, 'remove', num)
        await ctx.send(f'```DATABASE: Removed {num} from {player}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')
        
@client.command(help='Reset Player Data')
@commands.has_permissions(administrator=True)
async def reset(ctx, player):
    await modify_data(player, 'reset', 0)
    await ctx.send(f'```DATABASE: Reset {player} to 0```')

@client.command(help='Set Player Data')
@commands.has_permissions(administrator=True)
async def set(ctx, player, num : int):
    if num > 0:
        await modify_data(player, 'set', num)
        await ctx.send(f'```DATABASE: Set {player} to {num}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')

# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================

async def registered(player):
    data = await get_data(player)
    if data:
        return True
    return False

async def register(player):
    global log
    if not await registered(player):
        f = open('./discord/data.txt')
        f = f.read()
        lines = f.splitlines(True)
        lines.append(f'{player}: 0, 0, 0, 0, 0, 0, 0\n')
        with open(f'./discord/data.txt', 'w') as file:
            file.writelines(lines)
            file.close()
            await log.send(f'```DATABASE: Registered {player}```')

async def unregister(player):
    global log
    f = open(f'./discord/data.txt').read()
    lines = f.splitlines(True)
    with open(f'./discord/data.txt', 'w') as file:
        for i in range(len(lines)):
            if str(player) not in lines[i]:
                file.write(lines[i])
    await log.send(f'```DATABASE: Unregistered {player}```')


async def get_db_files():
    global db, log
    messages = await db.history(limit=None, oldest_first=True).flatten()
    if messages:
        file_num = 1
        for msg in messages:
            file = await msg.attachments[0].read()
            with open(f'./discord/data.txt', 'wb') as f:
                f.write(file)
                f.close()
            await log.send(f'```DATABASE: Saved {file_num}.txt to Directory```')
            file_num += 1

async def get_log_files():
    global file_log, log
    try:
        message = await file_log.fetch_message(file_log.last_message_id)
    except NotFound:
        await log.send('```DATABASE: Unknown Message```')
    file = await message.attachments[0].read()
    with open(f'./discord/data.txt', 'wb') as f:
        f.write(file)
        f.close()

async def log_update():
    global file_log, log
    await file_log.send(file=discord.File(f'./discord/data.txt'))

async def db_empty():
    if os.path.exists('./discord/data.txt'):
        return False
    return True

async def reload_database():
    global db, file_log
    await db.purge(limit=None)
    messages = await db.history().flatten()
    if messages == []:
        await db.send(file=discord.File(f'./discord/data.txt'))

# LOOP TO RELOAD FILE

@tasks.loop(minutes=1.0)
async def loop_restart():
    if await db_empty():
        await get_log_files()
    else:
        await log_update()
        await get_log_files()
    await reload_database()

@loop_restart.before_loop
async def before_loop_restart():
    print('waiting...')
    await client.wait_until_ready()

loop_restart.start()
if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)