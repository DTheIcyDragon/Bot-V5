from datetime import datetime

import discord
from discord.ext import commands

import SETTINGS


class Dragon(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.persistent_views_added = False

    async def on_ready(self) -> None:
        if not self.persistent_views_added:
            print(f"""
Logged in as {self.user.name}#{self.user.discriminator} {self.user.id}
at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}""")
#            self.add_view(PersistentView())
            self.persistent_views_added = True

client = Dragon(
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
    strip_after_prefix=True,
    intents = discord.Intents.all(),
    debug_guilds = SETTINGS.GUILDS,
    activity = discord.Activity(type = discord.ActivityType.playing,
                                name = "Modmail"),
    state = discord.Status.online)


if __name__ == '__main__':
    client.load_extension('cogs.join2create')
    client.run(SETTINGS.TOKEN)