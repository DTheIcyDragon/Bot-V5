import datetime
import json

import discord
from discord.ext import commands

class Join2Create(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        try:

            if after.channel.id == 894929343715885108:
                new_channel = await after.channel.category.create_voice_channel(name = f"{member.name}")
                with open("db/tempvoice.json", "r") as f:
                    data = json.load(f)
                data[f"voice:{new_channel.id}"] = new_channel.id
                with open("db/tempvoice.json", "w") as w:
                    json.dump(data, w, indent = 4)
                await member.move_to(new_channel)
                await new_channel.send(embed = discord.Embed(
                    title = "Channel Dashboard",
                    description = "Allow's you to modify your the channel.",
                    color = discord.Color.brand_green(),
                    timestamp = datetime.datetime.now()
                ))

            if len(before.channel.members) == 0:
                with open("db/tempvoice.json", "r") as f:
                    data = json.load(f)
                for key, entry in data.items():
                    if before.channel.id == int(entry):

                        with open("db/tempvoice.json", "w") as f:
                            del(data[key])
                        json.dump(data, f, indent = 4)
                        await before.channel.delete(reason = "TempChannel empty")
                    else:
                        pass
            else:
                pass
        except AttributeError:
            print("at error")


def setup(client):
    client.add_cog(Join2Create(client))