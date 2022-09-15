import discord
from discord.ext import commands

import SETTINGS


class Dragon(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.persistent_views_added = False

    async def on_ready(self) -> None:
        if not self.persistent_views_added:
#            self.add_view(PersistentView())
            self.persistent_views_added = True

client = Dragon(
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
    strip_after_prefix=True,
    intents = discord.Intents.all(),
    debug_guilds = [SETTINGS.GUILDS],
    activity = discord.Activity(type = discord.ActivityType.playing,
                                name = "Modmail"),
    state = discord.Status.online)
