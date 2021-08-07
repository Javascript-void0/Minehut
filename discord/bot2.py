import discord
import os
from asyncio import TimeoutError
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
    role = get(guild.roles, id=872657348441808936)
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
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/10 Online"))
        await role.edit(color=discord.Color(0x48b66c))
    else:
        await client.change_presence(activity=discord.Game(name="Server Offline"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0x698f75))

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
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/10 Online"))
        await role.edit(color=discord.Color(0x48b66c))
    else:
        await client.change_presence(activity=discord.Game(name="Server Offline"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0x698f75))

@client.command(help='ReShaft Server Status')
async def status(ctx):
    global guild, online, role
    server = MinecraftServer.lookup("reshaft.minehut.gg:25565")
    mc_status = server.status()
    if online:
        embed = discord.Embed(title='⚒     ReShaft Server Status', description=f'```       [ ONLINE ]```', color=discord.Color.green())
        embed.add_field(name=f'Players online: {mc_status.players.online}/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='reshaft.minehut.gg')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/10 Online"))
        await role.edit(color=discord.Color(0x48b66c))
    else:
        embed = discord.Embed(title='⚒     ReShaft Server Status', description=f'```       [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/10', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='reshaft.minehut.gg')
        await client.change_presence(activity=discord.Game(name="Server Offline"), status=discord.Status.dnd)
        await role.edit(color=discord.Color(0x698f75))
    await ctx.send(embed=embed)

async def updateDrop(message):
    embed = message.embeds[0]
    count = 0
    for reaction in message.reactions:
        count += reaction.count
        print(count)
    embed.set_footer(text=f'Limit: {count}/10')
    await message.edit(embed=embed)

async def dropGem(ctx, num):
    channel = guild.get_channel(872661226059096125)
    embed = discord.Embed(title=f'💎 New Drop - {num} Gems', description='React below to claim. You need linked account', color=discord.Color(0x36A9E5))
    embed.set_footer(text='Limit: 0/10')
    message = await channel.send(embed=embed)
    await message.add_reaction('💎')
    def check(reaction):
        return reaction.message.id == message.id
    while True:
        try:
            reaction = await client.wait_for('reaction_add', timeout=1200, check=check)
            if reaction.emoji == '💎':
                await updateDrop(message)
            else:
                await message.remove_reaction(reaction)
        except TimeoutError:
            await message.edit(content='```[x] Expired```', embed=embed)
            break

@client.command(help='Create Drop')
async def drop(ctx, num):
    await dropGem(ctx, num)
    await ctx.send('```Drop Created```')

@client.command(aliases=['purge'], help='Clears certin number of messages')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'Cleared {amount} messages', delete_after=5)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

@client.event
async def on_message(message):
    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if not message.author.id == '594352318464524289':
            await message.delete()
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)