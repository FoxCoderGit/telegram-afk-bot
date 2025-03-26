# Telegram AFK Bot

**Telegram AFK Bot** is a lightweight and reliable Telegram bot that allows the bot owner to enable an AFK (Away From Keyboard) status with an optional reason. While AFK mode is active, the bot automatically replies to private messages with the reason and the duration since the AFK status was activated.

## Features

- `/afk [reason]` — Enables AFK mode with an optional reason.
- `/off_afk` — Disables AFK mode.
- Sends auto-replies **only once per user** while AFK.
- Includes the AFK reason and elapsed time in replies.
- Minimal and easy to configure.

## Requirements

- Python 3.9 or higher
- `python-telegram-bot==20.0`
- A **Telegram Business Bot** (Business connection enabled)
- A **Telegram Premium account** (required to receive messages from strangers in private chats)

## Installation

```bash
git clone https://github.com/FoxCoderGit/telegram-afk-bot.git
cd telegram-afk-bot
pip install -r requirements.txt
```

## Usage

1. Open `afk_bot.py`
2. Replace `OWNER_ID` with your own Telegram user ID.
3. Replace `YOUR_BOT_TOKEN_HERE` with the bot token from [BotFather](https://t.me/BotFather).
4. Make sure your bot is **connected as a business bot** and you are using **Telegram Premium**.
5. Run the bot:

```bash
python afk_bot.py
```

The bot will automatically reply to private messages while you’re AFK, and stop when you disable it.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
