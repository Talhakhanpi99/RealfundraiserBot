import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
import os
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Load donor data
if os.path.exists("leaderboard.json"):
    with open("leaderboard.json", "r") as f:
        leaderboard = json.load(f)
else:
    leaderboard = {}

# /start handler
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply(
        "👋 Welcome to the Crypto Duel Fundraiser!\n\n"
        "Donate to support development of the upcoming Crypto Duel bot.\n"
        "📸 After donating, send a screenshot here.\n\n"
        "Top 10 donors will get early access, rewards & perks!\n\n"
        "Use /donate to see instructions.\n"
    )

# /donate instructions
@dp.message_handler(commands=["donate"])
async def donate_handler(message: types.Message):
    await message.reply(
        "💸 Send crypto to: `your-crypto-address-here`\n"
        "After payment, post a screenshot in this chat.\n"
        "We'll verify and add you to the leaderboard!\n\n"
        "🏆 Use /leaderboard to see the top donors.",
        parse_mode=ParseMode.MARKDOWN
    )

# Handle screenshot uploads
@dp.message_handler(content_types=["photo"])
async def handle_donation_screenshot(message: types.Message):
    username = message.from_user.username or f"id_{message.from_user.id}"
    leaderboard[username] = leaderboard.get(username, 0) + 1  # Replace with real value later
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)
    await message.reply("✅ Screenshot received! Admin will verify and update your donation amount.")

# /leaderboard command
@dp.message_handler(commands=["leaderboard"])
async def leaderboard_handler(message: types.Message):
    if not leaderboard:
        await message.reply("No donations yet.")
        return
    top = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:10]
    leaderboard_msg = "\n".join([f"{i+1}. @{user} — ${amount}" for i, (user, amount) in enumerate(top)])
    await message.reply(f"🏆 *Top Donors:*\n\n{leaderboard_msg}", parse_mode=ParseMode.MARKDOWN)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
