# ---------------------------------------------------
# File Name: plans.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from datetime import timedelta
import pytz
import datetime, time
from devgagan import app
import asyncio
from config import OWNER_ID
from devgagan.core.func import get_seconds
from devgagan.core.mongo import plans_db  
from pyrogram import filters 



@app.on_message(filters.command("rem") & filters.user(OWNER_ID))
async def remove_premium(client, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("⛔ You are not authorized.")
        return
    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])
        except ValueError:
            await message.reply_text("⚠️ Invalid user ID. Usage: `/rem 123456789`")
            return
        try:
            user = await client.get_users(user_id)
        except Exception:
            user = None
        data = await plans_db.check_premium(user_id)
        if data and data.get("_id"):
            await plans_db.remove_premium(user_id)
            await message.reply_text(f"✅ Premium removed successfully for `{user_id}`!")
            if user:
                try:
                    await client.send_message(
                        chat_id=user_id,
                        text=f"Hey {user.mention},\n\nYour premium access has been removed.\nThank you for using our service 😊."
                    )
                except Exception:
                    pass
        else:
            await message.reply_text("⚠️ This user is not a premium user.")
    else:
        await message.reply_text("**Usage:** `/rem user_id`") 



@app.on_message(filters.command("myplan"))
async def myplan(client, message):
    user_id = message.from_user.id
    user = message.from_user.mention
    data = await plans_db.check_premium(user_id)  
    if data and data.get("expire_date"):
        expiry = data.get("expire_date")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
        
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        
        time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"
        await message.reply_text(f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n👤 ᴜꜱᴇʀ : {user}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"ʜᴇʏ {user},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs")
        


@app.on_message(filters.command("check") & filters.user(OWNER_ID))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        if data and data.get("expire_date"):
            expiry = data.get("expire_date") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}")
        else:
            await message.reply_text("ɴᴏ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ !")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /check user_id")


@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def give_premium_cmd_handler(client, message):
    if len(message.command) != 4:
        await message.reply_text(
            "**Usage:** `/add user_id amount unit`\n\n"
            "**Examples:**\n"
            "`/add 123456789 1 day`\n"
            "`/add 123456789 1 month`\n"
            "`/add 123456789 1 year`\n"
            "`/add 123456789 1 hour`\n"
            "`/add 123456789 30 min`"
        )
        return
    try:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y %I:%M:%S %p")
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        duration = message.command[2] + " " + message.command[3]
        seconds = await get_seconds(duration)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            await plans_db.add_premium(user_id, expiry_time)
            data = await plans_db.check_premium(user_id)
            expiry = data.get("expire_date")
            expiry_str = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")
            await message.reply_text(
                f"✅ **Premium Added Successfully!**\n\n"
                f"👤 **User:** {user.mention}\n"
                f"🆔 **User ID:** `{user_id}`\n"
                f"⏰ **Duration:** `{duration}`\n"
                f"📅 **Joined:** `{current_time}`\n"
                f"⌛ **Expires:** `{expiry_str}`\n\n"
                f"__⚡ Powered by @Mr_1X8__",
                disable_web_page_preview=True
            )
            try:
                await client.send_message(
                    chat_id=user_id,
                    text=(
                        f"👋 Hey {user.mention},\n"
                        f"Thank you for purchasing premium. Enjoy! ✨🎉\n\n"
                        f"⏰ **Duration:** `{duration}`\n"
                        f"📅 **Joined:** `{current_time}`\n"
                        f"⌛ **Expires:** `{expiry_str}`"
                    ),
                    disable_web_page_preview=True
                )
            except Exception:
                pass
        else:
            await message.reply_text(
                "⚠️ Invalid time format.\n\n"
                "Use: `1 day`, `1 hour`, `30 min`, `1 month`, `1 year`"
            )
    except ValueError:
        await message.reply_text("⚠️ Invalid user ID.")
    except Exception as e:
        await message.reply_text(f"❌ Error: `{e}`")


@app.on_message(filters.command("transfer"))
async def transfer_premium(client, message):
    if len(message.command) == 2:
        new_user_id = int(message.command[1])  # The user ID to whom premium is transferred
        sender_user_id = message.from_user.id  # The current premium user issuing the command
        sender_user = await client.get_users(sender_user_id)
        new_user = await client.get_users(new_user_id)
        
        # Fetch sender's premium plan details
        data = await plans_db.check_premium(sender_user_id)
        
        if data and data.get("_id"):  # Verify sender is already a premium user
            expiry = data.get("expire_date")  
            
            # Remove premium for the sender
            await plans_db.remove_premium(sender_user_id)
            
            # Add premium for the new user with the same expiry date
            await plans_db.add_premium(new_user_id, expiry)
            
            # Convert expiry date to IST format for display
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime(
                "%d-%m-%Y\n⏱️ **Expiry Time:** %I:%M:%S %p"
            )
            time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            current_time = time_zone.strftime("%d-%m-%Y\n⏱️ **Transfer Time:** %I:%M:%S %p")
            
            # Confirmation message to the sender
            await message.reply_text(
                f"✅ **Premium Plan Transferred Successfully!**\n\n"
                f"👤 **From:** {sender_user.mention}\n"
                f"👤 **To:** {new_user.mention}\n"
                f"⏳ **Expiry Date:** {expiry_str_in_ist}\n\n"
                f"__Powered by Team SPY__ 🚀"
            )
            
            # Notification to the new user
            await client.send_message(
                chat_id=new_user_id,
                text=(
                    f"👋 **Hey {new_user.mention},**\n\n"
                    f"🎉 **Your Premium Plan has been Transferred!**\n"
                    f"🛡️ **Transferred From:** {sender_user.mention}\n\n"
                    f"⏳ **Expiry Date:** {expiry_str_in_ist}\n"
                    f"📅 **Transferred On:** {current_time}\n\n"
                    f"__Enjoy the Service!__ ✨"
                )
            )
        else:
            await message.reply_text("⚠️ **You are not a Premium user!**\n\nOnly Premium users can transfer their plans.")
    else:
        await message.reply_text("⚠️ **Usage:** /transfer user_id\n\nReplace `user_id` with the new user's ID.")


async def premium_remover():
    all_users = await plans_db.premium_users()
    removed_users = []
    not_removed_users = []

    for user_id in all_users:
        try:
            user = await app.get_users(user_id)
            chk_time = await plans_db.check_premium(user_id)

            if chk_time and chk_time.get("expire_date"):
                expiry_date = chk_time["expire_date"]

                if expiry_date <= datetime.datetime.now():
                    name = user.first_name
                    await plans_db.remove_premium(user_id)
                    await app.send_message(user_id, text=f"Hello {name}, your premium subscription has expired.")
                    print(f"{name}, your premium subscription has expired.")
                    removed_users.append(f"{name} ({user_id})")
                else:
                    name = user.first_name
                    current_time = datetime.datetime.now()
                    time_left = expiry_date - current_time

                    days = time_left.days
                    hours, remainder = divmod(time_left.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    if days > 0:
                        remaining_time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                    elif hours > 0:
                        remaining_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
                    elif minutes > 0:
                        remaining_time = f"{minutes} minutes, {seconds} seconds"
                    else:
                        remaining_time = f"{seconds} seconds"

                    print(f"{name} : Remaining Time : {remaining_time}")
                    not_removed_users.append(f"{name} ({user_id})")
        except:
            await plans_db.remove_premium(user_id)
            print(f"Unknown users captured : {user_id} removed")
            removed_users.append(f"Unknown ({user_id})")

    return removed_users, not_removed_users


@app.on_message(filters.command("freez") & filters.user(OWNER_ID))
async def refresh_users(_, message):
    removed_users, not_removed_users = await premium_remover()
    removed_text = "\n".join(removed_users) if removed_users else "No users removed."
    not_removed_text = "\n".join(not_removed_users) if not_removed_users else "No users remaining with premium."
    summary = (
        f"**Here is Summary...**\n\n"
        f"> **Removed Users:**\n{removed_text}\n\n"
        f"> **Not Removed Users:**\n{not_removed_text}"
    )
    await message.reply(summary)


@app.on_message(filters.command("get") & filters.user(OWNER_ID))
async def get_all_users(client, message):
    from devgagan.core.mongo.users_db import get_users
    users = await get_users()
    premium = await plans_db.premium_users()

    total = len(users)
    prem_count = len(premium)

    text = (
        f"╔══════════════════════╗\n"
        f"║  📊 **BOT DATABASE**  ║\n"
        f"╚══════════════════════╝\n\n"
        f"👥 **Total Users:** `{total}`\n"
        f"💎 **Premium Users:** `{prem_count}`\n"
        f"🆓 **Free Users:** `{total - prem_count}`\n\n"
    )

    if premium:
        text += "**💎 Premium User IDs:**\n"
        text += "\n".join([f"• `{uid}`" for uid in premium])
    else:
        text += "**💎 Premium Users:** None"

    # Split if too long
    if len(text) > 4000:
        await message.reply(text[:4000] + "\n\n_...truncated_")
    else:
        await message.reply(text)
    
