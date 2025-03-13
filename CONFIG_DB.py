import pymongo
import dns.resolver

# 🔹 DNS Resolver को सेट करें (Google DNS 8.8.8.8)
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]

try:
    client = pymongo.MongoClient(
        "mongodb+srv://Balak:43rVmgThcLlKpAms@balak.l3sw4.mongodb.net/?retryWrites=true&w=majority&appName=BALAK"
    )

    client.admin.command('ping')  # कनेक्शन टेस्ट करें
    print("✅ CONFIG DB CONNECTED SUCCESSFULLY!")

except pymongo.errors.ConnectionFailure as e:
    print("❌ CONFIG DB CONNECTION FAILED:", e)
except Exception as e:
    print("❌ ERROR:", e)


