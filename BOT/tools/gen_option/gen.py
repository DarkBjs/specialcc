import httpx
import os
import threading
import asyncio
import time
from pyrogram import Client, filters

# Import your functions
from FUNC.usersdb_func import *
from FUNC.cc_gen import *
from TOOLS.check_all_func import *

# Function to generate formatted CC output
def generate_code_blocks(all_cards):
    return "\n".join(f"<code>{card}</code>" for card in all_cards.split('\n'))

# Command Handler
@Client.on_message(filters.command("gen", [".", "/"]))
def multi(client, message):
    threading.Thread(target=bcall, args=(client, message)).start()

# Thread handler
def bcall(client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gen_cmd(client, message))
    loop.close()

async def fetch_bin_info(bin_number):
    urls = [
        f"https://lookup.binlist.net/{bin_number}",
        f"https://api.bincodes.com/bin/?format=json&api_key=YOUR_API_KEY&bin={bin_number}"
    ]
    
    for url in urls:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "brand": data.get("scheme", "Unknown").upper(),
                        "type": data.get("type", "Unknown").upper(),
                        "level": data.get("brand", "Unknown").upper(),
                        "bank": data.get("bank", {}).get("name", "Unknown").upper(),
                        "country": data.get("country", {}).get("name", "Unknown").upper(),
                        "currency": data.get("country", {}).get("currency", "USD"),
                        "flag": data.get("country", {}).get("emoji", "🏳")
                    }
        except Exception:
            continue
    return None

async def gen_cmd(client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return
        role = checkall[1]

        # Extract CC details
        try:
            ccsdata = message.text.split()[1]
            cc_parts = ccsdata.split("|")
            cc = cc_parts[0]
            mes = cc_parts[1] if len(cc_parts) > 1 else None
            ano = cc_parts[2] if len(cc_parts) > 2 else None
            cvv = cc_parts[3] if len(cc_parts) > 3 else None
        except IndexError:
            await message.reply_text(
                """𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌
                
𝗨𝘀𝗮𝗴𝗲:
Only Bin: <code>/gen 447697</code>  
With Exp: <code>/gen 447697|12|23</code>  
With CVV: <code>/gen 447697|12|23|000</code>  
Custom Amount: <code>/gen 447697 100</code>""",
                message.id
            )
            return

        # Default CC amount
        amount = 10
        try:
            amount = int(message.text.split()[2])
        except (IndexError, ValueError):
            pass

        if amount > 10000:
            await message.reply_text("<b>𝗟𝗶𝗺𝗶𝘁 𝗘𝘅𝗰𝗲𝗲𝗱𝗲𝗱 ⚠️\n\n𝗠𝗮𝘅𝗶𝗺𝘂𝗺: 𝟭𝟬,𝟬𝟬𝟬 𝗖𝗖𝘀</b>", message.id)
            return

        # Loading animation
        loading_message = await message.reply_text("𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴 𝗖𝗖𝘀...\n■■■□", message.id)

        start = time.perf_counter()
        bin_info = await fetch_bin_info(cc[:6])

        if not bin_info:
            await loading_message.edit("<b>𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗳𝗲𝘁𝗰𝗵 𝗕𝗜𝗡 𝗱𝗮𝘁𝗮 ❌</b>")
            return

        all_cards = await luhn_card_genarator(cc, mes, ano, cvv, amount)

        # Preparing response
        bin_details = f"""
━━━━━━━━━━━━━━━━━  
𝗕𝗜𝗡 𝗜𝗡𝗙𝗢:  
━━━━━━━━━━━━━━━━━  
𝗕𝗜𝗡: {cc[:6]}  
𝗕𝗥𝗔𝗡𝗗: {bin_info["brand"]}  
𝗧𝗬𝗣𝗘: {bin_info["type"]}  
𝗟𝗘𝗩𝗘𝗟: {bin_info["level"]}  
𝗕𝗔𝗡𝗞: {bin_info["bank"]}  
𝗖𝗢𝗨𝗡𝗧𝗥𝗬: {bin_info["country"]} {bin_info["flag"]}  
𝗖𝗨𝗥𝗥𝗘𝗡𝗖𝗬: {bin_info["currency"]}  
━━━━━━━━━━━━━━━━━  
🕒 **Processing Time:** {time.perf_counter() - start:.2f} sec  
👤 **Checked By:** <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ⤿ {role} ⤾
"""

        # If amount ≤ 10, send in text format
        if amount <= 10:
            response = f"""𝗖𝗔𝗥𝗗𝗦 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘𝗗 ✅\n\n{generate_code_blocks(all_cards)}\n{bin_details}"""
            await loading_message.edit(response)

        # If amount > 10, send as a document
        else:
            filename = f"downloads_{amount}x_CC_Generated_By_{user_id}.txt"
            with open(filename, "w") as f:
                f.write(all_cards)

            caption = f"""𝗖𝗔𝗥𝗗𝗦 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘𝗗 ✅\n\n𝗕𝗜𝗡: {cc[:6]}\n𝗔𝗠𝗢𝗨𝗡𝗧: {amount}\n\n{bin_details}"""
            await client.send_document(message.chat.id, document=filename, caption=caption, reply_to_message_id=message.id)
            os.remove(filename)

    except Exception as e:
        await message.reply_text(f"<b>𝗘𝗿𝗿𝗼𝗿: {str(e)}</b>", message.id)
