import sys

from ciri import BOT_TOKEN, OWNER_ID, bot, userbot
from ciri.utils import get_owner, load_modules

try:
    userbot.start()
    bot.start(bot_token=BOT_TOKEN)
except Exception:
    sys.exit(1)

load_modules()
print("Cirilla Userbot Is Alive")

userbot.loop.run_until_complete(get_owner())
print(OWNER_ID)
userbot.run_until_disconnected()
