# 🚩 Commie SMP Bot

Sends capitalists to the gulag. Full tankie mode enabled.

## Setup

### Step 1 — Create the Discord Bot
1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it "Commissar" or whatever
3. Go to **Bot** tab → click **Add Bot**
4. Under **Privileged Gateway Intents** enable:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Click **Reset Token** → copy the token (keep it secret!)
6. Go to **OAuth2 → URL Generator**
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Moderate Members`, `Manage Messages`, `Send Messages`, `View Channels`, `Manage Channels`
7. Copy the generated URL → open it → add the bot to your server

### Step 2 — Deploy to Railway (free hosting)
1. Go to https://railway.app and sign up with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Upload this folder to a GitHub repo first, then connect it
4. In Railway, go to **Variables** and add:
   - `DISCORD_TOKEN` = your bot token from step 1
5. Railway will auto-detect Python and run the bot!

### Alternative: Deploy to Render (also free)
1. Go to https://render.com and sign up
2. New → **Web Service** → connect your GitHub repo
3. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
4. Add environment variable `DISCORD_TOKEN`

## Commands
- `/gulag @user reason` — manually send someone to the gulag
- `/freefromgulag @user` — release a re-educated comrade
- `/banned_words` — see the list of banned words
- `/glory` — glory to the revolution 🚩

## How it works
- Watches every message for capitalist language
- If detected: deletes the message, timeouts the user for 60 seconds,
  and posts a shame message in #gulag
- Admins are exempt (the Commissar trusts the Party leadership)
- Creates #gulag automatically if it doesn't exist
