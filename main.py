# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='rd-')


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')


@bot.command(name='massadd', help='Sets the view channel permission to allow for a role and set view channel for '
                                  'everyone to deny')
async def massadd(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You do not have permission to use this command')
    else:
        if not len(ctx.message.role_mentions) == 1:
            await ctx.send("I can only deal with one role at a time, sorry")
            return
        elif len(ctx.message.channel_mentions) == 0:
            await ctx.send("No channels mentioned; aborting")
            return
        role = ctx.message.role_mentions[0]
        everyone = ctx.message.guild.default_role
        exeptioncount = 0
        for channel in ctx.message.channel_mentions:
            try:
                await channel.set_permissions(role, reason=f'{ctx.author.name}({ctx.author.id})', read_messages=True)
                await channel.set_permissions(everyone, reason=f'{ctx.author.name}({ctx.author.id})', read_messages=False)
                await ctx.send(f"Channel overrides set for role {role.name} on channel {channel.name}")
            except:
                await ctx.send("An unknown error occurred. Does the bot have permission to modify roles?")
                exeptioncount += 1
                if (exeptioncount >= 3):
                    await ctx.send("An error has occurred at least 3 times - cancelling")
                    return



@bot.command(name='clearperms', help='Clears the permissions of all mentioned roles and channels')
async def clearperms(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You do not have permission to use this command')
    else:
        if len(ctx.message.role_mentions) == 0:
            await ctx.send("No roles mentioned")
        else:
            noperms = discord.Permissions(permissions=0)
            exeptioncount = 0
            for role in ctx.message.role_mentions:
                print(role)
                try:
                    await role.edit(reason=f'{ctx.author.name}({ctx.author.id})', permissions=noperms)
                    await ctx.send(f'Role {role.name} permissions cleared')
                except:
                    await ctx.send("An unknown error occurred. Does the bot have permission to modify roles?")
                    exeptioncount += 1
                    if (exeptioncount >= 3):
                        await ctx.send("An error has occurred at least 3 times - cancelling")
                        return

        # Clear channels
        if len(ctx.message.channel_mentions) == 0:
            await ctx.send("No channels mentioned")
        else:
            exeptioncount = 0
            for channel in ctx.message.channel_mentions:
                await ctx.send(f'Clearings permission overwrites for channel {channel.name}...')
                print(channel)
                try:
                    overwrites = channel.overwrites
                    for key in overwrites:
                        await channel.set_permissions(key, reason=f'{ctx.author.name}({ctx.author.id})', overwrite=None)
                except Exception as e:
                    await ctx.send(f"An unknown error occurred: {str(e)}")
                    exeptioncount += 1
                    if (exeptioncount >= 3):
                        await ctx.send("An error has occurred at least 3 times - cancelling")
                        return

                await ctx.send(f'Channel {channel.name} overwrites cleared')


bot.run(TOKEN)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
