from pyrogram import Client 
import json
import threading
from flask import Flask
from FUNC.server_stats import *

# Load configuration
plugins = dict(root="BOT")

with open("FILES/config.json", "r", encoding="utf-8") as f:
    DATA      = json.load(f)
    API_ID    = DATA["API_ID"]
    API_HASH  = DATA["API_HASH"]
    BOT_TOKEN = DATA["BOT_TOKEN"]

# Pyrogram Clients
user = Client( 
            "Scrapper", 
             api_id   = API_ID, 
             api_hash = API_HASH
              )

bot = Client(
    "MY_BOT", 
    api_id    = API_ID, 
    api_hash  = API_HASH, 
    bot_token = BOT_TOKEN, 
    plugins   = plugins 
)

# Dummy Web Server for Koyeb Health Check
app = Flask(__name__)

@app.route("/")
def health_check():
    return "OK", 200  # Koyeb health check endpoint

def run_flask():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start the dummy web server in a separate thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start the bot
    print("Done Bot Active ✅")
    print("NOW START BOT ONCE MY MASTER")

    bot.run()
