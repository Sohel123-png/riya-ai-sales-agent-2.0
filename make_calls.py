"""contacts.csv (columns: name,phone) ke numbers par outbound call karta hai."""
import csv, os, time, requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.environ["VAPI_API_KEY"]
ASSISTANT = os.environ["VAPI_ASSISTANT_ID"]
PHONE_ID = os.environ["VAPI_PHONE_NUMBER_ID"]

def dnc():
    return set(open("do_not_call.txt").read().split()) if os.path.exists("do_not_call.txt") else set()

blocked = dnc()
for row in csv.DictReader(open("contacts.csv", encoding="utf-8")):
    phone = row["phone"].strip()
    if phone in blocked:
        print("Skip (DNC):", phone)
        continue
    r = requests.post("https://api.vapi.ai/call",
        headers={"Authorization": f"Bearer {KEY}"},
        json={"assistantId": ASSISTANT, "phoneNumberId": PHONE_ID,
              "customer": {"number": phone, "name": row.get("name", "")}}, timeout=30)
    print(phone, r.status_code)
    time.sleep(60)  # ek call ke baad gap, spam se bachne ke liye
