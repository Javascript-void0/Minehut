import discord
import os
from asyncio import sleep
from discord.ext import tasks, commands
from discord.utils import get
from mcstatus import MinecraftServer

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")
guild = None
online = False

server = MinecraftServer.lookup("farminfarm.minehut.gg:25565")
try:
    mc_status = server.status()
except OSError:
    pass

@client.event
async def on_ready():
    global guild, online
    guild = client.get_guild(747233433511788637)
    print('[ + ] Started {0.user}'.format(client))
    member = guild.me
    await client.wait_until_ready()
    while True:
        if online:
            await member.edit(nick='[✔] FarminFarm')
            await client.change_presence(activity=discord.Game(name=f"{mc_status.player.online}/20 Online | farminfarm.minehut.gg"))
        else:
            await member.edit(nick='[❌] Farminfarm') 
            await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)
        await sleep(30)
            
@client.command(help='FarminFarm Server Status')
async def status(ctx):
    global guild, online
    messages = await guild.get_channel(751663136448315464).history().flatten()
    for msg in messages:
        if 'started' in msg.content:
            online = True
            break
        elif 'stopped' in msg.content:
            online = False
            break
    
    if online:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```        [ ONLINE ]```', color=discord.Color.green())
        embed.add_field(name=f'Players online: {mc_status.players.online}/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
    else:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```        [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
    await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(TOKEN)