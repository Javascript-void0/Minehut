import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
# client.remove_command('help')
TOKEN = os.getenv("CHAT")
guild = None

@client.event
async def on_ready():
    global guild
    print('[ + ] Started {0.user}'.format(client))
    await client.wait_until_ready()
    guild = client.get_guild(747233433511788637)
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

@client.command(help='Wiki Table of Contents')
async def wiki(ctx):
    embed = discord.Embed(title='📚  **[ UMORIA WIKI ]**   Stack up on useless information', description='   The wiki is organized into Discord threads. \n   Click one of the links to jump to an archived thread. ', color=discord.Color(0x8FB6AB))
    embed.add_field(name='```I. Introduction```', value='       i : [info](https://discord.com/channels/747233433511788637/910695916359544912/910695919475904583) ii : [faq](https://discord.com/channels/747233433511788637/910695995866767380/910695998777618493) iii : [ip](https://discord.com/channels/747233433511788637/910696029488304198/910696031350566963) iv : [discord](https://discord.com/channels/747233433511788637/910696074358960209/910696076753920050)')
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if not message.author.name == 'Java' and not message.author.discriminator == 3865:
            await message.delete()
    if "Blessing" in message.content and message.channel.name == 'portal':
        channel = guild.get_channel(873434537802207273)
        msg = message.content
        name = msg.replace('```', '')
        await channel.edit(name=name)
    if ".link" in message.content and message.channel.name != "link":
        await message.delete()
        await message.channel.send('```This command can only be used in #link```', delete_after=3)

if __name__ == '__main__':
    client.run(TOKEN)