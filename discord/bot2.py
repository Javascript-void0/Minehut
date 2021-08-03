import discord
import os
from discord.ext import commands
from discord.utils import get
from mcstatus import MinecraftServer

client = commands.Bot(command_prefix='.')
client.remove_command('help')
TOKEN = os.getenv("CHAT")
guild = None
online = False
role = None

@client.event
async def on_ready():
    global guild, online, channel, role
    guild = client.get_guild(747233433511788637)
    channel = guild.get_channel(798198506878795797)
    role = get(guild.roles, id=862498099406438430)
    print('[ + ] Started {0.user}'.format(client))
    await client.wait_until_ready()
    server = MinecraftServer.lookup("reshaft.minehut.gg:25565")
    mc_status = server.status()
    if 'online' in channel.topic:
        print('online')
        online = True
    elif 'offline' in channel.topic:
        print('offline')
        online = False
    if online:
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/10 Online | reshaft.minehut.gg"))
        await role.edit(color=discord.Color(0x91caad))
    else:
        await client.change_presence(activity=discord.Game(name="Server Offline | reshaft.minehut.gg"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0xf7a982))

@client.event
async def on_guild_channel_update(before, after):
    global online, role
    server = MinecraftServer.lookup("reshaft.minehut.gg:25565")
    mc_status = server.status()
    if before.id == 798198506878795797:
        if 'online' in after.topic:
            print('online')
            online = True
        elif 'offline' in after.topic:
            print('offline')
            online = False
    if online:
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/10 Online | reshaft.minehut.gg"))
        await role.edit(color=discord.Color(0x91caad))
    else:
        await client.change_presence(activity=discord.Game(name="Server Offline | reshaft.minehut.gg"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0xf7a982))

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)