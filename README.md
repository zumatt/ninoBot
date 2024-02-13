# Nino: an assistat for the Designing With Discord channel
[![Deploy on Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/deploy-on-spaces-md.svg)](https://huggingface.co/spaces/zumat/ninoBot)

Nino is entirely developed using [Pycord](https://docs.pycord.dev/) and hosted on [Plexynodes](https://client.pylexnodes.net/).

![ninobot](https://raw.githubusercontent.com/zumatt/ninoBot/main/assets/ninoBotAvatar.jpg)

The capabilites are the following:
  - Command to send messages via a specific channel only for admin users;
  - Welcome user as soon as they join the server;
  - Reaction to messages sent on specific channels;
  - Capability to generate audio and song using MAGNeT;
  - Capability to generate text using LLaMa.

## Code breakout and examples
_More explanation will arrive soon..._

In order to catch events on the Discord Server you need to set the intents for what you need to check for as True
```
intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = discord.Bot(intents=intents)
```

