import discord
from discord.ext import commands

ninoToken = "Discord_Bot_Token"

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="ninotalk", description="Send a message with Nino to a specific channel")
@commands.has_role(1121063615106142329)
# pycord will figure out the types for you
async def add(ctx, channel: discord.TextChannel, message: discord.Option(str)):
    # you can use them as they were actual integers
    if str(channel.id) == "1121067425731989524":
        await channel.send(message)
        await ctx.respond(f'<:NinoBlue:1205472560842539028> successfuly sent the message "{message}" sent to <#{channel.id}> !')
    else:
        await ctx.respond("You can use the `/ninotalk` command only in <#1205476033642496030>", ephemeral=True)

@add.error
async def your_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You can use the `/ninotalk` command only if you are part of <@&1121063615106142329>", ephemeral=True)
    

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="🤖┊bot")
    print(f"Welcome, {member}!")

    if channel:  # Ensure the channel was found
        await channel.send(f"Ciao, {member.mention}! It's a pleasure to have you here! <:NinoBlue:1205472560842539028>")
    else:
        print("The channel 🤖┊bot was not found.")

@bot.event
async def on_message(message):
    # Don't let the bot react to its own messages.
    if message.author == bot.user:
        return

    # Check if the message is in the specific channel.
    if message.channel.name == "🌍┊risorse":
        emoji = discord.utils.get(bot.emojis, id=1205472560842539028)
        if emoji:  # If the emoji was found
            try:
                await message.add_reaction(emoji)
            except discord.HTTPException as e:
                print(f"Failed to add reaction: {e}")
        else:
            print("Emoji not found.")
    
    if message.channel.name == "🚀┊risultati":
        await message.add_reaction("🚀")
        

bot.run(ninoToken)