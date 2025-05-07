import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SELLAUTH_API_KEY = os.getenv("SELLAUTH_API_KEY")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

BASE_URL = "https://api.sellauth.com/v1"
HEADERS = {
    "Authorization": f"Bearer {SELLAUTH_API_KEY}",
    "Content-Type": "application/json"
}

@bot.event
async def on_ready():
    print(f"✅ Bot gestartet als {bot.user}")

@bot.command()
async def produkte(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/products", headers=HEADERS) as resp:
            if resp.status == 200:
                products = await resp.json()
                if not products:
                    await ctx.send("Keine Produkte gefunden.")
                    return
                msg = "\n".join([f"🔹 **{p['name']}** – {p['price']} {p['currency']}" for p in products])
                await ctx.send(msg)
            else:
                await ctx.send("Fehler beim Abrufen der Produkte.")

@bot.command()
async def check(ctx, email):
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/customers/email/{email}"
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                name = data.get("name", "Unbekannt")
                orders = data.get("orders", [])
                await ctx.send(f"👤 **{name}** hat {len(orders)} Bestellungen.")
            else:
                await ctx.send("❌ Kunde nicht gefunden.")

@bot.command()
async def license(ctx, email):
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/licenses/email/{email}"
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data:
                    msg = "\n".join([f"🔑 {lic['licenseKey']} – {lic['productName']}" for lic in data])
                    await ctx.send(msg)
                else:
                    await ctx.send("Keine Lizenzen gefunden.")
            else:
                await ctx.send("Fehler beim Abrufen der Lizenzdaten.")
@bot.command()
async def payout(ctx, amount: float, currency: str, address: str):
currency = currency.lower()
    if currency not in ["btc", "ltc"]:
        await ctx.send("❌ Ungültige Währung. Nur `btc` und `ltc` erlaubt.")
        return

    payload = {
        "amount": amount,
        "currency": currency,
        "walletAddress": address
    }

    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/crypto/payout"
        async with session.post(url, json=payload, headers=HEADERS) as resp:
            if resp.status == 200:
                await ctx.send(f"✅ Auszahlung von {amount} {currency.upper()} an {address} erfolgreich.")
            else:
                err = await resp.text()
                await ctx.send(f"❌ Fehler bei Auszahlung: {err}")


@bot.command()
async def balance(ctx):
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/crypto/balance"
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                balances = await resp.json()
                if balances:
                    msg = "\n".join([f"💰 {b['currency'].upper()}: {b['balance']} (Wallet: {b['walletAddress']})" for b in balances])
                    await ctx.send(f"**Wallet Balances:**\n{msg}")
                else:
                    await ctx.send("Keine Wallets gefunden.")
            else:
                await ctx.send("Fehler beim Abrufen des Wallet-Saldos.")

bot.run(DISCORD_TOKEN)
