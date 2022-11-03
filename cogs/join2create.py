import json

import discord
from discord.ext import commands

import SETTINGS
import embeds


def is_owner(user_id: int, voice_id: int) -> bool:
    with open("db/tempchannel.json", "r") as r:
        data: dict = json.load(r)
    if data[str(voice_id)]["owner"] == user_id:
        return True
    return False


def is_locked(voice_id: int) -> bool:
    with open("db/tempchannel.json", "r") as r:
        data: dict = json.load(r)
    if data[str(voice_id)]["locked"]:
        return True
    return False


def is_ghosted(voice_id: int) -> bool:
    with open("db/tempchannel.json", "r") as r:
        data: dict = json.load(r)
    if data[str(voice_id)]["ghosted"]:
        return True
    return False


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
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**")

        if is_owner(user_id = member.id, voice_id = channel.id):

            try:
                value = int(self.children[0].value)

                if value < 0:
                    await interaction.response.send_message(f"Please write a positive number.",
                                                            ephemeral = True,
                                                            delete_after = 5)

                if value == 0:
                    await interaction.response.send_message(f"Removed max members limit.",
                                                            ephemeral = True,
                                                            delete_after = 5)

                await interaction.response.send_message(f"Max members adjusted to {value}.",
                                                        ephemeral = True,
                                                        delete_after = 5)

                await channel.edit(user_limit = value)

            except ValueError:
                await interaction.response.send_message(f"**You messed up to write a valid number!**",
                                                        ephemeral = True,
                                                        delete_after = 5)

            except discord.errors.InteractionResponded:
                pass

        else:
            try:
                await interaction.response.send_message(f"**You are not the owner of the channel.**",
                                                        ephemeral = True,
                                                        delete_after = 5)
            except discord.errors.InteractionResponded:
                pass


class BitrateModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label = "Bitrate",
            min_length = 1,
            max_length = 3,
            placeholder = "Default is 64"))

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**")

        if is_owner(user_id = member.id, voice_id = channel.id):

            try:
                value = int(self.children[0].value)

                if value < 8:
                    await interaction.response.send_message(f"Please don't write a number larger then 8.",
                                                            ephemeral = True,
                                                            delete_after = 5)

                if value > 128:
                    await interaction.response.send_message(f"Please don't write a number larger then 128.",
                                                            ephemeral = True,
                                                            delete_after = 5)

                await interaction.response.send_message(f"Bitrate adjusted to {value}.",
                                                        ephemeral = True,
                                                        delete_after = 5)

                await channel.edit(bitrate = value * 1000)

            except ValueError:
                await interaction.response.send_message(f"**You messed up to write a valid number!**",
                                                        ephemeral = True,
                                                        delete_after = 5)

            except discord.errors.InteractionResponded:
                pass

        else:
            try:
                await interaction.response.send_message(f"**You are not the owner of the channel.**",
                                                        ephemeral = True,
                                                        delete_after = 5)
            except discord.errors.InteractionResponded:
                pass


class RenameModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label = "New Name",
            min_length = 1,
            max_length = 100,
            placeholder = "My supercool channel"))

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**")

        if is_owner(user_id = member.id, voice_id = channel.id):
            await channel.edit(name = self.children[0].value)
            await interaction.response.send_message(f"**Channel name changed to \"{self.children[0].value}\"**",
                                                    ephemeral = True,
                                                    delete_after = 5)

        else:
            try:
                await interaction.response.send_message(f"**You are not the owner of the channel.**",
                                                        ephemeral = True,
                                                        delete_after = 5)
            except discord.errors.InteractionResponded:
                pass


class Join2CreateView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Rename",
                       custom_id = "pers:but:ReNaMe")
    async def rename_button(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(RenameModal(title = "Rename channel"))

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Limit users",
                       custom_id = "pers:but:LiMiT_uSeRs")
    async def max_user_button(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(MaxUsersModal(title = "Set max users"))

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Lock",
                       custom_id = "pers:but:LoCk")
    async def lock_button(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        verified_role = guild.get_role(SETTINGS.VERIFY_ROLE)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**",
                                                           ephemeral = True,
                                                           delete_after = 5)

        if is_owner(user_id = member.id, voice_id = channel.id):
            if is_locked(channel.id):
                overwritten = {
                    guild.default_role: discord.PermissionOverwrite(view_channel = False),
                    member: discord.PermissionOverwrite(connect = True,
                                                        speak = True),
                    verified_role: discord.PermissionOverwrite(connect = True,
                                                               speak = True)
                }
                with open("db/tempchannel.json", "r") as r:
                    data: dict = json.load(r)
                data[str(channel.id)]["locked"] = False
                with open("db/tempchannel.json", "w") as w:
                    json.dump(data, w, indent = 4)
                await channel.edit(overwrites = overwritten)
                await interaction.response.send_message(f"**Your channel is now unlocked for {verified_role.name}**")

            else:
                overwritten = {
                    guild.default_role: discord.PermissionOverwrite(view_channel = False),
                    member: discord.PermissionOverwrite(connect = True,
                                                        speak = True),
                    verified_role: discord.PermissionOverwrite(connect = False,
                                                               speak = True)
                }
                with open("db/tempchannel.json", "r") as r:
                    data: dict = json.load(r)
                data[str(channel.id)]["locked"] = True
                with open("db/tempchannel.json", "w") as w:
                    json.dump(data, w, indent = 4)
                await channel.edit(overwrites = overwritten)
                await interaction.response.send_message(f"**Your channel is now locked for {verified_role.name}**")

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Take ownership",
                       custom_id = "pers:but:TaKe_OwNeR")
    async def take_owner_button(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**",
                                                           ephemeral = True,
                                                           delete_after = 5)

        with open("db/tempchannel.json", "r") as r:
            data: dict = json.load(r)

        old_owner = data[str(channel.id)]["owner"]
        if old_owner in [member.id for member in channel.members]:
            await interaction.response.send_message("**The owner is still in the channel.**",
                                                    ephemeral = True,
                                                    delete_after = 5)
        else:
            data[str(channel.id)]["owner"] = member.id
            with open("db/tempchannel.json", "w") as w:
                json.dump(data, w, indent = 4)
            await interaction.response.send_message("**You are now the new owner!**",
                                                    ephemeral = True,
                                                    delete_after = 5)
            await channel.send(f"**{member.display_name} is now the new owner of this channel!**")
            await channel.edit(name = f"{member.display_name}'s channel")

    # @discord.ui.button(style = discord.ButtonStyle.blurple,
    #                   label = "Permit",
    #                   custom_id = "pers:but:PeRmIt")
    # async def permit_button(self, button: discord.Button, interaction: discord.Interaction):
    #    pass # await interaction.response.send_message(view = PermitView(guild = interaction.guild))

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Ghost",
                       custom_id = "pers:but:GhOsT")
    async def ghost_button(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        verified_role = guild.get_role(SETTINGS.VERIFY_ROLE)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**",
                                                           ephemeral = True,
                                                           delete_after = 5)

        if is_owner(user_id = member.id, voice_id = channel.id):
            if is_ghosted(channel.id):
                overwritten = {
                    guild.default_role: discord.PermissionOverwrite(view_channel = False),
                    member: discord.PermissionOverwrite(connect = True,
                                                        speak = True),
                    verified_role: discord.PermissionOverwrite(connect = False,
                                                               speak = True,
                                                               view_channel = True)
                }
                with open("db/tempchannel.json", "r") as r:
                    data: dict = json.load(r)
                data[str(channel.id)]["ghosted"] = False
                with open("db/tempchannel.json", "w") as w:
                    json.dump(data, w, indent = 4)
                await channel.edit(overwrites = overwritten)
                await interaction.response.send_message(f"**Your channel is now visible for {verified_role.name}**")

            else:
                overwritten = {
                    guild.default_role: discord.PermissionOverwrite(view_channel = False),
                    member: discord.PermissionOverwrite(connect = True,
                                                        speak = True),
                    verified_role: discord.PermissionOverwrite(connect = True,
                                                               speak = True,
                                                               view_channel = False)
                }
                with open("db/tempchannel.json", "r") as r:
                    data: dict = json.load(r)
                data[str(channel.id)]["ghosted"] = True
                with open("db/tempchannel.json", "w") as w:
                    json.dump(data, w, indent = 4)
                await channel.edit(overwrites = overwritten)
                await interaction.response.send_message(f"**Your channel is now invisible for {verified_role.name}**")

    @discord.ui.button(style = discord.ButtonStyle.blurple,
                       label = "Bitrate",
                       custom_id = "pers:but:BiTrAtE")
    async def bitrate_button(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(f"**You are not in a voice channel.**",
                                                           ephemeral = True,
                                                           delete_after = 5)

        if is_owner(user_id = member.id, voice_id = channel.id):
            await interaction.response.send_modal(BitrateModal(title = "Set the Bitrate"))


class JoinToCreate(commands.Cog):
    def __init__(self, client):
        self.client: discord.Bot = client

    @commands.command(name = "Join2Create")
    @commands.has_permissions(administrator = True)
    async def join2create(self, ctx):

        em = discord.Embed(title = "**Voice Dashboard**",
                           color = discord.Color.dark_purple())
        em.add_field(name = "Rename", value = "If you are the channel owner you can rename the channel")
        em.add_field(name = "Limit users",
                     value = "If you are the channel owner you can set the maximal amount of members in a voice channel")
        em.add_field(name = "Lock", value = f"Lock your voice channel for <@&{SETTINGS.VERIFY_ROLE}>")
        em.add_field(name = "Take ownership", value = "If the old owner left the channel you can take ownership")
        # em.add_field(name = "Permit", value = "Allow or disallow users or roles to your channel")
        em.add_field(name = "Ghost", value = "Allow your channel to be seen by the public or not")
        em.add_field(name = "Bitrate", value = "Edit the voice quality of your channel")
        await ctx.channel.send(embed = em, view = Join2CreateView())

    @commands.Cog.listener("on_voice_state_update")
    async def on_join(self,
                      member: discord.Member,
                      before: discord.VoiceState,
                      after: discord.VoiceState) -> None:

        try:
            if member.voice.channel.id == SETTINGS.JOIN2CREATE:
                new_voice = await after.channel.category.create_voice_channel(name = f"{member.display_name}'s-channel",
                                                                              reason = f"Join2Create {member.name}#{member.discriminator}")
                await member.move_to(new_voice, reason = "Join2Create")

                with open("db/tempchannel.json", "r") as r:
                    data: dict = json.load(r)
                data[str(new_voice.id)] = {}
                data[str(new_voice.id)]["owner"] = member.id
                data[str(new_voice.id)]["locked"] = False
                data[str(new_voice.id)]["ghosted"] = False
                with open("db/tempchannel.json", "w") as w:
                    json.dump(data, w, indent = 4)

        except AttributeError:
            pass

    @commands.Cog.listener("on_voice_state_update")
    async def on_leave(self,
                       member: discord.Member,
                       before: discord.VoiceState,
                       after: discord.VoiceState) -> None:

        temp_channels = []
        with open("db/tempchannel.json", "r") as f:
            data: dict = json.load(f)
        for entry, _ in data.items():
            temp_channels.append(int(entry))

        try:
            if before.channel.id in temp_channels:
                if len(before.channel.members) == 0:
                    with open("db/tempchannel.json", "r") as r:
                        data = json.load(r)
                    data.pop(str(before.channel.id))
                    with open("db/tempchannel.json", "w") as w:
                        json.dump(data, w, indent = 4)
                    await before.channel.delete(reason = "Join2Delete")

        except AttributeError:
            pass

    @commands.slash_command(name = "permit",
                            description = "Allow access to your personal channel")
    async def permit_cmd(self,
                         ctx: discord.ApplicationContext,
                         mention: discord.Option(discord.abc.Mentionable),
                         allow: discord.Option(bool)):
        guild = ctx.guild
        member = guild.get_member(ctx.author.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await ctx.response.send_message(f"**You are not in a voice channel.**",
                                                   ephemeral = True,
                                                   delete_after = 5)

        if is_owner(user_id = member.id, voice_id = channel.id):
            overwritten = {
                mention: discord.PermissionOverwrite(connect = allow,
                                                     speak = allow)
            }
            await channel.edit(overwrites = overwritten)
            await ctx.response.send_message(embed = embeds.embed_success(f"{['Allowed' if allow else 'Denied']} access for {mention.mention}".strip("['']")))



def setup(client):
    client.add_cog(JoinToCreate(client))
