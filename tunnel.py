import os
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()
ngrok.set_auth_token(os.environ["NGROK_AUTHTOKEN"])
t = ngrok.connect(8000)
print("\nSERVER_URL =", t.public_url + "/vapi\n")
input("Band karne ke liye Enter dabao...\n")