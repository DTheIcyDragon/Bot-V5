import datetime

import discord
from discord.ext import commands

import SETTINGS
import cogs.join2create


class Dragon(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.persistent_views_added = False

    async def on_ready(self) -> None:
        print(f"""
Logged in as {self.user.name}#{self.user.discriminator}
Startup @{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
        if not self.persistent_views_added:
            self.add_view(cogs.join2create.Join2CreateView())
            self.persistent_views_added = True
#           self.add_view(PersistentView())


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
    client.load_extensions("cogs.join2create")
    client.run(SETTINGS.TOKEN)
