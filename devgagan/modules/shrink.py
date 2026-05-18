from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP


tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]


async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)


Param = {}


async def generate_random_param(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None


async def is_user_verified(user_id):
    session = await token.find_one({"user_id": user_id})
    return session is not None


@app.on_message(filters.command("start"))
async def token_handler(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
    user_id = message.chat.id
    if len(message.command) <= 1:
        first_name = message.from_user.first_name or "User"
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("💎 Get Premium", url="https://t.me/Mr_1X8?text=Hi%2C+I+want+to+get+Premium"),
                InlineKeyboardButton("📋 Plans", callback_data="see_plan")
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="help_next_0")
            ],
            [
                InlineKeyboardButton("👨‍💻 Developed by @Mr_1X8", url="https://t.me/Mr_1X8")
            ]
        ])
        text = (
            f"╔══════════════════════╗\n"
            f"║   ⚡ **SAVE BOT** ⚡   ║\n"
            f"╚══════════════════════╝\n\n"
            f"👋 **Hey {first_name}, Welcome!**\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 **What I Can Do:**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📥 **Save Restricted Content**\n"
            f"  ↳ Posts from channels with forwarding off\n\n"
            f"🔒 **Private Channel Access**\n"
            f"  ↳ Login with your account via /login\n\n"
            f"📦 **Bulk Download**\n"
            f"  ↳ Save hundreds of posts at once via /batch\n\n"
            f"🎬 **Media Downloader**\n"
            f"  ↳ YouTube, Instagram & 30+ platforms via /dl\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 **Quick Start:**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Just send any **Telegram post link**\n"
            f"2️⃣ For private channels → /login first\n"
            f"3️⃣ For bulk saving → /batch\n"
            f"4️⃣ Free users → /token for 3hr access\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"__⚡ Powered by @Mr_1X8__"
        )
        await message.reply_text(text, reply_markup=keyboard)
        return

    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user, no need of token 😉")
        return

    if param:
        if user_id in Param and Param[user_id] == param:
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=1),
            })
            del Param[user_id]
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return


@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user, no need of token 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active, enjoy!")
    else:
        param = await generate_random_param()
        Param[user_id] = param

        deep_link = f"https://t.me/{client.me.username}?start={param}"

        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔑 Verify Token Now", url=shortened_url)]]
        )
        await message.reply(
            "**Click the button below to verify your free access token:**\n\n"
            "> **What you get:**\n"
            "> 1. No time limit for 3 hours\n"
            "> 2. Batch limit: FreeLimit + 20\n"
            "> 3. All functions unlocked",
            reply_markup=button
        )
