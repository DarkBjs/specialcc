from FUNC.defs import *
from pyrogram import Client, filters

@Client.on_message(filters.command("host", [".", "/"]))
async def cmd_host(client, message):
    try:
        response = "<b>𝐁𝐨𝐭 𝐢𝐬 𝐇𝐨𝐬𝐭𝐞𝐝 𝐁𝐲: @Flex_Coder 👩‍💻</b>"
        await message.reply_text(response, quote=True)
    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
