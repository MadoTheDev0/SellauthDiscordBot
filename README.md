# SellAuth Discord Bot

Ein Discord-Bot mit SellAuth-API-Integration inklusive Webhook-Receiver, Produktabfrage, Kundenverifizierung und Krypto-Auszahlung (BTC/LTC).

## Features

- 🛒 Produktanzeige mit `!produkte`
- 📧 Kundencheck mit `!check <email>`
- 🔐 Lizenzabfrage mit `!license <email>`
- 💰 Wallet-Saldo mit `!balance`
- 💸 Auszahlung mit `!payout <amount> <btc|ltc> <wallet>`
- 🌐 Webhook-Empfänger für Verkaufsbenachrichtigungen

## Setup

```bash
pip install -r requirements.txt
python bot.py
uvicorn webhook_server:app --host 0.0.0.0 --port 8080
 
