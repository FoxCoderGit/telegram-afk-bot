import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your Telegram ID (only the owner can enable/disable AFK mode)
OWNER_ID = 123

# Global storage for AFK data
afk_data = {
    "enabled": False,        # AFK mode is enabled or not
    "reason": "",            # Reason for being away
    "start_time": 0.0,       # Time when AFK started (time.time())
    "notified_users": set()  # Set of user IDs who have already been auto-replied
}

async def afk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /afk {reason} command:
    Enables AFK mode for the owner, stores the reason and start time, and resets the notified users list.
    """
    if update.effective_user.id != OWNER_ID:
        return  # Ignore commands from non-owner users

    reason = " ".join(context.args) if context.args else "no reason"
    afk_data["enabled"] = True
    afk_data["reason"] = reason
    afk_data["start_time"] = time.time()
    afk_data["notified_users"].clear()  # Reset notified users
    if update.effective_message:
        await update.effective_message.reply_text(f"AFK mode is now enabled.\nReason: {reason}")

async def off_afk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /off_afk command:
    Disables AFK mode for the owner.
    """
    if update.effective_user.id != OWNER_ID:
        return

    if afk_data["enabled"]:
        afk_data["enabled"] = False
        if update.effective_message:
            await update.effective_message.reply_text("AFK mode is now disabled. Welcome back!")
    else:
        if update.effective_message:
            await update.effective_message.reply_text("AFK mode is not currently active.")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming private messages:
    If AFK mode is enabled and the message is from a user (not the owner) in a private chat
    who hasn't received an auto-reply yet, send an automated reply with the reason and AFK duration.
    """
    message = update.effective_message
    if message is None:
        return

    # Only handle private chats
    if update.effective_chat.type != 'private':
        return

    # Ignore messages from the owner
    if update.effective_user.id == OWNER_ID:
        return

    # If AFK mode is not enabled, do nothing
    if not afk_data["enabled"]:
        return

    # If the user has already been notified, do nothing
    if update.effective_user.id in afk_data["notified_users"]:
        return

    # Add user to the notified list
    afk_data["notified_users"].add(update.effective_user.id)
    elapsed = int(time.time() - afk_data["start_time"])
    reply_text = (
        f"I'm currently away: \"{afk_data['reason']}\"\n"
        f"AFK duration: {format_duration(elapsed)}."
    )
    await message.reply_text(reply_text)

def format_duration(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    # Replace "YOUR_BOT_TOKEN_HERE" with your token obtained from BotFather
    app = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()

    # Register command handlers
    app.add_handler(CommandHandler("afk", afk_command))
    app.add_handler(CommandHandler("off_afk", off_afk_command))
    # Register message handler for incoming text messages (non-commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    logging.info("Business bot started. Waiting for messages...")
    app.run_polling()

if __name__ == '__main__':
    main()