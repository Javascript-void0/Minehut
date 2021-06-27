import discord
import os
import datetime
from discord.ext import commands
from discord.utils import get
from mcstatus import MinecraftServer

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
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
async def on_member_join(member):
    global guild
    channel = guild.get_channel(800394119079002112)
    count = 0
    for member in guild.members:
        if not member.bot:
            count += 1
    await channel.edit(name=f'Members: {count} | S1²')

@client.event
async def on_member_remove(member):
    global guild
    channel = guild.get_channel(800394119079002112)
    count = 0
    for member in guild.members:
        if not member.bot:
            count += 1
    await channel.edit(name=f'Members: {count} | S1²')

@client.command(help='Update Member Count', aliases=['mu'])
async def memberupdate(ctx):
    global guild
    channel = guild.get_channel(800394119079002112)
    count = 0
    for member in guild.members:
        if not member.bot:
            count += 1
    await channel.edit(name=f'Members: {count} | S1²')
    await ctx.send(f'```Member Count Updated to {count}```')

@client.event
async def on_guild_channel_update(before, after):
    global guild, online
    member = guild.me
    role = get(guild.roles, id=837700794639187979)
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
        await member.edit(nick='[🤢] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
        await role.edit(color=discord.Color(0x3EA878))
    else:
        await member.edit(nick='[😡] FarminFarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0xE64043))

@client.command(help='FarminFarm Server Status')
async def status(ctx):
    global guild, online
    member = guild.me
    role = get(guild.roles, id=837700794639187979)
    server = MinecraftServer.lookup("farminfarm.minehut.gg:25565")
    mc_status = server.status()
    messages = await guild.get_channel(751663136448315464).history().flatten()
    if online:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ ONLINE ]```', color=discord.Color.green())
        embed.add_field(name=f'Players online: {mc_status.players.online}/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
        await member.edit(nick='[🤢] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
        await role.edit(color=discord.Color(0x3EA878))
    else:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
        await member.edit(nick='[😡] FarminFarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0xE64043))
    await ctx.send(embed=embed)

@client.command(aliases=['cl'], help='Input for Changlogs')
@commands.has_permissions(administrator=True)
async def changelog(ctx, *, change):
    role = ctx.guild.get_role(800936966988103680)
    channel = ctx.guild.get_channel(747234399422119988)
    d = datetime.date.today().strftime("%b %d")
    embed = discord.Embed(title = "Change Log", color=discord.Color(0xECA37E))
    embed.add_field(name = "Date:", value = f'{d}')
    embed.add_field(name = "<:down1:837675982998732851> Changes:", value = f"{change}")
    await channel.send(role.mention, embed=embed)
    await ctx.send('Created New Changelog')

@client.command(aliases=['rank'], help='Ranks Info')
async def ranks(ctx, rank = None):
    if not rank:
        embed = discord.Embed(title="🍞     FarminFarm Ranks", description='```         [ IN-GAME RANKS ]```\n- [`250K`]: Garden: `2nd Plot`\n- [` 5M`]: Vineyard: `/fly`, `/ec`, `/afk`, `/hat`, `/nick`\n- [`15M`]: Ranch: `3rd Plot`\n- [`30M`]: Plantation: `4th Plot`', color=discord.Color(0xECA37E))
        embed.set_footer(text='Rebirth to continue after Plantation')
    else:
        if rank == 'garden':
            embed = discord.Embed(title='🌻     Garden - 2nd Plot', description='```       [ $250K ]       ```\n**Previous**: `N/A`\n**Next**: `Garden`', color=discord.Color(0xECA37E))
        elif rank == 'vineyard':
            embed = discord.Embed(title='🌱     Vineyard - /fly, /ec, /afk, /hat`, `/nick', description='```           [ $5M ]       ```\n**Previous**: `Garden`\n**Next**: `Ranch`', color=discord.Color(0xECA37E))
        elif rank == 'ranch':
            embed = discord.Embed(title='🐄     Ranch - 3rd Plot', description='```       [ $15M ]       ```\n**Previous**: `Vineyard`\n**Next**: `Plantation`', color=discord.Color(0xECA37E))
        elif rank == 'plantation':
            embed = discord.Embed(title='🚜     Plantation - 4th Plot', description='```       [ $30M ]       ```\n**Previous**: `Ranch`\n**Next**: `Rebirth`', color=discord.Color(0xECA37E))
        else:
            embed = discord.Embed(title="🍞     FarminFarm Ranks", description='```         [ IN-GAME RANKS ]```\n- [`250K`]: Garden: `2nd Plot`\n- [` 5M`]: Vineyard: `/fly`, `/ec`, `/afk`, `/hat`, `/nick`\n- [`15M`]: Ranch: `3rd Plot`\n- [`30M`]: Plantation: `4th Plot`', color=discord.Color(0xECA37E))
            embed.set_footer(text='Rebirth to continue after Platation')
    await ctx.send(embed=embed)

@client.command(help='Rebirth Info')
async def rebirth(ctx):
    embed = discord.Embed(title="-                                           🥊     Rebirth", description='```                    [ REBIRTH ]```\nRebirth is avaiable at `Plantation` rank. Initialially it costs 50M, but the price increases `x1.2` each time. Rebirth multiplies the value of your crops. \n\nEx: \n**Rebirth `1`** would sell `1` wheat for `$12`. (default)\n**Rebirth `5`** would sell `1` wheat for `$60`. (each)', color=discord.Color(0xECA37E))
    await ctx.send(embed=embed)

@client.command(aliases=['sell'], help='Crop Sell Prices')
async def worth(ctx, *, crop = None):
    if not crop:
        embed = discord.Embed(title='💸     Crop Prices', description='```         [ WORTH ]           ```\nDefault Prices - _Before_ factoring in rebirth. \n\n`        Wheat`: $12\n`       Potato`: $12\n`       Carrot`: $12\n`  Wheat Seeds`: $1\n`      Pumpkin`: $10\n`  Melon Slice`: $5\n`       Cactus`: $10\n`   Sugar Cane`: $12\n`       Bamboo`: $1\n`         Kelp`: $6\n` Chorus Fruit`: $20\n`         Vine`: $20\n`  Nether Wart`: $20', color=discord.Color(0xECA37E))
        await ctx.send(embed=embed)
    else:
        if crop == 'wheat':
            cost = 12
        elif crop == 'potato':
            cost = 12
        elif crop == 'carrot':
            cost = 12
        elif crop == 'wheatseeds' or crop == 'wheat_seeds' or crop == 'seeds' or crop == 'wheat seeds':
            cost = 1
        elif crop == 'pumpkin':
            cost = 10
        elif crop == 'melon' or crop == 'melonslice':
            cost = 5
        elif crop == 'cactus':
            cost = 10
        elif crop == 'sugarcane':
            cost = 12
        elif crop == 'bamboo':
            cost = 1
        elif crop == 'kelp':
            cost = 6
        elif crop == 'chorus' or crop == 'chorusfruit' or crop == 'chorus fruit':
            cost = 20
        elif crop == 'vine':
            cost = 20
        elif crop == 'wart' or crop == 'nether wart' or crop == 'netherwart':
            cost = 20
        try:
            await ctx.send(f'```{crop}: ${cost}```')
        except UnboundLocalError:
            await ctx.send(f'```"{crop}" not found. ```')

@client.event
async def on_message(message):
    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if not message.author.id == '594352318464524289':
            await message.delete()

@client.command(aliases=['purge'], help='Clears certin number of messages')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'Cleared {amount} messages', delete_after=5)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)