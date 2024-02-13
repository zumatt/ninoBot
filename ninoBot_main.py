import discord
from discord import File
from discord.ext import commands
from gradio_client import Client
import os
import sys
from ninoSecret import ninoToken


# Initialize the bot with the intents
intents = discord.Intents.default()
intents.members = True
intents.messages = True

#Pass the intent variables to the bot
bot = discord.Bot(intents=intents)

# Function that is called as soon as the bot is ready
@bot.event
async def on_ready():
    global clientMAGNeT, magnetAvailable, clientLLaMa, llamaAvailable
    
    try:
        clientMAGNeT = Client("https://fffiloni-magnet.hf.space/--replicas/58jap/")
        magnetAvailable = True
    except Exception as e:
        print(f"Failed to connect to MAGNet: {str(e)}")
        magnetAvailable = False
    
    try:
        clientLLaMa = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/--replicas/brc3o/")
        llamaAvailable = True
    except Exception as e:
        print(f"Failed to connect to MAGNet: {str(e)}")
        llamaAvailable = False

    print(f'{bot.user} has connected to Discord!')

# Function to trigger the command /ninowrite
@bot.command(name="ninowrite", description="Send a message with Nino to a specific channel")
@commands.has_role(1121063615106142329)
# pycord will figure out the types for you
async def ninowrite(ctx, channel: discord.TextChannel, message: discord.Option(str, "Enter your message")):
    await channel.send(message)
    await ctx.respond(f'<:NinoBlue:1205472560842539028> successfuly sent the message `{message}` sent to <#{channel.id}> !')

# Check for errors in the /ninowrite command
@ninowrite.error
async def your_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You can use the `/ninotalk` command only if you are part of <@&1121063615106142329>", ephemeral=True)

# Function to trigger the command /ninoplay
@bot.command(name="ninoplay", description="Generate audio tracks from text")
@commands.check_any(commands.has_role(1121063615106142329), commands.has_role(1204421985443258498))
async def ninoplay(ctx,
              model: discord.Option(str, "Choose your model", choices=["facebook/magnet-small-10secs", "facebook/magnet-medium-10secs", "facebook/magnet-small-30secs", "facebook/magnet-medium-30secs", "facebook/audio-magnet-small", "facebook/audio-magnet-medium"]),
              prompt: discord.Option(str, "Enter your prompt"),
              temperature: discord.Option(float, "Temperature", choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])):
    if magnetAvailable:
        await ctx.respond(f'<:NinoBlue:1205472560842539028> successfuly added in queue!\nYour audio generation with the prompt `{prompt}` using the model `{model}` with the temperature `{temperature}` has started, in approx. 45s will be available!', ephemeral=True)
        result = clientMAGNeT.predict(
            model,	        # Literal['facebook/magnet-small-10secs', 'facebook/magnet-medium-10secs', 'facebook/magnet-small-30secs', 'facebook/magnet-medium-30secs', 'facebook/audio-magnet-small', 'facebook/audio-magnet-medium']  in 'Model' Radio component
            "",	            # str  in 'Model Path (custom models)' Textbox component
            prompt,	        # str  in 'Input Text' Textbox component
            temperature,	# float  in 'Temperature' Number component
            0.9,	        # float  in 'Top-p' Number component
            10,	            # float  in 'Max CFG coefficient' Number component
            1,	            # float  in 'Min CFG coefficient' Number component
            20,	            # float  in 'Decoding Steps (stage 1)' Number component
            10,	            # float  in 'Decoding Steps (stage 2)' Number component
            10,	            # float  in 'Decoding Steps (stage 3)' Number component
            10,	            # float  in 'Decoding Steps (stage 4)' Number component
            "prod-stride1 (new!)",	# Literal['max-nonoverlap', 'prod-stride1 (new!)']  in 'Span Scoring' Radio component
            api_name="/predict_full"
        )

        print(f"{prompt} from {ctx.author} generated!")

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
    else:
        await ctx.respond("The MAGNeT service is currently unavailable, please try again later.", ephemeral=True)

# Check for errors in the /ninoplay command
@ninoplay.error
async def your_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You can use the `/ninoaudio` command only if you are part of <@&1121063615106142329> or <@&1121063615106142329>", ephemeral=True)

# Function to trigger the command /ninochat
@bot.command(name="ninochat", description="Nino LLm chatbot based on LLaMa") 
@commands.check_any(commands.has_role(1121063615106142329), commands.has_role(1204421985443258498))
async def ninochat(ctx,
              model: discord.Option(str, "Choose your model", choices=["llama-2-70b-chat"]),
              prompt: discord.Option(str, "Enter your prompt"),
              temperature: discord.Option(float, "Temperature", choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])):
    if llamaAvailable:
        await ctx.respond(f'<:NinoBlue:1205472560842539028> successfuly added in queue!\nYour text with the prompt `{prompt}` using the model `{model}` and with the temperature `{temperature}` has started, in approx. 24s will be available!', ephemeral=True)
        
        result = clientLLaMa.predict(
            prompt,	# str  in 'parameter_7' Textbox component
            "",	# str  in 'Optional system prompt' Textbox component
            temperature,	# float (numeric value between 0.0 and 1.0) in 'Temperature' Slider component
            1024,	# float (numeric value between 0 and 4096) in 'Max new tokens' Slider component
            0.9,	# float (numeric value between 0.0 and 1) in 'Top-p (nucleus sampling)' Slider component
            1.2,	# float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
            api_name="/chat"
        )

        print(f"{prompt} from {ctx.author} generated!")

        try:
            message_prefix = f"<:NinoBlue:1205472560842539028> the answer to the <@{ctx.author.id}>:\n"
            max_length = 2000 - len(message_prefix) - 10
            chunks = [result[i:i+max_length] for i in range(0, len(result), max_length)]
            await ctx.respond(message_prefix)
            for chunk in chunks:
                await ctx.followup.send(f"{chunk}\n")
        except Exception as e:
            await ctx.respond(f"Failed to retrieve the answer: {str(e)}", ephemeral=True)
    else:
        await ctx.respond("The LLaMa service is currently unavailable, please try again later.", ephemeral=True)

# Check for errors in the /ninochat command
@ninochat.error
async def your_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You can use the `/ninochat` command only if you are part of <@&1121063615106142329> or <@&1121063615106142329>", ephemeral=True)

# Function to trigger the command /restart
@bot.command(name="restart", description="Restart the bot")
@commands.has_role(1121063615106142329)
async def restart(ctx):
    await ctx.send("I'm taking a power nap! <:NinoBlue:1205472560842539028>\nI'll be back in a moment!")
    await bot.logout()
    await bot.close()
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Check for errors in the /ninochat command
@restart.error
async def your_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You can use the `/restart` command only if you are part of <@&1121063615106142329>", ephemeral=True)

# Function that is triggered when a member joins the server
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="🤖┊bot")

    if channel:  # Ensure the channel was found
        await channel.send(f"Ciao, {member.mention}! It's a pleasure to have you here! <:NinoBlue:1205472560842539028>")
    else:
        print("The channel 🤖┊bot was not found.")

# Function that is triggered when a member send a message
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

# -----------------------------------------------------------
# Run the bot in a loop
bot.run(ninoToken)


