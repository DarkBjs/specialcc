import httpx
import os
import threading
import asyncio
import time
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.cc_gen import *
from TOOLS.check_all_func import *


BIN_APIS = [
    "https://lookup.binlist.net/",
    "https://bins.antipublic.cc/bins/",
    "https://bin-checker.net/api/",
]


async def fetch_bin_info(bin_number):
    async with httpx.AsyncClient(timeout=10) as session:
        for api in BIN_APIS:
            try:
                response = await session.get(f"{api}{bin_number}")
                if response.status_code == 200:
                    return response.json()
            except Exception:
                continue  
    return None  


def format_cards(cards_list):
    return "\n".join([f"<code>{card}</code>" for card in cards_list.split("\n")])


@Client.on_message(filters.command("gen", [".", "/"]))
def multi(client, message):
    threading.Thread(target=run_gen_command, args=(client, message)).start()


def run_gen_command(client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gen_command(client, message))
    loop.close()


async def gen_command(client, message):
    try:
        user_id = str(message.from_user.id)
        check_result = await check_all_thing(client, message)
        if not check_result[0]:
            return

        role = check_result[1]

        try:
            cc_input = message.text.split()[1]
            cc_parts = cc_input.split("|")
            cc = cc_parts[0]
            mes = cc_parts[1] if len(cc_parts) > 1 else None
            ano = cc_parts[2] if len(cc_parts) > 2 else None
            cvv = cc_parts[3] if len(cc_parts) > 3 else None
        except IndexError:
            error_msg = """
𝗜𝗡𝗖𝗢𝗥𝗥𝗘𝗖𝗧 𝗙𝗢𝗥𝗠𝗔𝗧 ❌

𝗨𝗦𝗔𝗚𝗘:
- 𝗢𝗻𝗹𝘆 𝗕𝗜𝗡:  
<code>/gen 447697</code>

- 𝗪𝗶𝘁𝗵 𝗘𝘅𝗽𝗶𝗿𝗮𝘁𝗶𝗼𝗻:  
<code>/gen 447697|12</code>  
<code>/gen 447697|12|23</code>  

- 𝗪𝗶𝘁𝗵 𝗖𝗩𝗩:  
<code>/gen 447697|12|23|123</code>

- 𝗪𝗶𝘁𝗵 𝗖𝘂𝘀𝘁𝗼𝗺 𝗔𝗺𝗼𝘂𝗻𝘁:  
<code>/gen 447697 100</code>
"""
            await message.reply_text(error_msg, message.id)
            return

        amount = 10  
        try:
            amount = int(message.text.split()[2])
        except (IndexError, ValueError):
            pass

        loading_msg = await message.reply_text("𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼 & 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴 𝗖𝗖...\n𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 ⏳", message.id)

        start_time = time.perf_counter()

        bin_info = await fetch_bin_info(cc[:6])

        if bin_info:
            brand = bin_info.get("scheme", "Unknown").upper()
            type_ = bin_info.get("type", "Unknown").upper()
            level = bin_info.get("brand", "Unknown").upper()
            bank = bin_info.get("bank", {}).get("name", "Unknown")
            country = bin_info.get("country", {}).get("name", "Unknown")
            flag = bin_info.get("country", {}).get("emoji", "")
            currency = bin_info.get("country", {}).get("currency", "Unknown")
        else:
            brand, type_, level, bank, country, flag, currency = ["Unknown"] * 7

        if amount > 10000:
            await loading_msg.edit_text("𝗟𝗜𝗠𝗜𝗧 𝗥𝗘𝗔𝗖𝗛𝗘𝗗 ⚠️\n𝗠𝗔𝗫 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗜𝗢𝗡 𝗟𝗜𝗠𝗜𝗧: 𝟭𝟬𝗞.", message.id)
            return

        all_cards = await luhn_card_genarator(cc, mes, ano, cvv, amount)

        if amount <= 10:
            response = f"""
𝗖𝗔𝗥𝗗𝗦 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘𝗗 ✅  

𝗕𝗜𝗡: <code>{cc}</code>  
𝗔𝗠𝗢𝗨𝗡𝗧: {amount}  

𝗜𝗡𝗙𝗢: {brand} - {type_} - {level}  
𝗕𝗔𝗡𝗞: {bank}  
𝗖𝗢𝗨𝗡𝗧𝗥𝗬: {country} {flag}  
𝗖𝗨𝗥𝗥𝗘𝗡𝗖𝗬: {currency}  

𝗧𝗜𝗠𝗘 𝗧𝗔𝗞𝗘𝗡: {time.perf_counter() - start_time:.2f} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀  
𝗖𝗛𝗘𝗖𝗞𝗘𝗗 𝗕𝗬: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [{role}]

{format_cards(all_cards)}
"""
            await client.delete_messages(message.chat.id, loading_msg.id)
            await message.reply_text(response, message.id)

        else:
            filename = f"downloads/{amount}x_CC_Generated_By_{user_id}.txt"
            with open(filename, "w") as file:
                file.write(all_cards)

            caption = f"""
𝗕𝗜𝗡: <code>{cc}</code>  
𝗔𝗠𝗢𝗨𝗡𝗧: {amount}  

𝗜𝗡𝗙𝗢: {brand} - {type_} - {level}  
𝗕𝗔𝗡𝗞: {bank}  
𝗖𝗢𝗨𝗡𝗧𝗥𝗬: {country} {flag}  
𝗖𝗨𝗥𝗥𝗘𝗡𝗖𝗬: {currency}  

𝗧𝗜𝗠𝗘 𝗧𝗔𝗞𝗘𝗡: {time.perf_counter() - start_time:.2f} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀  
𝗖𝗛𝗘𝗖𝗞𝗘𝗗 𝗕𝗬: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [{role}]
"""
            await client.delete_messages(message.chat.id, loading_msg.id)
            await message.reply_document(filename, caption=caption, reply_to_message_id=message.id)
            os.remove(filename)

    except Exception as e:
        import traceback
        await message.reply_text("𝗘𝗥𝗥𝗢𝗥 ❌\n𝗙𝗔𝗜𝗟𝗘𝗗 𝗧𝗢 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘.", message.id)
        print(traceback.format_exc())
