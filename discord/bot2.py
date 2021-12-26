import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
client.remove_command('help')
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
	embed = discord.Embed(title='📚  **[ UMORIA WIKI ]**', description=' >   Stack up on useless information\n >   The wiki is organized into Discord threads. \n >   Click one of the links to jump to an archived thread. ', color=discord.Color(0x8FB6AB))
	embed.add_field(inline=True, name='Chapters', value='**I. Introduction**\nBasic Information About Umoria\n\n**II. Reference**\nGood to know\n\n**III. Server**\nInformation about gameplay\n\n**IV. Player**')
	embed.add_field(inline=True, name='Sections', value='i : [info](https://discord.com/channels/747233433511788637/910695916359544912/910695919475904583) \nii : [faq](https://discord.com/channels/747233433511788637/910695995866767380/910695998777618493) \n\nr1 : [numeral](https://discord.com/channels/747233433511788637/910696220069097542/910696222887641118)\nr2 : [value](https://discord.com/channels/747233433511788637/910696273626152980/910696277782708254)\n\ni : [blessing](https://discord.com/channels/747233433511788637/910696370292264981/910696374192980068)\nii: [npc](https://discord.com/channels/747233433511788637/910696408431075369/910696411769765888)\n\ni : [armor](https://discord.com/channels/747233433511788637/910696495215415336/910696498054967396)\nii : [tools](https://discord.com/channels/747233433511788637/910696547455496252/910696550915797002)')
	embed.add_field(inline=True, name='\u200b', value='iii : [ip](https://discord.com/channels/747233433511788637/910696029488304198/910696031350566963) \niv : [discord](https://discord.com/channels/747233433511788637/910696074358960209/910696076753920050)\n\nr3 : [commands](https://discord.com/channels/747233433511788637/910696329607528459/910696332811968593)\n\n\niii : [quests](https://discord.com/channels/747233433511788637/910696450697093141/910696453490495488)')#'')
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
	await client.process_commands(message)

if __name__ == '__main__':
	client.run(TOKEN)