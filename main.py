import discord
from discord.ext import commands
from secrets import token_id
import os
import time
import asyncio
import math


upTime = time.time()

intents = discord.Intents.all()

server_name = "friends"
devMode = False

client =  commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')

missing_req_arg = "You are missing a required arugment, look at the usage above and try again"


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("hi! im a bot"))
    print("Bot is online.")
    channel = client.get_channel(808083925507112960)
    await channel.send("**ALERT:** Bot is online")

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="member")
    channel = client.get_channel(808773981200842822)
    await discord.Member.add_roles(member, role)
    embed = discord.Embed(title='New Member', color=0xf40000)
    embed.add_field(name="New User: ", value=f'{member}', inline=False)
    embed.add_field(name="Welcome message: ", value=f"Hey, {member}! Welcome to {server_name}!")
    await channel.send(embed=embed)






@client.command()
@commands.has_permissions(administrator=True)
async def test(ctx):
    await ctx.send(f'{ctx.author} has issued the test command, checking if elgible for bot status....')
    user = ctx.author
    allowed_user = client.get_user(463016897110343690)
    if user == allowed_user:
        await ctx.send(f'{user} has ran the test command with the corect permissions. Direct messaging them bot information...')
        await user.send(f'Bot information: \n**Server name:** {server_name}\n**Bot uptime:** {round(time.time() - upTime)} seconds\n**Dev Mode:** {devMode}')
    else:
        await ctx.send(f'{user}, you do not have permission to run the test command. If you think this is a mistake, please contact {allowed_user}')






@client.command()
@commands.has_permissions(administrator=True)
async def ban_f(ctx, member: discord.Member, *, arg=None):
    await ctx.author.send(f"Note, this is not a real ban command, you have only fake banned {member}")
    await ctx.send(f'{ctx.author} has banned {member} for {arg}.')
    await member.send(f'You have banned in {server_name} for {arg}.')



@client.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx,member: discord.Member,*,arg):
    role =  discord.utils.get(member.guild.roles, name=arg)
    await discord.Member.add_roles(member, role)
    await ctx.send(f"{member} has received the role: **{role}**")
    
    
@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx,member: discord.Member,*,arg):
    role =  discord.utils.get(member.guild.roles, name=arg)
    await discord.Member.remove_roles(member, role)
    await ctx.send(f"{member} has been removed from the role: **{role}**")



@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)



@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, arg):
    if member == ctx.author:
        await ctx.send("You cannot kick yourself!")
    else:
        embed = discord.Embed(title="Member kicked: ", color=0xf40000)
        embed.add_field(name="Kicked: ", value=f"Reason: {arg}", inline=False)
        embed.add_field(name="User kicked: ", value=f"{member.mention}", inline=False)
        embed.add_field(name="Kicked by: ", value=f'{ctx.author}', inline=False)
        await member.send(f'You have been kicked in {server_name} for **{arg}**!')

        await ctx.send(embed=embed)

        await member.kick(reason=arg)



@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, arg):
    user = member.mention
    embed = discord.Embed(title="Warning issued: ", color=0xf40000)
    embed.add_field(name="Warning: ", value=f'Reason: {arg}', inline=False)
    embed.add_field(name="User warned: ", value=f'{member.mention}', inline=False)
    embed.add_field(name="Warned by: ", value=f'{ctx.author}', inline=False)
    await member.send(f'You have been warned in {server_name} for **{arg}**!')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return 

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, arg):
    if member == ctx.author:
        await ctx.send("You cannot ban yourself!")
    else:
        embed = discord.Embed(title='Member banned', color=0xf40000)
        embed.add_field(name='Banned: ', value=f'Reason: {arg} ', inline=False)
        embed.add_field(name='User banned: ', value=f'{member}', inline=False)
        embed.add_field(name='Banned by:', value=f'{ctx.author}', inline=False)
        await member.send(f'You have been banned in {server_name} for **{arg}**!')

        await ctx.send(embed=embed)

        await member.ban(reason=arg)



@client.command(aliases=['help', 'commands'])
async def cmds(ctx):
    embed = discord.Embed(title="Dinner Club Commands: ", color=0xf40000)
    embed.add_field(name=".addrole", value="Description: The add role command is to add a role to a user, you need the admin permission for this command.", inline=False)
    embed.add_field(name=".ban", value="Description: This is the command to ban a user, you need the ban members permission for this command", inline=False)
    embed.add_field(name='.kick', value="Description: This is the command to kick a user, you need the kick members permission for this command", inline=False)
    embed.add_field(name='.purge', value="Description: This is the command to purge a channel, you need the manage messages permission for this command", inline=False)
    embed.add_field(name=".unban", value="Description: This is the command to unban a user, you need the ban members permission for this command", inline=False)
    embed.add_field(name=".warn", value="Description: This is the command to warn a user, you need the kick members permission for this command.", inline=False)
   
   
    embed.add_field(name=".removerole", value="Description: The remove role command is to add a role to a user, you need the admin permission for this command.", inline=False)
    
    await ctx.send(embed=embed)



# Error handling




@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.addrole    (mention valid user)    (role)**\n**Error:**     {missing_req_arg}")



@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.removerole    (mention valid user)    (role)**\n**Error:**     {missing_req_arg}")


@ban_f.error
async def banfake_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.ban_f     (mention valid user)    (reason)**\n**Error:**    {missing_req_arg}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to run this command!")


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.purge     (number of messages)**\n**Error:**    {missing_req_arg}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to run this command!")

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only bot admins can run the bot test command!")


@kick.error
async def kick_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **kick members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.kick      (mention valid user)**\n**Error:**      {missing_req_arg}")


@ban.error
async def ban_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **ban members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.ban      (mention valid user)**\n**Error:**      {missing_req_arg}")

@warn.error
async def warn_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **kick members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.warn      (mention valid user)**\n**Error:**      {missing_req_arg}")

@unban.error
async def unban_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **ban members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.unban      (mention valid user)**\n**Error:**      {missing_req_arg}")


client.run("TOKEN HERE")
