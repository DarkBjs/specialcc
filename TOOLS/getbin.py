import csv
import pycountry
import httpx
import os

# 🔹 List of Public BIN APIs (Auto-Fallback)
BIN_APIS = [
    "https://api.binlist.net/{}",   
    "https://bins.antipublic.cc/bins/{}", 
    "https://lookup.binlist.io/{}"
]

CSV_FILE = "FILES/bins_all.csv"  # CSV File Location

async def get_bin_details(cc):
    fbin = cc[:6]

    # 🔹 Step 1: Check in CSV First
    bin_info = get_bin_info_from_csv(fbin)
    if bin_info:
        return bin_info

    # 🔹 Step 2: Try Multiple APIs (Fetch BIN Data)
    for api in BIN_APIS:
        api_url = api.format(fbin)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, timeout=10)
                if response.status_code == 200:
                    bin_data = response.json()
                    bin_info = (
                        bin_data.get("scheme", "N/A").upper(),    # Brand (Visa/MasterCard)
                        bin_data.get("type", "N/A").upper(),      # Credit/Debit
                        bin_data.get("category", "N/A").upper(),  # Level (Gold/Platinum)
                        bin_data.get("bank", {}).get("name", "N/A").upper(), # Bank Name
                        bin_data.get("country", {}).get("alpha2", "N/A").upper(), # Country Code
                        bin_data.get("country", {}).get("emoji", "🏳"), # Country Flag
                        bin_data.get("country", {}).get("currency", "N/A") # Currency
                    )

                    # 🔹 Step 3: Save Data to CSV (Avoid Duplicates)
                    save_bin_to_csv(fbin, bin_info)
                    
                    return bin_info

        except Exception as e:
            print(f"❌ API Failed: {api_url} - {e}")

    # 🔹 Step 4: If No Data Found, Return Default
    return "N/A", "N/A", "N/A", "N/A", "N/A", "🏳", "N/A"

def get_bin_info_from_csv(fbin):
    """ Check if BIN already exists in CSV. """
    try:
        if not os.path.exists(CSV_FILE):  # If file doesn't exist, return empty
            return None

        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["bin"] == fbin:
                    return (
                        row["brand"].upper(),
                        row["type"].upper(),
                        row["level"].upper(),
                        row["bank"].upper(),
                        row["country"].upper(),
                        row["flag"],
                        row["currency"]
                    )
    except Exception as e:
        print(f"❌ CSV Read Error: {e}")

    return None  # If not found, return None

def save_bin_to_csv(fbin, bin_info):
    """ Save BIN details to CSV if not already present. """
    try:
        # Ensure the CSV file exists
        file_exists = os.path.exists(CSV_FILE)
        
        # Read existing BINs to avoid duplicates
        existing_bins = set()
        if file_exists:
            with open(CSV_FILE, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_bins.add(row["bin"])

        # If BIN is new, save it
        if fbin not in existing_bins:
            with open(CSV_FILE, "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                
                # Write headers if file is new
                if not file_exists:
                    writer.writerow(["bin", "brand", "type", "level", "bank", "country", "flag", "currency"])
                
                writer.writerow([fbin] + list(bin_info))

    except Exception as e:
        print(f"❌ CSV Write Error: {e}")
