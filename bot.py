import discord
import os
from discord.ext import commands
from discord.utils import get
from mcstatus import MinecraftServer

intents = discord.Intents.default()
intents.guilds = True
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("TOKEN")
guild = None
online = False

@client.event
async def on_ready():
    global guild, online
    guild = client.get_guild(747233433511788637)
    channel = guild.get_channel(751663136448315464)
    print('[ + ] Started {0.user}'.format(client))
    await client.wait_until_ready()
    server = MinecraftServer.lookup("farminfarm.minehut.gg:25565")
    mc_status = server.status()
    if 'online' in channel.topic:
        print('online')
        online = True
    elif 'offline' in channel.topic:
        print('offline')
        online = False

@client.event
async def on_guild_channel_update(before, after):
    global guild, online
    member = guild.me
    server = MinecraftServer.lookup("farminfarm.minehut.gg:25565")
    mc_status = server.status()
    if before.id == 751663136448315464:
        if 'online' in after.topic:
            print('online')
            online = True
        elif 'offline' in after.topic:
            print('offline')
            online = False
    if online:
        await member.edit(nick='[🔹] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
    else:
        await member.edit(nick='[🔸] Farminfarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)

@client.command(help='FarminFarm Server Status')
async def status(ctx):
    global guild, online
    member = guild.me
    server = MinecraftServer.lookup("farminfarm.minehut.gg:25565")
    mc_status = server.status()
    messages = await guild.get_channel(751663136448315464).history().flatten()
    if online:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ ONLINE ]```', color=discord.Color.green())
        embed.add_field(name=f'Players online: {mc_status.players.online}/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
        await member.edit(nick='[🔹] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
    else:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
        await member.edit(nick='[🔸] Farminfarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)
    await ctx.send(embed=embed)
        
if __name__ == '__main__':
    client.run(TOKEN)