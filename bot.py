import discord
import os
import datetime
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
        await member.edit(nick='[🔹] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
        await role.edit(color=discord.Color(0x82c1f7))
    else:
        await member.edit(nick='[🔸] FarminFarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0xf7a982))

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
        await member.edit(nick='[🔹] FarminFarm')
        await client.change_presence(activity=discord.Game(name=f"{mc_status.players.online}/20 Online | farminfarm.minehut.gg"))
        await role.edit(color=discord.Color(0x82c1f7))
    else:
        embed = discord.Embed(title='🍞     FarminFarm Server Status', description=f'```       [ OFFLINE ]```', color=discord.Color.red())
        embed.add_field(name=f'Players online: 0/20', value=f" - `Ping: {mc_status.latency} ms`")
        embed.set_footer(text='farminfarm.minehut.gg')
        await member.edit(nick='[🔸] FarminFarm') 
        await client.change_presence(activity=discord.Game(name="Server Offline | farminfarm.minehut.gg"), status=discord.Status.do_not_disturb)
        await role.edit(color=discord.Color(0xf7a982))
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
        embed = discord.Embed(title="🍞     FarminFarm Ranks", description='```       [ IN-GAME RANKS ]```\n- [`50K`]: Miner\n- [`250K`]: Warrior: `2nd Plot`\n- [` 1M`]: General\n- [` 5M`]: Engineer: `/fly`, `/ec`, `/afk`, `/hat`\n- [`10M`]: Spectre\n- [`15M`]: Monopoly: `3rd Plot`\n- [`20M`]: CEO\n- [`25M`]: Veteran\n- [`30M`]: God: `4th Plot`', color=discord.Color(0xECA37E))
        embed.set_footer(text='Rebirth to continue after God')
    else:
        if rank == 'miner':
            embed = discord.Embed(title='⛏     Miner', description='```       [ $50K ]       ```\n**Previous**: `N/A`\n**Next**: `Warrior`', color=discord.Color(0xECA37E))
        if rank == 'warrior':
            embed = discord.Embed(title='🪓     Warrior - 2nd Plot', description='```       [ $250K ]       ```\n**Previous**: `Miner`\n**Next**: `General`', color=discord.Color(0xECA37E))
        elif rank == 'general':
            embed = discord.Embed(title='💪     General', description='```       [ $1M ]       ```\n**Previous**: `Warrior`\n**Next**: `Engineer`', color=discord.Color(0xECA37E))
        elif rank == 'engineer':
            embed = discord.Embed(title='🧠     Engineer - /fly, /ec, /afk, /hat', description='```           [ $5M ]       ```\n**Previous**: `General`\n**Next**: `Spectre`', color=discord.Color(0xECA37E))
        elif rank == 'spectre':
            embed = discord.Embed(title='🛸     Spectre', description='```       [ $10M ]       ```\n**Previous**: `Engineer`\n**Next**: `Monopoly`', color=discord.Color(0xECA37E))
        elif rank == 'monopoly':
            embed = discord.Embed(title='💸     Monopoly - 3rd Plot', description='```       [ $15M ]       ```\n**Previous**: `Spectre`\n**Next**: `CEO`', color=discord.Color(0xECA37E))
        elif rank == 'ceo':
            embed = discord.Embed(title='💼     CEO', description='```       [ $20M ]       ```\n**Previous**: `Monopoly`\n**Next**: `Veteran`', color=discord.Color(0xECA37E))
        elif rank == 'veteran':
            embed = discord.Embed(title='🔑     Veteran', description='```       [ $25M ]       ```\n**Previous**: `CEO`\n**Next**: `God`', color=discord.Color(0xECA37E))
        elif rank == 'god':
            embed = discord.Embed(title='👑     God - 4th Plot', description='```       [ $30M ]       ```\n**Previous**: `Veteran`\n**Next**: `Rebirth`', color=discord.Color(0xECA37E))
        else:
            embed = discord.Embed(title="🍞     FarminFarm Ranks", description='```       [ IN-GAME RANKS ]```\n- [`50K`]: Miner\n- [`250K`]: Warrior: `2nd Plot`\n- [` 1M`]: General\n- [` 5M`]: Engineer: `/fly`, `/ec`, `/afk`, `/hat`\n- [`10M`]: Spectre\n- [`15M`]: Monopoly: `3rd Plot`\n- [`20M`]: CEO\n- [`25M`]: Veteran\n- [`30M`]: God: `4th Plot`', color=discord.Color(0xECA37E))
            embed.set_footer(text='Rebirth to continue after God')
    await ctx.send(embed=embed)

@client.command(help='Rebirth Info')
async def rebirth(ctx):
    embed = discord.Embed(title="-                                           🥊     Rebirth", description='```                    [ REBIRTH ]```\nRebirth is avaiable at `God` rank. Initialially it costs 10M, but the price increases `x1.2` each time. Rebirth multiplies the value of your crops. \n\nEx: \n**Rebirth `1`** would sell `1` wheat for `$24`. (default)\n**Rebirth `5`** would sell `1` wheat for `$120`. (each)', color=discord.Color(0xECA37E))
    await ctx.send(embed=embed)

@client.command(aliases=['sell'], help='Crop Sell Prices')
async def worth(ctx, *, crop = None):
    if not crop:
        embed = discord.Embed(title='💸     Crop Prices', description='```         [ WORTH ]           ```\nDefault Prices - _Before_ factoring in rebirth. \n\n`        Wheat`: $24\n`       Potato`: $24\n`       Carrot`: $24\n`  Wheat Seeds`: $1\n`      Pumpkin`: $20\n`  Melon Slice`: $10\n`       Cactus`: $20\n`   Sugar Cane`: $24\n`       Bamboo`: $1\n`         Kelp`: $12\n` Chorus Fruit`: $30\n`         Vine`: $30\n`  Nether Wart`: $30', color=discord.Color(0xECA37E))
        await ctx.send(embed=embed)
    else:
        if crop == 'wheat':
            cost = 24
        elif crop == 'potato':
            cost = 24
        elif crop == 'carrot':
            cost = 24
        elif crop == 'wheatseeds' or crop == 'wheat_seeds' or crop == 'seeds' or crop == 'wheat seeds':
            cost = 1
        elif crop == 'pumpkin':
            cost = 20
        elif crop == 'melon' or crop == 'melonslice':
            cost = 10
        elif crop == 'cactus':
            cost = 20
        elif crop == 'sugarcane':
            cost = 24
        elif crop == 'bamboo':
            cost = 1
        elif crop == 'kelp':
            cost = 12
        elif crop == 'chorus' or crop == 'chorusfruit' or crop == 'chorus fruit':
            cost = 30
        elif crop == 'vine':
            cost = 30
        elif crop == 'wart' or crop == 'nether wart' or crop == 'netherwart':
            cost = 30
        try:
            await ctx.send(f'```{crop}: ${cost}```')
        except UnboundLocalError:
            await ctx.send(f'```"{crop}" not found. ```')

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)