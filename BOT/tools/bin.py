import csv
import os
import requests
import pycountry
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

BIN_CSV_FILE = "FILES/bins_all.csv"

# BIN lookup APIs (priority-wise)
BIN_LOOKUP_APIS = [
    "https://lookup.binlist.net/{}",  
    "https://api.bincodes.com/bin/?format=json&api_key=YOUR_API_KEY&bin={}",  
    "https://bins.payout.com/api/{}"
]

# Function to create CSV if not exists
def ensure_csv_exists():
    if not os.path.exists("FILES"):
        os.makedirs("FILES")
    
    if not os.path.exists(BIN_CSV_FILE):
        with open(BIN_CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["bin", "country", "flag", "brand", "type", "level", "bank"])  

# Function to check if BIN exists in CSV
def get_bin_info_from_csv(fbin):
    if not os.path.exists(BIN_CSV_FILE):
        ensure_csv_exists()
    
    with open(BIN_CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["bin"] == fbin:
                return row
    return None

# Function to fetch BIN details from API
def fetch_bin_from_api(fbin):
    for api_url in BIN_LOOKUP_APIS:
        try:
            response = requests.get(api_url.format(fbin), timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "bin": fbin,
                    "country": data.get("country", {}).get("alpha2", "N/A"),
                    "flag": data.get("country", {}).get("emoji", "🏳"),
                    "brand": data.get("scheme", "N/A").upper(),
                    "type": data.get("type", "N/A").upper(),
                    "level": data.get("brand", "N/A").upper(),
                    "bank": data.get("bank", {}).get("name", "Unknown")
                }
        except Exception as e:
            print(f"API Error for {api_url}: {e}")
    return None

# Function to save BIN details in CSV
def save_bin_to_csv(bin_info):
    ensure_csv_exists()

    # Check if BIN already exists (avoid duplicates)
    existing_data = get_bin_info_from_csv(bin_info["bin"])
    if existing_data:
        return

    with open(BIN_CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            bin_info["bin"], bin_info["country"], bin_info["flag"], bin_info["brand"], 
            bin_info["type"], bin_info["level"], bin_info["bank"]
        ])

# Command handler for BIN lookup
@Client.on_message(filters.command("bin", [".", "/"]))
async def cmd_bin(client, message):
    try:
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text("𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗕𝗜𝗡 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐁𝐈𝐍.", quote=True)
            return

        fbin = parts[1][:6]
        bin_info = get_bin_info_from_csv(fbin)

        # If not found in CSV, fetch from API
        if not bin_info:
            bin_info = fetch_bin_from_api(fbin)
            if bin_info:
                save_bin_to_csv(bin_info)  # Save newly fetched BIN info

        # If still not found, send error message
        if not bin_info:
            await message.reply_text("𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗕𝗜𝗡 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐁𝐈𝐍 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.", quote=True)
            return

        # Prepare response message
        country_name = pycountry.countries.get(alpha_2=bin_info["country"]).name if bin_info["country"] != "N/A" else "Unknown"
        resp = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗜𝗡: <code>{bin_info["bin"]}</code>
𝗜𝗻𝗳𝗼: <code>{bin_info["brand"]} - {bin_info["type"]} - {bin_info["level"]}</code>
𝐁𝐚𝐧𝐤: <code>{bin_info["bank"]} 🏛</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country_name} {bin_info["flag"]}</code>
"""
        await message.reply_text(resp, quote=True)

    except Exception as e:
        print(f"Error in /bin command: {e}")
