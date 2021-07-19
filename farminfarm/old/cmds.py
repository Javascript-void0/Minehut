import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("CMDS")
GUILD = None
CONSOLE = None

@client.event
async def on_ready():
    global GUILD, CONSOLE
    GUILD = client.get_guild(747233433511788637)
    CONSOLE = GUILD.get_channel(751663682856943716)
    await client.change_presence(activity=discord.Game(name="Staff Commands"))
    print('[ + ] Started {0.user}'.format(client))

@client.command(help='.kick <player> [reason]')
@commands.has_role("Staff Team")
async def kick(ctx, player, reason=None):
    global CONSOLE
    await CONSOLE.send(f'kick {player} {reason}')
    await ctx.send(f'```Kicked {player} for {reason}```')

@client.command(help='.kick <player> [reason]')
@commands.has_role("Staff Team")
async def ban(ctx, player, reason=None):
    global CONSOLE
    await CONSOLE.send(f'ban {player} {reason}')
    await ctx.send(f'```Banned {player} for {reason}```')

@client.command(help='.mutechat')
@commands.has_role("Staff Team")
async def mutechat(ctx):
    global CONSOLE
    await CONSOLE.send('mutechat')
    await ctx.send(f'```Muted/Unmuted Chat (idk which)```')

@client.command(help='.clearchat')
@commands.has_role("Staff Team")
async def clearchat(ctx):
    global CONSOLE
    await CONSOLE.send('clearchat')
    await ctx.send(f'```Cleared Chat```')

@client.command(help='.mute <player> [reason]')
@commands.has_role("Staff Team")
async def mute(ctx, player, reason=None):
    global CONSOLE
    await CONSOLE.send(f'mute {player} {reason}')
    await ctx.send(f'```Muted/Unmuted {player} for {reason} (idk which)```')

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)