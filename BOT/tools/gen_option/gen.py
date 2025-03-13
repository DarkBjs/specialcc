import httpx
import os
import threading
import asyncio
import time
import csv
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.cc_gen import *
from TOOLS.check_all_func import *

# 📌 List of Public APIs for BIN Lookup
BIN_APIS = [
    "https://lookup.binlist.net/{}",  # API 1
    "https://bins.payouts.com/api/{}",  # API 2
    "https://api.bincodes.com/bin/{}?api_key=YOUR_API_KEY"  # API 3 (Replace with actual key)
]

BIN_FILE = "FILES/bins_all.csv"  # BIN details storage file

# ✅ Ensure BIN storage file exists
if not os.path.exists("FILES"):
    os.makedirs("FILES")

if not os.path.exists(BIN_FILE):
    with open(BIN_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["BIN", "Brand", "Type", "Level", "Bank", "Country", "Flag", "Currency"])


async def fetch_bin_from_api(bin_number):
    """Fetch BIN details from multiple public APIs"""
    for api_url in BIN_APIS:
        try:
            url = api_url.format(bin_number)
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    # Extract necessary details
                    return {
                        "brand": data.get("scheme", "N/A").upper(),
                        "type": data.get("type", "N/A").upper(),
                        "level": data.get("brand", "N/A").upper(),
                        "bank": data.get("bank", {}).get("name", "N/A"),
                        "country": data.get("country", {}).get("name", "N/A"),
                        "flag": data.get("country", {}).get("emoji", "🏳️"),
                        "currency": data.get("country", {}).get("currency", "N/A")
                    }
        except Exception:
            continue  # Try next API if one fails
    return None  # If all APIs fail


def save_bin_details(bin_number, bin_data):
    """Save unique BIN details to CSV (No duplicates)"""
    with open(BIN_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        bin_list = [row[0] for row in reader]

    if bin_number not in bin_list:  # Avoid duplicate entries
        with open(BIN_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                bin_number, bin_data["brand"], bin_data["type"], bin_data["level"],
                bin_data["bank"], bin_data["country"], bin_data["flag"], bin_data["currency"]
            ])


def generate_code_blocks(all_cards):
    """Format generated cards in <code> blocks for Telegram."""
    return "\n".join([f"<code>{card}</code>" for card in all_cards.split("\n")])


@Client.on_message(filters.command("gen", [".", "/"]))
def multi(client, message):
    t1 = threading.Thread(target=bcall, args=(client, message))
    t1.start()


def bcall(client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gen_cmd(client, message))
    loop.close()


async def gen_cmd(client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        role = checkall[1]

        try:
            ccsdata = message.text.split()[1]
            cc_parts = ccsdata.split("|")
            cc = cc_parts[0]
            mes = cc_parts[1] if len(cc_parts) > 1 else None
            ano = cc_parts[2] if len(cc_parts) > 2 else None
            cvv = cc_parts[3] if len(cc_parts) > 3 else None
        except IndexError:
            await message.reply_text(
                "❌ 𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁\n\nUsage:\n<code>/gen 447697</code>\n<code>/gen 447697|12|23</code>\n",
                message.id
            )
            return

        # Default generation amount
        amount = 10
        try:
            amount = int(message.text.split()[2])
        except (IndexError, ValueError):
            pass

        # Restrict amount to avoid abuse
        if amount > 10000:
            await message.reply_text("⚠️ 𝗠𝗮𝘅 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗼𝗻 𝗟𝗶𝗺𝗶𝘁 𝟭𝟬𝗞.", message.id)
            return

        delete = await message.reply_text("<b>𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴...</b>", message.id)
        start = time.perf_counter()

        # Fetch BIN Details
        bin_info = await fetch_bin_from_api(cc[:6])
        if not bin_info:
            await message.reply_text("⚠️ 𝗕𝗜𝗡 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱", message.id)
            return
        
        # Save BIN details if new
        save_bin_details(cc[:6], bin_info)

        # Generate Cards
        all_cards = await luhn_card_genarator(cc, mes, ano, cvv, amount)

        # Prepare Response
        if amount == 10:
            resp = f"""
✔️ 𝐂𝐂 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!

- 𝐁𝐈𝐍: <code>{cc}</code>
- 𝐀𝐦𝐨𝐮𝐧𝐭: {amount}

{generate_code_blocks(all_cards)}

- 𝗜𝗻𝗳𝗼: {bin_info["brand"]} - {bin_info["type"]} - {bin_info["level"]}
- 𝐁𝐚𝐧𝐤: {bin_info["bank"]} 🏛  
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {bin_info["country"]} {bin_info["flag"]} - {bin_info["currency"]}

- ⏳ 𝐓𝐢𝐦𝐞: {time.perf_counter() - start:0.2f} 𝐬𝐞𝐜
- 🔍 𝐂𝐡𝐞𝐜𝐤𝐞𝐝: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ({role})
"""
            await client.delete_messages(message.chat.id, delete.id)
            await message.reply_text(resp, message.id)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
