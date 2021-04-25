import discord
import os
from discord.ext import tasks, commands
from discord.utils import get
from mcstatus import MinecraftServer

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")
guild = None
online = False

server = MinecraftServer.lookup("farminfarm.minehut.gg:25565")
mc_status = server.status()

@client.event
async def on_ready():
    global guild, online
    guild = client.get_guild(747233433511788637)
    print('[ + ] Started {0.user}'.format(client))
            
@tasks.loop(seconds=5.0)
async def on_off():
    global guild, online
    member = guild.me
    messages = await guild.get_channel(751663136448315464).history().flatten()
    for msg in messages:
        if '✅' in msg.content and 'has started' in msg.content:
            print('online')
            online = True
            break
        elif '🛑' in msg.content and 'has stopped' in msg.ceont:
            print('offline')
            online = False
            break
    if online:
        await member.edit(nick='[🔹] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
    else:
        await member.edit(nick='[🔸] Farminfarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)

@on_off.before_loop
async def before_on_off():
    print('waiting...')
    await client.wait_until_ready()

@client.command(help='FarminFarm Server Status')
async def status(ctx):
    global guild, online
    messages = await guild.get_channel(751663136448315464).history().flatten()
    if online:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ ONLINE ]```', color=discord.Color.green())
        embed.add_field(name=f'Players online: {mc_status.players.online}/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
    else:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
    await ctx.send(embed=embed)

on_off.start()
if __name__ == '__main__':
    client.run(TOKEN)