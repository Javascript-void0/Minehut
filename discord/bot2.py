import discord
import os
from asyncio import TimeoutError
from discord.ext import commands
from discord.utils import get
from math import floor

client = commands.Bot(command_prefix='.')
client.remove_command('help')
TOKEN = os.getenv("CHAT")
guild = None
online = False

@client.event
async def on_ready():
    global guild, online, channel, role
    guild = client.get_guild(872657348299227218)
    channel = guild.get_channel(872657350316687362)
    print('[ + ] Started {0.user}'.format(client))
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Anime"))

@client.command(aliases=['purge'], help='Clears certin number of messages')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'Cleared {amount} messages', delete_after=5)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

def timeFormat(integer):
    msg = str(integer).replace('```', '').replace('Time: ', '')
    h = floor(int(msg) // 60)
    m = int(msg) % 60
    if h < 10:
        h = "0" + str(h)
    if m < 10:
        m = "0" + str(m)
    return f'{h}:{m}'

@client.event
async def on_message(message):
    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if not message.author.name == 'Java' and not message.author.discriminator == 3865:
            await message.delete()
            print('deleted')
    if "Blessing" in message.content and message.channel.name == 'portal':
        channel = guild.get_channel(873434537802207273)
        msg = message.content
        name = msg.replace('```', '')
        await channel.edit(name=name)
    if ".link" in message.content and message.channel.name != "link":
        await message.delete()
        await message.channel.send('```This command can only be used in #link```', delete_after=3)
    # if "Time" in message.content and message.channel.name == 'portal':
    #     channel = guild.get_channel(873434491123826689)
    #     time = timeFormat(message.content)
    #     await channel.edit(name=f'Time: {time}')
    # await client.process_commands(message)

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)