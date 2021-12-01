import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("CHAT")

@client.event
async def on_ready():
    print(f'Started {client.user}')

@client.command(help='Rules Embed')
async def rules2(ctx):
    embed = discord.Embed(title='FarminFarm Discord Rules', description='', color=discord.Color(0xECA37E))
    embed.add_field(name='`1.` Keep All Channels SFW', value='> Keep all topics and images clean. Limit swearing. \n|', inline=False)
    embed.add_field(name='`2.` Use channels For Their Proper Use', value="> Don't misuse channels. Each of them have their uses. \n:", inline=False)
    embed.add_field(name='`3.` English Only', value='> Due to all of out staff mainly speaking English, it is required to \n> speak English only. They can not moderate something theat they \n> do not understand. \n|', inline=False)
    embed.add_field(name="`4.` Don't Spam / Flood", value='> This includes character spam, image spam, copy and pasting \n> large text, etc. \n:', inline=False)
    embed.add_field(name='`5.` Respect Everyone', value="> Respect all users and their opinions. Please don't insult, bully, or \n> harass anyone. \n|", inline=False)
    embed.add_field(name="`6.` Don't advertise", value="> Any form of advertising is not allowed. This includes posting \n> invites, sending invites in DMs, advertising social media \n> accounts, etc. \n:", inline=False)
    embed.add_field(name='`7.` Have Common Sense', value="> If you're not sure something is allowed then please don't post it. \n> Not every rule can be listed so you must have common sense. \n|", inline=False)
    embed.add_field(name='`8.` The Staff Team Always Have The Final Say', value="> Don't argue with staff members about their modertation activity. \n> If you don't agree with a moderation actions, please discuss with \n> an admin. \n:", inline=False)
    embed.add_field(name='`9.` Follow Discord TOS', value="> Follow Discord's rules on their pklatform. **[TOS](https://discord.com/terms)**", inline=False)
    embed.set_image(url='https://i.pinimg.com/originals/b7/c0/e8/b7c0e83b3a4582303923f654c3d9c668.gif')
    embed.set_footer(text='Follow These Rules to Not Get Banned :D', icon_url='https://media.tenor.com/images/4223cf9120369eea473fcf3565c4e676/tenor.gif')
    await ctx.send(embed=embed)

@client.command(help='Rules Embed')
async def rules(ctx):
    await ctx.send(embed = ruleEmbed())

@client.command(help='Edit Rule Embed')
async def rulesedit(ctx, id: int):
    new_embed = ruleEmbed()
    
    guild = client.get_guild(747233433511788637)
    channel = guild.get_channel(900145049243902012)
    message = await channel.fetch_message(id) 
    await message.edit(embed=new_embed)

def ruleEmbed():
    embed = discord.Embed(title='Umoria Discord Rules', description='', color=discord.Color(0x8bc077))
    embed.add_field(name='`1.` Keep All Channels SFW', value="> Keep all topics and images clean. Limit swearing. \n> **`2.` Use channels For Their Proper Use**\n> Don't misuse channels. Each of them have their uses. \n> :\n> **`3.` English Only**\n> Due to all of out staff mainly speaking English, it is required to \n> speak English only. They can not moderate something theat they \n> do not understand.", inline=False)
    embed.add_field(name="`4.` Don't Spam / Flood", value="> This includes character spam, image spam, copy and pasting \n> large text, etc.", inline=False)
    embed.add_field(name='`5.` Respect Everyone', value="> Respect all users and their opinions. Please don't insult, bully, or \n> harass anyone.", inline=False)
    embed.add_field(name="`6.` Don't advertise", value="> Any form of advertising is not allowed. This includes posting \n> invites, sending invites in DMs, advertising social media \n> accounts, etc.\n> **`7.` Don't Start Drama**\n> Keep all your disagreements in DMs. Nobody likes to see drama \n> or arguements in chat. Do not insult or bully each other in DMs\n> :\n> **`8.` Have Common Sense**\n> If you're not sure something is allowed then please don't post it. \n> Not every rule can be listed so you must have common sense. \n> :\n> **`9.` The Staff Team Always Have The Final Say**\n> Don't argue with staff members about their modertation activity.\n> If you don't agree with a moderation action, please discuss with \n> an admin.", inline=False)
    embed.add_field(name='`10.` Follow Discord TOS', value="> Follow Discord's rules on their platform. **[TOS](https://discord.com/terms)**", inline=False)
    # embed.set_image(url='https://i.pinimg.com/originals/4c/b4/3d/4cb43d3fc28b1ed77589e0fcfee93fde.gif')
    embed.set_image(url='https://i.imgur.com/LP66YuR.gif')
    # embed.set_image(url='https://i.pinimg.com/originals/b7/c0/e8/b7c0e83b3a4582303923f654c3d9c668.gif')
    embed.set_footer(text='Follow These Rules to Not Get Banned :D', icon_url='https://media.tenor.com/images/4223cf9120369eea473fcf3565c4e676/tenor.gif')
    # await ctx.send(embed=embed)
    return embed

if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)