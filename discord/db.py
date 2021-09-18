import discord
import os, os.path
from asyncio import sleep
from discord.errors import DiscordServerError, NotFound
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("CHAT")

db = None
test = None
guild = None
log = None
file_log = None
portal = None

@client.event
async def on_ready():
    global db, guild, log, file_log, portal
    guild = client.get_guild(872657348299227218)
    test = client.get_guild(805299220935999509)
    db = guild.get_channel(872657351461732395)
    log = test.get_channel(872829816624271381)
    file_log = test.get_channel(872829900485193758)
    portal = guild.get_channel(886738161491914772)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')
    await log.send('```DATABASE: Started {0.user}```'.format(client))
    await log.send(f'```DATABASE: Connected to database...```')

async def get_data(discord):
    data = None
    f = open(f'./discord/data.txt', 'r').read()
    lines = f.splitlines()
    for i in range(len(lines)):
        if str(discord) in lines[i]:
            data = lines[i].split(': ')
            return data
    if not data:
        return False

@client.command(aliases=['data', 'search', 'stat', 'stats'], help='Find Data')
async def find(ctx, discord):
    global db
    discord, minecraft = await get_data(discord)
    if minecraft:
        await ctx.send(f'```Discord: {discord}\nMinecraft: {minecraft}```')
    else:
        await ctx.send(f'```DATABASE: No data for {discord}```')

@client.event
async def on_message(message):
    global log, portal, guild
    if message.channel == portal:
        if message.content.startswith('```Link: '):
            markdown = message.content.replace('```', '')
            discord, minecraft = markdown[6:].split(', ')
            await register(discord, minecraft)
            await log.send(f'Linked {discord} to {minecraft}')
            member = guild.get_member(int(discord))
            await member.edit(nick=f'[Linked] {minecraft}')
    await client.process_commands(message)

# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================

@client.command(help='Send Database File')
async def file(ctx):
    await ctx.send(file=discord.File(f'./discord/data.txt'))

@client.command(name='register', help='Registers a Player', aliases=['link'])
@commands.has_permissions(administrator=True)
async def _register(ctx, discord, minecraft):
    await register(discord, minecraft)
    await ctx.send(f'```DATABASE: Registered {discord} to {minecraft}```')

@client.command(name='unregister', help='Unregisters a Player', aliases=['unlink'])
@commands.has_permissions(administrator=True)
async def _unregister(ctx, discord):
    await unregister(discord)
    await ctx.send(f'```DATABASE: Unregistered {discord}```')

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

@client.command(help='Change your Discord nick (must be linked)')
async def nick(ctx, *, nick=None):
    if await registered(ctx.author.id):
        if not nick:
            await ctx.send('```.nick <nickname>```')
        elif len(nick) > 15:
            await ctx.send('```Nicknames must be less than 16 characters long```')
        else:
            await ctx.author.edit(nick=f'[Linked] {nick}')
            await ctx.send(f'```Nickname changed to {nick}```')
    else:
        await ctx.send('```You must link your account with minecraft to change your nickname```')

# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================
# ============================= DISCORD COMMANDS =============================

async def registered(discord):
    data = await get_data(discord)
    if data:
        return True
    return False

async def register(discord, minecraft):
    global log
    if not await registered(discord):
        f = open('./discord/data.txt')
        f = f.read()
        lines = f.splitlines(True)
        p = discord.rjust(16)
        lines.append(f'{p}: {minecraft}\n')
        with open(f'./discord/data.txt', 'w') as file:
            file.writelines(lines)
            file.close()
            await log.send(f'```DATABASE: Registered {discord}```')

async def unregister(discord):
    global log
    f = open(f'./discord/data.txt').read()
    lines = f.splitlines(True)
    with open(f'./discord/data.txt', 'w') as file:
        for i in range(len(lines)):
            if str(discord) not in lines[i]:
                file.write(lines[i])
    await log.send(f'```DATABASE: Unregistered {discord}```')


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