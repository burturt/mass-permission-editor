import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix='rd-', description='A utility bot to help apply mass permission changes',
                   help_command=commands.DefaultHelpCommand(no_category='Commands'))


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
        exceptioncount = 0
        for channel in ctx.message.channel_mentions:
            try:
                await channel.set_permissions(role, reason=f'{ctx.author.name}({ctx.author.id})', read_messages=True)
                await channel.set_permissions(everyone, reason=f'{ctx.author.name}({ctx.author.id})',
                                              read_messages=False)
                await ctx.send(f"Channel overrides set for role {role.name} on channel {channel.name}")
            except:
                await ctx.send("An unknown error occurred. Does the bot have permission to modify roles?")
                exceptioncount += 1
                if (exceptioncount >= 3):
                    await ctx.send("An error has occurred at least 3 times - cancelling")
                    return


@bot.command(name='masscategorychildadd',
             help='Mass add role as allow view channel and everyone deny view in all channels under category')
async def masscategorychildadd(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You do not have permission to use this command')
        return
    if not len(ctx.message.channel_mentions) == 1:
        await ctx.send('I need one channel mention; no more, no less. Aboirting')
        return
    channels = ctx.message.channel_mentions[0].category.text_channels
    role = ctx.message.role_mentions[0]
    everyone = ctx.message.guild.default_role
    exceptioncount = 0
    for channel in channels:
        try:
            await channel.set_permissions(role, reason=f'{ctx.author.name}({ctx.author.id})', read_messages=True)
            await channel.set_permissions(everyone, reason=f'{ctx.author.name}({ctx.author.id})', read_messages=False)
            await ctx.send(f"Channel overrides set for role {role.name} on channel {channel.name}")
        except:
            await ctx.send("An unknown error occurred. Does the bot have permission to modify roles?")
            exceptioncount += 1
            if (exceptioncount >= 3):
                await ctx.send("An error has occurred at least 3 times - cancelling")
                return


@bot.command(name='clearperms', help='Clears the permissions of all mentioned roles and channels')
async def clearperms(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You do not have permission to use this command')
        return

    # Clear roles
    if len(ctx.message.role_mentions) == 0:
        await ctx.send("No roles mentioned; aborting")
        return
    noperms = discord.Permissions(permissions=0)
    exceptioncount = 0
    for role in ctx.message.role_mentions:
        print(role)
        try:
            await role.edit(reason=f'{ctx.author.name}({ctx.author.id})', permissions=noperms)
            await ctx.send(f'Role {role.name} permissions cleared')
        except:
            await ctx.send("An unknown error occurred. Does the bot have permission to modify roles?")
            exceptioncount += 1
            if (exceptioncount >= 3):
                await ctx.send("An error has occurred at least 3 times - cancelling")
                return

    # Clear channels
    if len(ctx.message.channel_mentions) == 0:
        await ctx.send("No channels mentioned")
        return
    exceptioncount = 0
    for channel in ctx.message.channel_mentions:
        await ctx.send(f'Clearing permission overwrites for channel {channel.name}...')
        print(channel)
        try:
            overwrites = channel.overwrites
            for key in overwrites:
                await channel.set_permissions(key, reason=f'{ctx.author.name}({ctx.author.id})', overwrite=None)
        except Exception as e:
            await ctx.send(f"An unknown error occurred: {str(e)}")
            exceptioncount += 1
            if (exceptioncount >= 3):
                await ctx.send("An error has occurred at least 3 times - cancelling")
                return

        await ctx.send(f'Channel {channel.name} overwrites cleared')


@bot.command(name='clearcategoryperms', help='Clear override permissions on a category given its id. Mention any '
                                             'channel within a category to have that category\'s permissions cleared.')
async def clearcategoryperms(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You do not have permission to use this command')
        return
    if ctx.message.channel_mentions == 0:
        await ctx.send('No mentioned channels; exiting')
        return
    uniquecategores = []
    for channel in ctx.message.channel_mentions:
        if not channel.category in uniquecategores:
            uniquecategores.append(channel.category)
    exceptioncount = 0
    for category in uniquecategores:
        await ctx.send(f'Clearing permission overwrites for category {category.name}...')
        print(category)
        try:
            overwrites = category.overwrites
            for key in overwrites:
                await category.set_permissions(key, reason=f'{ctx.author.name}({ctx.author.id})', overwrite=None)
        except Exception as e:
            await ctx.send(f"An unknown error occurred: {str(e)}")
            exceptioncount += 1
            if (exceptioncount >= 3):
                await ctx.send("An error has occurred at least 3 times - cancelling")
                return

        await ctx.send(f'category {category.name} overwrites cleared')


@bot.command(name='clearcategorychildrenperms',
             help='Clears permissions for all channels under category of mentioned channel')
async def clearcategorychildrenperms(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You do not have permission to use this command')
        return
    if not len(ctx.message.channel_mentions) == 1:
        await ctx.send('I need one channel mention, no more, no less; exiting')
        return
    category = ctx.message.channel_mentions[0].category
    exceptioncount = 0
    for channel in category.channels:
        await ctx.send(f'Clearing permission overwrites for channel {channel.name}...')
        print(channel)
        try:
            overwrites = channel.overwrites
            for key in overwrites:
                await channel.set_permissions(key, reason=f'{ctx.author.name}({ctx.author.id})', overwrite=None)
        except Exception as e:
            await ctx.send(f"An unknown error occurred: {str(e)}")
            exceptioncount += 1
            if (exceptioncount >= 3):
                await ctx.send("An error has occurred at least 3 times - cancelling")
                return

        await ctx.send(f'Channel {channel.name} overwrites cleared')


bot.run(TOKEN)
