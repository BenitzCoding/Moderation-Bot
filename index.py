import os
import json
import traceback

from discord import Intents
from discord.app_commands import AppCommand
from discord.ext.commands import Bot

from dotenv import load_dotenv, find_dotenv
from typing import Any, Coroutine, List

class BotInstance(Bot):
	def __init__(self):
		super().__init__(
			command_prefix = "!",
			intents = Intents.all(),
			description = "Your Concise & Easy to use Moderation Bot."
		)
		with open("config.json", "r") as config_file:
			self.constants = json.dump(config_file.read)

	async def sync_commands(self) -> Coroutine[Any, Any, List[AppCommand]]:
		return await self.tree.sync()

	async def setup_hook(self) -> None:
		try: [await self.load_extension(file[:-3]) for file in os.listdir("cogs") if file.endswith(".py")]
		except Exception as error: traceback.print_exc(error)
		await self.sync_commands()

	async def start(self, *args, **kwargs) -> Coroutine[Any, Any, None]:
		return await super().start(*args, **kwargs)

	async def close(self, *args, **kwargs) -> Coroutine[Any, Any, None]:
		return await super().close(*args, **kwargs)

bot = BotInstance()

@bot.listen("on_ready")
async def startup():
	print("Bot is Operational")

if __name__ == "__main__":
	load_dotenv(find_dotenv())
	bot.run(os.environ("TOKEN"))