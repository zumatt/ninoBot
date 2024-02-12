import discord
from discord import File
from discord.ext import commands
from gradio_client import Client
import os

ninoToken = "Discord_Bot_Token"

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    global client
    client = Client("https://fffiloni-magnet.hf.space/--replicas/58jap/")
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


@bot.command(name="ninoaudio", description="Generate audio tracks from text")
@commands.check_any(commands.has_role(1121063615106142329), commands.has_role(1204421985443258498))
async def add(ctx, model: discord.Option(str, "Choose your model", choices=["facebook/magnet-small-10secs", "facebook/magnet-medium-10secs", "facebook/magnet-small-30secs", "facebook/magnet-medium-30secs", "facebook/audio-magnet-small", "facebook/audio-magnet-medium"]), prompt: discord.Option(str)):
    await ctx.respond(f'<:NinoBlue:1205472560842539028> successfuly added in queue!\nYour audio generation with the prompt `{prompt}` using the model {model} has started, in approx. 45s will be available!', ephemeral=True)
    result = client.predict(
		model,	# Literal['facebook/magnet-small-10secs', 'facebook/magnet-medium-10secs', 'facebook/magnet-small-30secs', 'facebook/magnet-medium-30secs', 'facebook/audio-magnet-small', 'facebook/audio-magnet-medium']  in 'Model' Radio component
		"",	# str  in 'Model Path (custom models)' Textbox component
		prompt,	# str  in 'Input Text' Textbox component
		3,	# float  in 'Temperature' Number component
		0.9,	# float  in 'Top-p' Number component
		10,	# float  in 'Max CFG coefficient' Number component
		1,	# float  in 'Min CFG coefficient' Number component
		20,	# float  in 'Decoding Steps (stage 1)' Number component
		10,	# float  in 'Decoding Steps (stage 2)' Number component
		10,	# float  in 'Decoding Steps (stage 3)' Number component
		10,	# float  in 'Decoding Steps (stage 4)' Number component
		"prod-stride1 (new!)",	# Literal['max-nonoverlap', 'prod-stride1 (new!)']  in 'Span Scoring' Radio component
		api_name="/predict_full"
    )

    print("Result generated!")

    # Format the result paths
    parent_folders = []
    result_paths = []
    if isinstance(result[0], dict):
        for key, value in result[0].items():
            if key != "subtitles":
                os.remove(value)
                os.rmdir(os.path.dirname(value))
    for path in result[1:]:
        result_paths.append(path)

    try:
        await ctx.respond(f"<:NinoBlue:1205472560842539028> `{prompt}` generated using the MAGNeT model `{model}` by <@{ctx.author.id}>")
        for index, path in enumerate(result_paths):
            with open(path, 'rb') as fp:
                await ctx.followup.send(file=File(fp, f"{prompt}_{ctx.author}_output_{index}.wav"))
                os.remove(path)
                parent_folders.append(os.path.dirname(path))
        
        for folder in parent_folders:
            os.rmdir(folder)
        
    except Exception as e:
        await ctx.respond(f"Failed to send the audio file: {str(e)}", ephemeral=True)

    

@add.error
async def your_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You can use the `/ninoaudio` command only if you are part of <@&1121063615106142329> or <@&1121063615106142329>", ephemeral=True)
    

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="🤖┊bot")

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