import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from datetime import timedelta

# ── CONFIG ─────────────────────────────────────────────────────────────────
GULAG_CHANNEL_NAME = "gulag"
TIMEOUT_SECONDS = 60

BANNED_WORDS = [
    "profit", "profits", "profitable", "capital", "capitalism", "capitalist",
    "capitalists", "market", "markets", "free market", "stock", "stocks",
    "shares", "shareholder", "shareholders", "dividend", "dividends",
    "invest", "investing", "investment", "investor", "investors",
    "entrepreneur", "entrepreneurship", "startup", "startups",
    "landlord", "landlords", "landlady", "tenant", "rent", "renting",
    "property", "properties", "real estate", "mortgage", "loan", "loans",
    "debt", "debts", "interest rate", "bank", "banking", "banks",
    "own", "owned", "owner", "owners", "ownership", "private",
    "buy", "bought", "sell", "sold", "purchase",
    "boss", "bosses", "employer", "employers", "employee", "employees",
    "wage", "wages", "salary", "salaries", "hire", "hired", "firing",
    "fired", "layoff", "layoffs", "corporate", "corporation", "corporations",
    "company", "companies", "business", "businesses", "firm", "firms",
    "ceo", "cfo", "executive", "executives", "manager", "managers",
    "management", "supervisor", "supervisors",
    "money", "cash", "rich", "wealthy", "wealth", "billionaire", "billionaires",
    "millionaire", "millionaires", "fortune", "fortunes", "luxury",
    "expensive", "afford", "price", "prices", "cost", "costs", "fee", "fees",
    "tax", "taxes", "tariff", "tariffs",
    "conservative", "conservatives", "republican", "republicans", "tory",
    "tories", "libertarian", "libertarians", "neoliberal", "neoliberalism",
    "right wing", "right-wing", "far right", "fascist", "fascism", "nazi",
    "neocon", "neocons",
    "brand", "brands", "branded", "consumer", "consumers", "consumerism",
    "advertising", "advertisement", "ads", "marketing",
    "product", "products", "commodity", "commodities",
    "grind", "hustle", "hustling", "side hustle", "passive income",
    "nft", "crypto", "bitcoin", "blockchain", "web3",
    "meritocracy", "bootstraps", "self made",
]

COMMUNIST_PRAISE_WORDS = [
    "communism", "communist", "comrade", "comrades", "solidarity",
    "proletariat", "workers", "revolution", "revolutionary",
    "marxism", "marxist", "marx", "engels", "lenin", "leninist",
    "socialism", "socialist", "collective", "collectively",
    "means of production", "class struggle", "bourgeoisie",
    "vanguard", "dialectic", "materialism", "manifesto",
    "seize", "workers unite", "workers of the world",
    "glory to", "long live", "down with capitalism",
    "anti-capitalist", "anticapitalist", "leftist", "left wing",
    "anarchism", "anarchist", "mutual aid", "commune",
]

GULAG_MESSAGES = [
    "🚨 **CAPITALIST DETECTED** 🚨\n{mention} has been sent to the gulag for saying `{word}`!\nThe people demand re-education.",
    "⛏️ {mention} thought they could sneak some bourgeois language past the Commissar. They were wrong. Gulag time for saying `{word}`.",
    "🚩 The Party has detected counter-revolutionary speech from {mention} (`{word}`). They have been removed from the means of conversation for {timeout} seconds.",
    "📋 **CITIZEN REPORT FILED**\n{mention} said `{word}`, a known capitalist term. The Commissar has issued a {timeout} second sentence.",
    "🔴 BOURGEOIS ALERT: {mention} said `{word}`. This ideological deviation will not be tolerated. Timeout: {timeout} seconds. Glory to the revolution! ✊",
    "⚔️ The revolution does not tolerate `{word}`. {mention} has been escorted to the gulag for {timeout} seconds of mandatory dialectical materialism study.",
]

PRAISE_MESSAGES = [
    "✊ {mention} shows excellent class consciousness by mentioning `{word}`! The Party is pleased. 🚩",
    "🚩 AH YES! {mention} speaks the language of the revolution! `{word}` — a truly beautiful word. The Commissar approves!",
    "📖 {mention} has clearly studied their Marx! Mentioning `{word}` warms the Commissar's heart. Glory to the struggle! ✊",
    "🌹 The proletariat thanks {mention} for spreading the word of `{word}`! This is exactly the kind of revolutionary spirit we need!",
    "⭐ OUTSTANDING IDEOLOGICAL PURITY! {mention} said `{word}`. The Commissar awards you one (1) ration of extra bread. 🍞✊",
    "🔴 {mention} is a TRUE comrade! `{word}` — the Commissar shed a single tear of joy. The revolution is inevitable! 🚩",
    "✨ The Party recognizes {mention} for their correct usage of `{word}`. You are an example to all comrades! ✊🚩",
    "📣 ATTENTION ALL COMRADES: {mention} said `{word}` and has proven themselves a loyal servant of the revolution! 🌹",
]

# ── BOT SETUP ───────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🚩 Commissar Bot online as {bot.user}")
    print(f"   Monitoring {len(bot.guilds)} server(s)")
    try:
        synced = await bot.tree.sync()
        print(f"   Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"   Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.guild:
        return

    content_lower = message.content.lower()

    NEGATIVE_WORDS = [
        "hate", "hating", "hates", "against", "anti",
        "ban", "banned", "destroy", "kill", "bad", "worst",
        "stupid", "dumb", "gross", "eww", "ew", "yikes",
        "dont like", "don't like", "dislike", "disgusting",
        "terrible", "awful", "cringe", "trash", "garbage",
        "down with", "death to", "away with",
        "isnt good", "isn't good", "is bad", "is terrible",
        "is trash", "is stupid", "is dumb", "is awful",
        "is cringe", "is gross", "is worst", "not good",
        "not great", "not real", "doesn't work", "doesnt work",
        "will fail", "has failed", "never works", "sucks",
        "is fake", "is a lie", "is wrong",
    ]

    found_praise = None
    for word in COMMUNIST_PRAISE_WORDS:
        if word in content_lower:
            word_index = content_lower.find(word)
            # Check 40 chars before AND after the word
            context_before = content_lower[max(0, word_index - 40):word_index]
            context_after = content_lower[word_index:min(len(content_lower), word_index + 40)]
            is_negative = any(neg in context_before or neg in context_after for neg in NEGATIVE_WORDS)
            if not is_negative:
                found_praise = word
                break

    if found_praise:
        praise_msg = random.choice(PRAISE_MESSAGES).format(
            mention=message.author.mention,
            word=found_praise
        )
        await message.channel.send(praise_msg)
        await bot.process_commands(message)
        return  # Don't check banned words if they said something communist

    # Admins exempt from banned words
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    # Check for banned words
    found_word = None
    for word in BANNED_WORDS:
        if word in content_lower:
            found_word = word
            break

    if found_word:
        try:
            await message.delete()
        except discord.Forbidden:
            pass

        try:
            await message.author.timeout(
                timedelta(seconds=TIMEOUT_SECONDS),
                reason=f"Counter-revolutionary speech: said '{found_word}'"
            )
        except discord.Forbidden:
            pass

        gulag_channel = discord.utils.get(message.guild.channels, name=GULAG_CHANNEL_NAME)
        if gulag_channel is None:
            try:
                gulag_channel = await message.guild.create_text_channel(
                    GULAG_CHANNEL_NAME,
                    topic="🚨 Hall of shame for counter-revolutionary speech 🚨"
                )
            except discord.Forbidden:
                return

        shame_msg = random.choice(GULAG_MESSAGES).format(
            mention=message.author.mention,
            word=found_word,
            timeout=TIMEOUT_SECONDS
        )
        await gulag_channel.send(shame_msg)

    await bot.process_commands(message)


# ── SLASH COMMANDS ──────────────────────────────────────────────────────────

@bot.tree.command(name="gulag", description="Manually send a counter-revolutionary to the gulag")
@app_commands.describe(member="The bourgeois offender", reason="Their crime against the people")
@app_commands.checks.has_permissions(moderate_members=True)
async def gulag_command(interaction: discord.Interaction, member: discord.Member, reason: str = "counter-revolutionary behaviour"):
    try:
        await member.timeout(timedelta(seconds=TIMEOUT_SECONDS), reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to timeout that user.", ephemeral=True)
        return

    gulag_channel = discord.utils.get(interaction.guild.channels, name=GULAG_CHANNEL_NAME)
    if gulag_channel is None:
        gulag_channel = await interaction.guild.create_text_channel(GULAG_CHANNEL_NAME)

    await gulag_channel.send(
        f"⛏️ {member.mention} has been manually sent to the gulag by the Commissar for: *{reason}*\n"
        f"Sentence: {TIMEOUT_SECONDS} seconds of re-education. ✊"
    )
    await interaction.response.send_message(f"✅ {member.mention} has been sent to the gulag.", ephemeral=True)


@bot.tree.command(name="freefromgulag", description="Release a comrade who has been re-educated")
@app_commands.describe(member="The comrade to release")
@app_commands.checks.has_permissions(moderate_members=True)
async def free_command(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.timeout(None)
        await interaction.response.send_message(
            f"✅ {member.mention} has completed their re-education and is free to rejoin the revolution! ✊",
        )
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to do that.", ephemeral=True)


@bot.tree.command(name="banned_words", description="See the list of banned capitalist words")
async def banned_words_command(interaction: discord.Interaction):
    words = ", ".join(f"`{w}`" for w in BANNED_WORDS[:40])
    await interaction.response.send_message(
        f"🚩 **Banned Capitalist Terms (first 40):**\n{words}\n\n...and {len(BANNED_WORDS) - 40} more. Stay vigilant, comrade!",
        ephemeral=True
    )


@bot.tree.command(name="glory", description="Glory to the revolution!")
async def glory_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "✊🚩 **GLORY TO THE COMMIE SMP!** 🚩✊\n"
        "The workers own the means of production!\n"
        "The bourgeoisie shall not pass!"
    )


# ── RUN ─────────────────────────────────────────────────────────────────────
token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN environment variable not set!")

bot.run(token)
