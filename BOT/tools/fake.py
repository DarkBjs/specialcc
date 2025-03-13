import httpx
from pyrogram import Client, filters
from bs4 import BeautifulSoup
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

async def fetch_fake_data_fakexy(country_code):
    """ Fakexy.com se Fake Address Scrape karne ka function """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://www.fakexy.com/fake-address-generator-{country_code}')
            soup = BeautifulSoup(response.text, 'html.parser')

            fake_name = soup.find('td', text='Full Name').find_next_sibling('td').get_text(strip=True).title()
            fake_address = soup.find('td', text='Street').find_next_sibling('td').get_text(strip=True).title()
            fake_city = soup.find('td', text='City/Town').find_next_sibling('td').get_text(strip=True).title()
            fake_state = soup.find('td', text='State/Province/Region').find_next_sibling('td').get_text(strip=True).title()
            fake_country = soup.find('td', text='Country').find_next_sibling('td').get_text(strip=True).title()
            fake_zipcode = soup.find('td', text='Zip/Postal Code').find_next_sibling('td').get_text(strip=True).title()
            fake_gender = soup.find('td', text='Gender').find_next_sibling('td').get_text(strip=True).title()
            fake_phone = soup.find('td', text='Phone Number').find_next_sibling('td').get_text(strip=True).title()

            return {
                "name": fake_name, "gender": fake_gender, "address": fake_address,
                "city": fake_city, "state": fake_state, "zipcode": fake_zipcode,
                "phone": fake_phone, "country": fake_country
            }

    except Exception:
        return None  # Failover ke liye None return karega

async def fetch_fake_data_randomuser():
    """ Backup API (randomuser.me) se Fake Address Fetch karne ka function """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://randomuser.me/api/')
            data = response.json()["results"][0]

            return {
                "name": f"{data['name']['first']} {data['name']['last']}",
                "gender": data['gender'].title(),
                "address": data['location']['street']['name'],
                "city": data['location']['city'],
                "state": data['location']['state'],
                "zipcode": data['location']['postcode'],
                "phone": data['phone'],
                "country": data['location']['country']
            }

    except Exception:
        return None  # Agar API bhi fail ho jaye to None return karega

@Client.on_message(filters.command("fake", [".", "/"]))
async def cmd_fake(Client, message):
    try:
        checkall = await check_all_thing(Client, message)
        if not checkall[0]:
            return

        role = checkall[1]

        # User ne country diya hai ya nahi?
        country_code = message.text.split(" ")[1].lower() if len(message.text.split(" ")) > 1 else 'us'

        # **Step 1:** Pehle `fakexy.com` try karega
        fake_data = await fetch_fake_data_fakexy(country_code)

        # **Step 2:** Agar `fakexy.com` fail ho jaye, to `randomuser.me` use karega
        if fake_data is None:
            fake_data = await fetch_fake_data_randomuser()

        # **Step 3:** Agar dono sources fail ho jayein, to error message bhejo
        if fake_data is None:
            await message.reply_text("⚠️ Fake address generate karne me error aayi. Kripya dobara try karein.")
            return

        # **Response Format**
        resp = f"""
<b>Fake Info Created Successfully ✅</b>
━━━━━━━━━━━━━━
🆔 <b>Full Name:</b> <code>{fake_data['name']}</code>
👤 <b>Gender:</b> <code>{fake_data['gender']}</code>
🏠 <b>Street:</b> <code>{fake_data['address']}</code>
🏙️ <b>City/Town/Village:</b> <code>{fake_data['city']}</code>
🌍 <b>State/Province/Region:</b> <code>{fake_data['state']}</code>
📮 <b>Postal Code:</b> <code>{fake_data['zipcode']}</code>
📞 <b>Phone Number:</b> <code>{fake_data['phone']}</code>
🌏 <b>Country:</b> <code>{fake_data['country']}</code>
━━━━━━━━━━━━━━
<b>Checked By:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [ {role} ]
<b>Bot by:</b> <a href="tg://user?id=7028548502">亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼 Bᴀʟᴀᴋ (◕‿◕</a>
"""
        await message.reply_text(resp)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
