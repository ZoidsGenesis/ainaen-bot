import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
# ✅ SLASH COMMAND: /nn (help only)
@bot.tree.command(name="nn", description="show help menu for !nn commands")
async def nn_help(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**🧠 cruel the best guild – command list:**\n"
        "- `!nn enh for <class name>` – enhancement builds\n"
        "- `!nn resetlist` – shows daily and weekly main todo list.\n"
        "- `!nn potionguide` – shows basic potions guide.\n"
        "- `!nn cruel` – dont prompt it. only for softies.\n"
        "`Got suggestions? Ping <@1052580900497534999> anytime!`",
        ephemeral=True
    )

# 🔄 Sync slash command
@bot.event
async def on_ready():
    print(f"✅ logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ slash command sync failed: {e}")
    bot.loop.create_task(daily_reset_task())

enhancements = {
    "abyssal angel": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Valiance, Acheron",
        "helm": "Examen",
        "cape": "Lament"
    },
    "abyssal angel's shadow": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Valiance, Acheron",
        "helm": "Examen",
        "cape": "Lament"
    },
    "alpha doomega": {
        "purpose": "Stun PvP",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "alpha omega": {
        "purpose": "Stun PvP",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "alpha pirate": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Ravenous",
        "helm": "Vim",
        "cape": "Lament"
    },
    "pirate": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Ravenous",
        "helm": "Vim",
        "cape": "Lament"
    },
    "antique hunter": {
        "purpose": "All-Rounder DPS, Anti-Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Elysium",
        "helm": "Vim, Pneuma",
        "cape": "Vainglory"
    },
    "artifact hunter": {
        "purpose": "All-Rounder DPS, Anti-Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Elysium",
        "helm": "Vim, Pneuma",
        "cape": "Vainglory"
    },
    "arachnomancer": {
        "purpose": "Bossfighter (Dodge), Hybrid Support (Debuffs)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "archfiend": {
        "purpose": "Farming, Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Lacerate, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "legendary archfiend": {
        "purpose": "Farming, Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Lacerate, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "archpaladin": {
        "purpose": "Defensive Tank, Hybrid Support (Debuffs/Heals)",
        "class": "Luck",
        "weapon": "Awe Blast, Valiance",
        "helm": "Forge",
        "cape": "Vainglory, Lament"
    },
    "assassin": {
        "purpose": "Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "ninja": {
        "purpose": "Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "ninja warrior": {
        "purpose": "Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "barber": {
        "purpose": "Soloer (DPS), Support (Buffs)",
        "class": "Luck",
        "weapon": "Dauntless, Arcana's Concerto",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "bard": {
        "purpose": "Support (Buffs/Heals)",
        "class": "Luck",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Forge",
        "cape": "Absolution"
    },
    "troubadour of love": {
        "purpose": "Support (Buffs/Heals)",
        "class": "Luck",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Forge",
        "cape": "Absolution"
    },
    "beast warrior": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "pumpkin lord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "warlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "beastmaster": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Smite, Ravenous",
        "helm": "Anima",
        "cape": "Lament"
    },
    "berserker": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "beta berserker": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "chaos avenger member preview": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "blademaster": {
        "purpose": "All-Rounder DPS, Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Praxis",
        "helm": "Vim",
        "cape": "Lament"
    },
    "swordmaster": {
        "purpose": "All-Rounder DPS, Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Praxis",
        "helm": "Vim",
        "cape": "Lament"
    },
    "blademaster assassin": {
        "purpose": "Farming, Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Praxis",
        "helm": "Vim",
        "cape": "Lament"
    },
    "swordmaster assassin": {
        "purpose": "Farming, Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Praxis",
        "helm": "Vim",
        "cape": "Lament"
    },
    "blood ancient": {
        "purpose": "Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "cardclasher": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "chaos avenger": {
        "purpose": "Offensive Tank, Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory, Avarice"
    },
    "chaos champion prime": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Elysium",
        "helm": "Anima",
        "cape": "Vainglory, Avarice"
    },
    "any chaos slayer class": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Elysium",
        "helm": "Anima",
        "cape": "Vainglory, Avarice"
    },
    "dark chaos berserker": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Elysium",
        "helm": "Anima",
        "cape": "Vainglory, Avarice"
    },
    "chaos shaper": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Lament"
    },
    "chrono assassin": {
        "purpose": "All-Rounder DPS, Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Arcana's Concerto",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "chrono chaorruptor": {
        "purpose": "All-Rounder DPS, Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Smite",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "chronocorrupter": {
        "purpose": "All-Rounder DPS, Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Smite",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "chronocommander": {
        "purpose": "Offensive Tank, Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "chrono commandant": {
        "purpose": "Offensive Tank, Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "chronomancer": {
        "purpose": "All-Rounder DPS, Bossfighter (Glass Cannon)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "chronomancer prime": {
        "purpose": "All-Rounder DPS, Bossfighter (Glass Cannon)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "chrono shadowhunter": {
        "purpose": "Soloer (DPS), Hybrid Support (Debuffs)",
        "class": "Luck",
        "weapon": "Ravenous, Arcana's Concerto",
        "helm": "Vim",
        "cape": "Lament"
    },
    "chrono shadowslayer": {
        "purpose": "Soloer (DPS), Hybrid Support (Debuffs)",
        "class": "Luck",
        "weapon": "Ravenous, Arcana's Concerto",
        "helm": "Vim",
        "cape": "Lament"
    },
    "chunin": {
        "purpose": "Farming, Hybrid Support (Debuffs)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "imperial chunin": {
        "purpose": "Farming, Hybrid Support (Debuffs)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "classic alpha pirate": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "classic barber": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "classic pirate": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "rogue": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "rogue (rare)": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "classic defender": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "classic doomknight": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory, Avarice"
    },
    "classic dragonlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "classic exalted soul cleaver": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "classic soul cleaver": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "classic guardian": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "classic legion doomknight": {
        "purpose": "Bossfighter (Anti-Decay), Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Forge, Anima",
        "cape": "Lament"
    },
    "classic ninja": {
        "purpose": "Soloer (Stun), Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "classic paladin": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "clawsuit": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "continuum chronomancer": {
        "purpose": "Hybrid Support (Buffs/Nukes)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "quantum chronomancer": {
        "purpose": "Hybrid Support (Buffs/Nukes)",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "corrupted chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Lacerate",
        "helm": "Forge",
        "cape": "Penitence"
    },
    "overworld chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Lacerate",
        "helm": "Forge",
        "cape": "Penitence"
    },
    "timeless chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Lacerate",
        "helm": "Forge",
        "cape": "Penitence"
    },
    "underworld chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Lacerate",
        "helm": "Forge",
        "cape": "Penitence"
    },
    "dark harbinger": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory, Lament"
    },
    "exalted harbinger": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory, Lament"
    },
    "exalted soul cleaver": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory, Lament"
    },
    "soul cleaver": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory, Lament"
    },
    "dark legendary hero": {
        "purpose": "Support (Heals)",
        "class": "Luck",
        "weapon": "Ravenous, Arcana's Concerto",
        "helm": "Forge",
        "cape": "Absolution, Vainglory"
    },
    "legendary hero": {
        "purpose": "Support (Heals)",
        "class": "Luck",
        "weapon": "Ravenous, Arcana's Concerto",
        "helm": "Forge",
        "cape": "Absolution, Vainglory"
    },
    "dark metal necro": {
        "purpose": "Offensive Tank",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory, Penitence"
    },
    "doom metal necro": {
        "purpose": "Offensive Tank",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory, Penitence"
    },
    "heavy metal necro": {
        "purpose": "Offensive Tank",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory, Penitence"
    },
    "heavy metal rockstar": {
        "purpose": "Offensive Tank",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory, Penitence"
    },
    "shadow ripper": {
        "purpose": "Offensive Tank",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory, Penitence"
    },
    "unchained rockstar": {
        "purpose": "Offensive Tank",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory, Penitence"
    },
    "deathknight lord": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Health Vamp",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "defender": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "doomknight": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "doomknight overlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "dragonlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Lament, Vainglory"
    },
    "dragon shinobi": {
        "purpose": "Soloer (DoT)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "dragonsoul shinobi": {
        "purpose": "Soloer (DoT)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "shadow dragon shinobi": {
        "purpose": "Soloer (DoT)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "dragonslayer": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "dragonslayer general": {
        "purpose": "Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Ravenous",
        "helm": "Vim, Anima",
        "cape": "Vainglory"
    },
    "shadowflame dragonlord": {
        "purpose": "Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Ravenous",
        "helm": "Vim, Anima",
        "cape": "Vainglory"
    },
    "drakel warlord": {
        "purpose": "Defensive Tank, Soloer (DPS), Anti-Physical PvP",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "empyrean chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Valiance, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "eternal chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Valiance, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "immortal chronomancer": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Luck",
        "weapon": "Valiance, Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "enchanted vampire lord": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Valiance, Elysium",
        "helm": "Forge",
        "cape": "Avarice, Lament"
    },
    "royal vampire lord": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Valiance, Elysium",
        "helm": "Forge",
        "cape": "Avarice, Lament"
    },
    "vampire": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Valiance, Elysium",
        "helm": "Forge",
        "cape": "Avarice, Lament"
    },
    "vampire lord": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Valiance, Elysium",
        "helm": "Forge",
        "cape": "Avarice, Lament"
    },
    "enforcer": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "protosartorium": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "rustbucket": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "eternal inversionist": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "evolved clawsuit": {
        "purpose": "Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "prismatic clawsuit": {
        "purpose": "Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "evolved leprechaun": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "evolved pumpkin lord": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "flame dragon warrior": {
        "purpose": "Farming, Bossfighter (DoT)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Avarice, Vainglory"
    },
    "glacial berserker": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "glacial warlord": {
        "purpose": "Soloer (DPS), DPS Support (Debuffs)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "glaceran warlord": {
        "purpose": "Soloer (DPS), DPS Support (Debuffs)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "savage glaceran warlord": {
        "purpose": "Soloer (DPS), DPS Support (Debuffs)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "great thief": {
        "purpose": "Bossfighter (DPS), Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "grunge rocker": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Forge",
        "cape": "Lament"
    },
    "neo metal necro": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Forge",
        "cape": "Lament"
    },
    "nu metal necro": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Forge",
        "cape": "Lament"
    },
    "shadow rocker": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Forge",
        "cape": "Lament"
    },
    "unchained rocker": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Forge",
        "cape": "Lament"
    },
    "guardian": {
        "purpose": "Hybrid Support (Buffs)",
        "class": "Luck",
        "weapon": "Ravenous, Valiance",
        "helm": "Vim",
        "cape": "Penitence"
    },
    "heroic naval commander": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "legendary naval commander": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "naval commander": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "hobo highlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "no class": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "obsidian no class": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "horc evader": {
        "purpose": "Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Elysium",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "legendary elemental warrior": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "ultra elemental warrior": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "legion blademaster assassin": {
        "purpose": "Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Praxis",
        "helm": "Vim",
        "cape": "Lament"
    },
    "legion swordmaster assassin": {
        "purpose": "Dodge PvP",
        "class": "Luck",
        "weapon": "Dauntless, Praxis",
        "helm": "Vim",
        "cape": "Lament"
    },
    "legion doomknight": {
        "purpose": "Bossfighter (Anti-Decay), Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Forge, Anima",
        "cape": "Lament"
    },
    "glacial berserker test": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "legion doomknight tester": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "legion paladin member trial": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "legion revenant member test": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "warrior": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "warrior (rare)": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "warriorscythe general": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "void highlord tester": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "leprechaun": {
        "purpose": "Soloer (Nuke), Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "lord of order": {
        "purpose": "Support (Buffs/Heals)",
        "class": "Luck",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Forge",
        "cape": "Absolution"
    },
    "lycan": {
        "purpose": "Stun PvP",
        "class": "Luck",
        "weapon": "Smite",
        "helm": "Forge",
        "cape": "Lament"
    },
    "master martial artist": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Lament"
    },
    "martial artist": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Lament"
    },
    "master ranger": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Elysium, Valiance",
        "helm": "Anima",
        "cape": "Vainglory, Avarice"
    },
    "ranger": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Elysium, Valiance",
        "helm": "Anima",
        "cape": "Vainglory, Avarice"
    },
    "mechajouster": {
        "purpose": "Hybrid Support (Debuffs), Stun PvP",
        "class": "Luck",
        "weapon": "Ravenous, Dauntless",
        "helm": "Forge",
        "cape": "Lament"
    },
    "nechronomancer": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Arcana's Concerto, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "necrotic chronomancer": {
        "purpose": "Farming",
        "class": "Luck",
        "weapon": "Arcana's Concerto, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "not a mod": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "paladin": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "silver paladin": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "paladin highlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Elysium",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "paladinslayer": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Elysium",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "renegade": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "sentinel": {
        "purpose": "Soloer (DPS), Anti-Dodge PvP",
        "class": "Luck",
        "weapon": "Ravenous",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "shadowscythe general": {
        "purpose": "Defensive Tank, Stun PvP",
        "class": "Luck",
        "weapon": "Smite",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "shadowstalker of time": {
        "purpose": "Soloer (Nuke), Soloer (Dodge), Bossfighter (DoT)",
        "class": "Luck",
        "weapon": "Dauntless, Smite",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "shadowwalker of time": {
        "purpose": "Soloer (Nuke), Soloer (Dodge), Bossfighter (DoT)",
        "class": "Luck",
        "weapon": "Dauntless, Smite",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "shadowweaver of time": {
        "purpose": "Soloer (Nuke), Soloer (Dodge), Bossfighter (DoT)",
        "class": "Luck",
        "weapon": "Dauntless, Smite",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "skycharged grenadier": {
        "purpose": "Stun PvP",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "skyguard grenadier": {
        "purpose": "Stun PvP",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "sovereign of storms": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "2 dps soloer)": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "star captain": {
        "purpose": "Soloer (DPS)",
        "class": "Luck",
        "weapon": "Valiance, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "starlord": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Dauntless",
        "helm": "Vim",
        "cape": "Lament"
    },
    "thief of hours": {
        "purpose": "All-Rounder DPS, Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Vim",
        "cape": "Vainglory"
    },
    "timekeeper": {
        "purpose": "Bossfighter (Nuke), Bossfighter (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless, Lacerate",
        "helm": "Vim",
        "cape": "Lament"
    },
    "timekiller": {
        "purpose": "Bossfighter (Nuke), Bossfighter (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless, Lacerate",
        "helm": "Vim",
        "cape": "Lament"
    },
    "undead goat": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Valiance",
        "helm": "Forge",
        "cape": "Vainglory"
    },
    "undead leprechaun": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Vim",
        "cape": "Lament"
    },
    "unlucky leprechaun": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Luck",
        "weapon": "Lacerate",
        "helm": "Vim",
        "cape": "Lament"
    },
    "undeadslayer": {
        "purpose": "Farming, Soloer (Nuke)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Vim",
        "cape": "Lament"
    },
    "verus doomknight": {
        "purpose": "Defensive Tank, DPS Support (Debuffs)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "void highlord": {
        "purpose": "Soloer (DPS), Bossfighter (DPS)",
        "class": "Luck",
        "weapon": "Smite, Dauntless",
        "helm": "Anima",
        "cape": "Vainglory"
    },
    "yami no ronin": {
        "purpose": "Soloer (Nuke), Soloer (Dodge)",
        "class": "Luck",
        "weapon": "Dauntless, Valiance",
        "helm": "Anima, Vim",
        "cape": "Vainglory"
    },
    "zaina": {
        "purpose": "Soloer",
        "class": "Gay",
        "weapon": "Gay",
        "helm": "Gay",
        "cape": "Gay"
    },
    "arcana invoker": {
        "purpose": "Generalist, Offensive Tank",
        "class": "Wizard",
        "weapon": "Ravenous, Valiance, Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Lament"
    },
    "arcane dark caster": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "mystical dark caster": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "timeless dark caster": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "archmage": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance (Astral), Acheron (Corporeal), Elysium (Corporeal)",
        "helm": "Pneuma",
        "cape": "Vainglory (Astral),Penitence (Corporeal), Avarice"
    },
    "battlemage": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Examen, Pneuma",
        "cape": "Lament, Vainglory"
    },
    "battlemage of love": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Examen, Pneuma",
        "cape": "Lament, Vainglory"
    },
    "dark battlemage": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Examen, Pneuma",
        "cape": "Lament, Vainglory"
    },
    "royal battlemage": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Examen, Pneuma",
        "cape": "Lament, Vainglory"
    },
    "blaze binder": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Avarice"
    },
    "firelord summoner": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Avarice"
    },
    "blood sorceress": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Avarice, Lament"
    },
    "chrono dataknight": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Pneuma",
        "cape": "Lament, Vainglory"
    },
    "chrono dragonknight": {
        "purpose": "Bossfighter (Nuke)",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Pneuma",
        "cape": "Lament, Vainglory"
    },
    "cryomancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "dark cryomancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "sakura cryomancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "daimon": {
        "purpose": "Farming, Support (Buffs/Heals)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Examen",
        "cape": "Vainglory, Avarice"
    },
    "dark caster": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "immortal dark caster": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "dark lord": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Penitence, Vainglory"
    },
    "darkside": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Penitence, Vainglory"
    },
    "dark master of moglins": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Avarice"
    },
    "master of moglins": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Avarice"
    },
    "dark ultra omniknight": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Penitence"
    },
    "ultra omniknight": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory, Penitence"
    },
    "darkblood stormking": {
        "purpose": "Farming, Soloer (Nuke)",
        "class": "Wizard",
        "weapon": "Dauntless",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "dragon knight": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "dragon of time": {
        "purpose": "Farming, Bossfighter (DoT)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma, Wizard",
        "cape": "Vainglory"
    },
    "2 to save inventory space)": {
        "purpose": "Farming, Bossfighter (DoT)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma, Wizard",
        "cape": "Vainglory"
    },
    "elemental dracomancer": {
        "purpose": "Defensive Tank",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "love caster": {
        "purpose": "Defensive Tank",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "evolved dark caster": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "infinite dark caster": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "infinite legion dark caster": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "legion evolved dark caster": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "evolved shaman": {
        "purpose": "Anti-Dodge PvP",
        "class": "Wizard",
        "weapon": "Mana Vamp",
        "helm": "Pneuma",
        "cape": "Absolution, Vainglory"
    },
    "frost spiritreaver": {
        "purpose": "Stun PvP",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "grim necromancer": {
        "purpose": "Offensive Tank",
        "class": "Wizard",
        "weapon": "Ravenous, Valiance",
        "helm": "Pneuma",
        "cape": "Penitence"
    },
    "highseas commander": {
        "purpose": "All-Rounder DPS, Soloer (Dodge)",
        "class": "Wizard",
        "weapon": "Valiance, Lacerate",
        "helm": "Examen",
        "cape": "Vainglory"
    },
    "infinity knight": {
        "purpose": "Bossfighter (DoT)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "interstellar knight": {
        "purpose": "Bossfighter (DoT)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "infinity titan": {
        "purpose": "Support (Buffs/Debuffs/Heals)",
        "class": "Wizard",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Forge",
        "cape": "Absolution"
    },
    "stonecrusher": {
        "purpose": "Support (Buffs/Debuffs/Heals)",
        "class": "Wizard",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Forge",
        "cape": "Absolution"
    },
    "legion paladin": {
        "purpose": "Bossfighter (DPS), Support (Buffs/Debuffs/Heals)",
        "class": "Wizard",
        "weapon": "Ravenous, Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "legion revenant": {
        "purpose": "Generalist, Hybrid Support (Debuffs)",
        "class": "Wizard",
        "weapon": "Valiance, Praxis",
        "helm": "Pneuma, Wizard",
        "cape": "Vainglory, Avarice"
    },
    "obsidian paladin chronomancer": {
        "purpose": "Support (Buffs/Debuffs/Heals)",
        "class": "Healer",
        "weapon": "Mana Vamp, Valiance",
        "helm": "Healer, Hearty",
        "cape": "Absolution"
    },
    "paladin chronomancer": {
        "purpose": "Support (Buffs/Debuffs/Heals)",
        "class": "Healer",
        "weapon": "Mana Vamp, Valiance",
        "helm": "Healer, Hearty",
        "cape": "Absolution"
    },
    "frostval barbarian": {
        "purpose": "Support (Buffs/Debuffs/Heals",
        "class": "Fighter",
        "weapon": "Arcana's Concerto, Awe Blast",
        "helm": "Fighter",
        "cape": "Absolution"
    },
    "lightcaster": {
        "purpose": "Bossfighter (Glass Cannon), Hybrid Support (Buffs/Nukes/Heals)",
        "class": "Wizard",
        "weapon": "Valiance, Praxis",
        "helm": "Pneuma, Wizard",
        "cape": "Vainglory, Lament"
    },
    "lightmage": {
        "purpose": "Bossfighter (Glass Cannon), Hybrid Support (Buffs/Nukes/Heals)",
        "class": "Wizard",
        "weapon": "Valiance, Praxis",
        "helm": "Pneuma, Wizard",
        "cape": "Vainglory, Lament"
    },
    "mage": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "mage (rare)": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "sorcerer": {
        "purpose": "N/A: Better suited for collecting only",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "mindbreaker": {
        "purpose": "Bossfighter (DPS)",
        "class": "Wizard",
        "weapon": "Dauntless",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "necromancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Penitence"
    },
    "pinkomancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Penitence"
    },
    "northlands monk": {
        "purpose": "Soloer (DPS), DPS Support (Buffs)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "oracle": {
        "purpose": "Support (Heals)",
        "class": "Wizard",
        "weapon": "Awe Blast",
        "helm": "Wizard",
        "cape": "Absolution"
    },
    "pink romancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Penitence"
    },
    "pyromancer": {
        "purpose": "Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Penitence"
    },
    "psionic mindbreaker": {
        "purpose": "Farming, Bossfighter (DPS)",
        "class": "Wizard",
        "weapon": "Dauntless, Valiance, Ravenous",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
    "scarlet sorceress": {
        "purpose": "Farming",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Lament"
    },
    "shaman": {
        "purpose": "Generalist, Hybrid Support (Buffs/Heals)",
        "class": "Wizard",
        "weapon": "Valiance, Elysium",
        "helm": "Examen, Pneuma",
        "cape": "Avarice, Vainglory"
    },
    "sovereign of storms (option 1": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Avarice"
    },
    "2 farming)": {
        "purpose": "Farming, Soloer (DPS)",
        "class": "Wizard",
        "weapon": "Elysium",
        "helm": "Pneuma",
        "cape": "Avarice"
    },
    "the collector": {
        "purpose": "Soloer (DPS), Stun PvP",
        "class": "Wizard",
        "weapon": "Ravenous",
        "helm": "Pneuma, Examen",
        "cape": "Lament"
    },
    "vindicator of they": {
        "purpose": "Soloer (DPS), Stun PvP",
        "class": "Wizard",
        "weapon": "Ravenous",
        "helm": "Pneuma, Examen",
        "cape": "Lament"
    },
    "troll spellsmith": {
        "purpose": "Generalist, Hybrid Support (Debuffs)",
        "class": "Wizard",
        "weapon": "Valiance",
        "helm": "Pneuma",
        "cape": "Vainglory"
    },
}


def dailies_embed(include_weekly=False):
    embed = discord.Embed(
        title="<:alert:1393035801008541717> Daily Reset" if not include_weekly else "<:alert:1393035801008541717> Daily + Weekly Reset",
        description="Request for help in <#1347562297937236112>",
        color=discord.Color.from_rgb(128, 0, 0)
    )
    
    embed.set_thumbnail(url="https://i.imgur.com/T9lX2Nm.png")

    # Organizing Classes
    embed.add_field(
        name="<:red:1393037160516550727> Classes",
        value=(
            "**Pyro:** Blaze Token\n"
            "**Cryo:** Ice Token\n"
            "**Collector:** Token of Collection *(Opt.)*\n"
            "**DKL:** Shadow Skull <:member:1392745711665283073>\n"
            "**LoO:** Lord of Order\n"
            "**SSG:** Daily *(Opt.)*\n"
            "**FB:** Crypto Token\n"
            "**VHL:** Elders' Blood"
        ),
        inline=False
    )

    # Organizing Boss Dailies
    embed.add_field(
        name="<:red1:1393037179210698792> Boss Dailies",
        value=(
            "**TimeInn Ultra Bosses:**\n"
            "• **UltraEzrajal** – Insignia\n"
            "• **UltraWarden** – Insignia\n"
            "• **UltraEngineer** – Insignia\n"
            "\n**AstralShrine** – Star of the Empyrean\n"
            "**Queen Iona** – Lothian’s Lightning *(F2P)*\n"
            "**UltraTyndarius** – Insignia\n"
            "**Apex Azalith** – Divinas Voluntas *(Opt.)*\n"
            "**Templeshrine** *(Opt.):*\n"
            "  - Moonlight, Sunlight, Ecliptic Offering"
        ),
        inline=False
    )

    # Organizing Useful Materials
    embed.add_field(
        name="<:red1:1393037179210698792> Useful Materials",
        value=(
            "**Friendship:** Gifts + NPCs\n"
            "**BLoD / SDKA:** Mine / Hardcore Metals <:member:1392745711665283073>\n"
            "**Drakath’s Armor:** Dage’s Scroll\n"
            "**NSoD:** Void Aura\n"
            "**Nulgath:** Voidbuquerque\n"
            "**Wheel Boosts:** 1hr <:member:1392745711665283073>\n"
            "**Legion Tokens:** Daily Exercise 1–6"
        ),
        inline=False
    )

    if include_weekly:
        embed.add_field(
            name="<:NUUU:1393035825381642472> Weeklies – Insignias",
            value=(
                "• **Nulgath** – `/join ultranulgath`\n"
                "• **Dage** – `/join ultradage`\n"
                "• **Drago** – `/join ultradrago`\n"
                "• **Drakath** – `/join championdrakath`\n"
                "• **Darkon** – `/join ultradarkon`\n"
                "• **Malgor** – `/join ultraspeaker`\n"
                "• **Gramiel** – `/join ultragramiel`"
            ),
            inline=False
        )

    embed.set_footer(text="Type /nn for more commands")
    return embed

# 🔧 !nn command
@bot.command(name='nn')
async def enhancement(ctx, *args):
    message = ' '.join(args).lower().strip()

    if message == "cruel":
        await ctx.send("**no drama. no fight. only love.**")
        return

    if message == "resetlist":
        embed = dailies_embed(include_weekly=True)
        await ctx.send(embed=embed)
        return

    if message == "potionguide":
        embed = discord.Embed(
            title="GENERAL POTIONS GUIDE\n\nTreat this list as a BASELINE",
            color=discord.Color.from_rgb(128, 0, 0)
        )
        embed.set_thumbnail(url="https://i.imgur.com/T9lX2Nm.png")

        embed.add_field(name="**Damage Type:**", value="1. Physical Damage\n2. Magic Damage\n3. Hybrid Damage", inline=False)

        embed.add_field(name="**Potion (Skill 6)**", value="1. Potent Honor/Malice Potion\n2. Potent Honor/Malice Potion\n3. Potent Honor/Malice Potion", inline=False)

        embed.add_field(name="**Elixir (15 Minutes)**", value="1. Potent/Unstable Battle Elixir\n2. Potent/Unstable Malevolence Elixir\n3. Potent Destruction/Unstable Keen Elixir", inline=False)

        embed.add_field(name="**Tonic (15 Minutes)**", value="1. Might/Unstable Might Tonic\n2. Sage/Unstable Sage Tonic\n3. Fate/Unstable Fate Tonic", inline=False)

        embed.add_field(name="**Additional Helpful Potions**", value="Potent Revitalize Elixir\nBody/Unstable Body Tonic\nUnstable Mastery Tonic\nUnstable Wise Tonic", inline=False)

        embed.set_footer(text="All Potions/Elixir/Tonics listed will most likely be the only ones you need")
        await ctx.send(embed=embed)
        return


    if not message:
        await ctx.send("Type `/nn` to see a list of available commands.")
        return

    if not message.startswith("enh for"):
        await ctx.send("Please read and use help??? wtf man: `/nn` to see a list of commands")
        return

    class_name = message.replace("enh for", "").strip()
    data = enhancements.get(class_name)

    if data:
        embed = discord.Embed(
            title=f"**Enhancements for {class_name.title()}**",
            color=discord.Color.from_rgb(128, 0, 0)
        )
        embed.add_field(name="Purpose", value=data['purpose'], inline=False)
        embed.add_field(name="Class", value=data['class'], inline=False)
        embed.add_field(name="Weapon", value=data['weapon'], inline=False)
        embed.add_field(name="Helm", value=data['helm'], inline=False)
        embed.add_field(name="Cape", value=data['cape'], inline=False)
        embed.set_footer(text="Feel free to change up the enhancements to suit your needs")
        embed.set_thumbnail(url="https://i.imgur.com/T9lX2Nm.png")  # Add the logo here
    else:
        embed = discord.Embed(
            title="Error",
            description=f"Sorry, I couldn't find enhancements for `{class_name}`. You dumbass bitch.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://i.imgur.com/T9lX2Nm.png")  # Add the logo here as well

    await ctx.send(embed=embed)


        # ⏰ Auto-post at 12:00 PM PH time
async def daily_reset_task():
    await bot.wait_until_ready()
    channel_id = 1350109632256802878  # your channel ID
    channel = bot.get_channel(channel_id)

    while not bot.is_closed():
        # Use PH time (UTC+8) for all calculations
        now_ph = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        target = now_ph.replace(hour=12, minute=0, second=0, microsecond=0)

        if now_ph > target:
            target += datetime.timedelta(days=1)

        wait_time = (target - now_ph).total_seconds()
        print(f"⏳ waiting {wait_time / 60:.2f} minutes until next dailies auto-post...")
        await asyncio.sleep(wait_time)

        # Recalculate current PH time after sleep
        now_ph = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        is_friday = now_ph.weekday() == 4  # Friday = 4

        # Send Daily Message
        embed_daily = dailies_embed(include_weekly=False)
        if channel:
            await channel.send(embed=embed_daily)

        # Send Weekly Message if Friday
        if is_friday:
            embed_weekly = discord.Embed(
                title="<:alert:1393035801008541717> Weekly Reset",
                description="Request for help in <#1347562297937236112>",
                color=discord.Color.from_rgb(128, 0, 0)
            )
            embed_weekly.set_thumbnail(url="https://i.imgur.com/T9lX2Nm.png")
            embed_weekly.add_field(
                name="Ultra Bosses",
                value=(
                    "• **Nulgath Insignia** – `/join ultranulgath`\n"
                    "• **Dage Insignia** – `/join ultradage`\n"
                    "• **King Drago Insignia** – `/join ultradrago`\n"
                    "• **Champion Drakath Insignia** – `/join championdrakath`\n"
                    "• **Darkon Insignia** – `/join ultradarkon`\n"
                    "• **Malgor Insignia** – `/join ultraspeaker`\n"
                    "• **Gramiel the Graceful Insignia** – `/join ultragramiel`"
                ),
                inline=False
            )
            embed_weekly.set_footer(text="Type /nn for more commands")
            await channel.send(embed=embed_weekly)


# 🔒 Run bot
bot.run(os.getenv("DISCORD_TOKEN"))
