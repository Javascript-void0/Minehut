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
    guild = client.get_guild(872657348299227218)
    channel = guild.get_channel(872657350316687362)
    role = get(guild.roles, id=872657348408258618)
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
    if before.id == 872657350316687362:
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

@client.command(help='ReShaft Server Status')
async def status(ctx):
    global guild, online, role
    server = MinecraftServer.lookup("reshaft.minehut.gg:25565")
    mc_status = server.status()
    if online:
        embed = discord.Embed(title='⚒     ReShaft Server Status', description=f'```       [ ONLINE ]```', color=discord.Color.green())
        embed.add_field(name=f'Players online: {mc_status.players.online}/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='reshaft.minehut.gg')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/10 Online | reshaft.minehut.gg"))
        await role.edit(color=discord.Color(0x91caad))
    else:
        embed = discord.Embed(title='⚒     ReShaft Server Status', description=f'```       [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/10', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='reshaft.minehut.gg')
        await client.change_presence(activity=discord.Game(name="Server Offline | reshaft.minehut.gg"), status=discord.Status.dnd)
        await role.edit(color=discord.Color(0xf7a982))
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if not message.author.id == '594352318464524289':
            await message.delete()
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)