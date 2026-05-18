from pyrogram import Client, filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
from devgagan.core.func import *
from pyrogram.types import BotCommand, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


CONTACT_URL = "https://t.me/Mr_1X8?text=Hi%2C+I+want+to+get+Premium"


@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🎲 Get 3 hours free access"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("freez", "🧊 Remove all expired user"),
        BotCommand("pay", "₹ Pay now to get subscription"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("session", "🧵 Generate Pyrogramv2 session"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("gcast", "⚡ Broadcast message to bot users"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ])

    await message.reply("✅ Commands configured successfully!")


help_pages = [
    (
        "╔══════════════════════╗\n"
        "║  📖 **HELP GUIDE (1/2)**  ║\n"
        "╚══════════════════════╝\n\n"
        "1. **/add userID**\n"
        "> ➕ Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n"
        "> ➖ Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n"
        "> 💘 Transfer premium to another user\n\n"
        "4. **/get**\n"
        "> 📋 Get all user IDs (Owner only)\n\n"
        "5. **/lock**\n"
        "> 🔒 Lock channel from extraction (Owner only)\n\n"
        "6. **/dl link**\n"
        "> 💀 Download videos from 30+ sites\n\n"
        "7. **/adl link**\n"
        "> 👻 Download audio from 30+ sites\n\n"
        "8. **/login**\n"
        "> 🔑 Login for private channel access\n\n"
        "9. **/batch**\n"
        "> 📦 Bulk extraction for posts (After login)\n\n"
        "__⚡ Powered by @Mr_1X8__"
    ),
    (
        "╔══════════════════════╗\n"
        "║  📖 **HELP GUIDE (2/2)**  ║\n"
        "╚══════════════════════╝\n\n"
        "10. **/logout**\n"
        "> 🚪 Logout from the bot\n\n"
        "11. **/stats**\n"
        "> 📊 Get bot stats\n\n"
        "12. **/plan**\n"
        "> 🗓️ Check premium plans\n\n"
        "13. **/speedtest**\n"
        "> 🚅 Test the server speed\n\n"
        "14. **/terms**\n"
        "> 📜 Terms and conditions\n\n"
        "15. **/cancel**\n"
        "> 🚫 Cancel ongoing batch process\n\n"
        "16. **/myplan**\n"
        "> ⌛ Get details about your plan\n\n"
        "17. **/session**\n"
        "> 🧵 Generate Pyrogram V2 session\n\n"
        "18. **/settings**\n"
        "> ⚙️ SETCHATID, SETRENAME, CAPTION,\n"
        "> REPLACEWORDS, RESET and more\n\n"
        "__⚡ Powered by @Mr_1X8__"
    )
]


async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return

    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")

    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)

    keyboard = InlineKeyboardMarkup([buttons])

    await message.delete()
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )


@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
    await send_or_edit_help_page(client, message, 0)


@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])

    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    await send_or_edit_help_page(client, callback_query.message, page_number)
    await callback_query.answer()


@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "╔══════════════════════╗\n"
        "║  📜 **TERMS OF USE**  ║\n"
        "╚══════════════════════╝\n\n"
        "✨ We are not responsible for user deeds and do not promote copyrighted content.\n\n"
        "✨ Upon purchase, we do not guarantee uptime, downtime, or plan validity. "
        "__Authorization and banning of users are at our discretion.__\n\n"
        "✨ Payment **__does not guarantee__** authorization for /batch. "
        "All decisions are made at our discretion.\n\n"
        "__⚡ Powered by @Mr_1X8__"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
        [InlineKeyboardButton("💬 Contact Now", url=CONTACT_URL)],
    ])
    await message.reply_text(terms_text, reply_markup=buttons)


@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "╔══════════════════════╗\n"
        "║  💎 **PREMIUM PLANS**  ║\n"
        "╚══════════════════════╝\n\n"
        "💰 **Price:** Starting from $2 or ₹200\n"
        "   ↳ Accepted via **Amazon Gift Card**\n\n"
        "📥 **Download Limit:** Up to 1,00,000 files per batch\n\n"
        "🛑 **Batch Modes:** /batch and /bulk\n"
        "   ↳ Wait for process to complete before starting new\n\n"
        "📜 Send /terms for full terms and conditions\n\n"
        "__⚡ Powered by @Mr_1X8__"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
        [InlineKeyboardButton("💬 Contact Now", url=CONTACT_URL)],
    ])
    await message.reply_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "╔══════════════════════╗\n"
        "║  💎 **PREMIUM PLANS**  ║\n"
        "╚══════════════════════╝\n\n"
        "💰 **Price:** Starting from $2 or ₹200\n"
        "   ↳ Accepted via **Amazon Gift Card**\n\n"
        "📥 **Download Limit:** Up to 1,00,000 files per batch\n\n"
        "🛑 **Batch Modes:** /batch and /bulk\n"
        "   ↳ Wait for process to complete before starting new\n\n"
        "📜 Click See Terms below for full terms\n\n"
        "__⚡ Powered by @Mr_1X8__"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
        [InlineKeyboardButton("💬 Contact Now", url=CONTACT_URL)],
    ])
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "╔══════════════════════╗\n"
        "║  📜 **TERMS OF USE**  ║\n"
        "╚══════════════════════╝\n\n"
        "✨ We are not responsible for user deeds and do not promote copyrighted content.\n\n"
        "✨ Upon purchase, we do not guarantee uptime, downtime, or plan validity. "
        "__Authorization and banning of users are at our discretion.__\n\n"
        "✨ Payment **__does not guarantee__** authorization for /batch. "
        "All decisions are made at our discretion.\n\n"
        "__⚡ Powered by @Mr_1X8__"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
        [InlineKeyboardButton("💬 Contact Now", url=CONTACT_URL)],
    ])
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
