import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from datetime import timedelta

# ── CONFIG ─────────────────────────────────────────────────────────────────
GULAG_CHANNEL_NAME = "gulag"
TIMEOUT_SECONDS = 60

# Full tankie mode - anything remotely capitalist
BANNED_WORDS = [
    # Core capitalism
    "profit", "profits", "profitable", "capital", "capitalism", "capitalist",
    "capitalists", "market", "markets", "free market", "stock", "stocks",
    "shares", "shareholder", "shareholders", "dividend", "dividends",
    "invest", "investing", "investment", "investor", "investors",
    "entrepreneur", "entrepreneurship", "startup", "startups",

    # Ownership & property
    "landlord", "landlords", "landlady", "tenant", "rent", "renting",
    "property", "properties", "real estate", "mortgage", "loan", "loans",
    "debt", "debts", "interest rate", "bank", "banking", "banks",
    "own", "owned", "owner", "owners", "ownership", "private",
    "mine", "my property", "buy", "bought", "sell", "sold", "purchase",

    # Work & exploitation
    "boss", "bosses", "employer", "employers", "employee", "employees",
    "wage", "wages", "salary", "salaries", "hire", "hired", "firing",
    "fired", "layoff", "layoffs", "corporate", "corporation", "corporations",
    "company", "companies", "business", "businesses", "firm", "firms",
    "ceo", "cfo", "executive", "executives", "manager", "managers",
    "management", "supervisor", "supervisors",

    # Money & wealth
    "money", "cash", "rich", "wealthy", "wealth", "billionaire", "billionaires",
    "millionaire", "millionaires", "fortune", "fortunes", "luxur", "luxury",
    "expensive", "afford", "price", "prices", "cost", "costs", "fee", "fees",
    "tax", "taxes", "tariff", "tariffs",

    # Right-wing politics
    "conservative", "conservatives", "republican", "republicans", "tory",
    "tories", "libertarian", "libertarians", "neoliberal", "neoliberalism",
    "right wing", "right-wing", "far right", "fascist", "fascism", "nazi",
    "neocon", "neocons",

    # Consumerism
    "brand", "brands", "branded", "consumer", "consumers", "consumerism",
    "advertis", "advertising", "advertisement", "ads", "marketing",
    "product", "products", "commodity", "commodities",

    # Misc capitalist vibes
    "grind", "hustle", "hustling", "side hustle", "passive income",
    "nft", "crypto", "bitcoin", "blockchain", "web3",
    "meritocracy", "bootstraps", "self made",
]

# Gulag responses for public shaming
GULAG_MESSAGES = [
    "🚨 **CAPITALIST DETECTED** 🚨\n{mention} has been sent to the gulag for saying `{word}`!\nThe people demand re-education.",
    "⛏️ {mention} thought they could sneak some bourgeois language past the Commissar. They were wrong. Gulag time for saying `{word}`.",
    "🚩 The Party has detected counter-revolutionary speech from {mention} (`{word}`). They have been removed from the means of conversation for {timeout} seconds.",
    "📋 **CITIZEN REPORT FILED**\n{mention} said `{word}`, a known capitalist term. The Commissar has issued a {timeout} second sentence.",
    "🔴 BOURGEOIS ALERT: {mention} said `{word}`. This ideological deviation will not be tolerated. Timeout: {timeout} seconds. Glory to the revolution! ✊",
    "⚔️ The revolution does not tolerate `{word}`. {mention} has been escorted to the gulag for {timeout} seconds of mandatory dialectical materialism study.",
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
    # Ignore bots and DMs
    if message.author.bot:
        return
    if not message.guild:
        return

    # Ignore admins/mods (they can say what they want, comrade)
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    content_lower = message.content.lower()

    # Check for banned words
    found_word = None
    for word in BANNED_WORDS:
        if word in content_lower:
            found_word = word
            break

    if found_word:
        # Delete the capitalist propaganda
        try:
            await message.delete()
        except discord.Forbidden:
            pass

        # Timeout the counter-revolutionary
        try:
            await message.author.timeout(
                timedelta(seconds=TIMEOUT_SECONDS),
                reason=f"Counter-revolutionary speech: said '{found_word}'"
            )
        except discord.Forbidden:
            pass

        # Find or create the gulag channel
        gulag_channel = discord.utils.get(message.guild.channels, name=GULAG_CHANNEL_NAME)
        if gulag_channel is None:
            try:
                gulag_channel = await message.guild.create_text_channel(
                    GULAG_CHANNEL_NAME,
                    topic="🚨 Hall of shame for counter-revolutionary speech 🚨"
                )
            except discord.Forbidden:
                return

        # Post the shame message
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
    # Split into chunks so it fits in a message
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
