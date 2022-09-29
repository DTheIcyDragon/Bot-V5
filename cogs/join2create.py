import json

import discord
from discord.ext import commands

import SETTINGS


class MaxUsersModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label = "Max Users",
            min_length = 1,
            max_length = 2,
            placeholder = "5"))

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        channel = guild.get_channel(member.voice.channel.id)
        try:
            limit = int(self.children[0].value)
            await channel.edit(user_limit = limit)
            if limit == 0:
                await interaction.response.send_message(f"Removed max members limit",
                                                        ephemeral = True)

            await interaction.response.send_message(f"Max members adjusted to {limit}",
                                                    ephemeral = True)

        except ValueError:
            await interaction.response.send_message(f"**You messed up to write a valid number!**",
                                                    ephemeral = True)


class Join2CreateView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Set max users",
                       custom_id = "pers:but:MaX_uSeRs")
    async def max_user_button(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(MaxUsersModal(title = "Set max users"))


class JoinToCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState) -> None:

        temp_channels = []
        with open("db/tempchannel.json", "r") as f:
            data: dict = json.load(f)
        for _, entry in data.items():
            temp_channels.append(entry)
        print(temp_channels)

        if before.channel.id in temp_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete(reason = "Join2Delete")

        elif after.channel.id == SETTINGS.JOIN2CREATE:
            new_voice = await after.channel.category.create_voice_channel(name = f"{member.display_name}'s-channel",
                                                                          reason = f"Join2Create {member.name}#{member.discriminator}")
            await member.move_to(new_voice, reason = "Join2Create")

    @commands.command(name = "Join2Create")
    async def join2create(self, ctx):

        em = discord.Embed(title = "**Voice Dashboard**",
                           color = discord.Color.dark_purple())
        em.add_field(name = "Set max users", value = "Set's the maximum possible amount of members in a voice channel")
        await ctx.channel.send(embed = em, view = Join2CreateView())


def setup(client):
    client.add_cog(JoinToCreate(client))
