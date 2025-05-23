import os
import requests
import pandas as pd

# Încarcă datele la start
SERVICII_DF = pd.read_excel("servicii.xlsx", sheet_name="servicii")

def is_qualified_lead(message):
    keywords = ["servicii", "preț", "colaborare", "abonament", "automatizare", "chatbot"]
    return any(word in message.lower() for word in keywords)

def get_price_info_from_excel():
    text = "Serviciile și prețurile noastre:\n"
    for _, row in SERVICII_DF.iterrows():
        text += f"- {row['serviciu']}: {row['descriere']} - {row['pret']}\n"
    return text

def get_contact_info_from_excel():
    # Poți adăuga în alt sheet info de contact, pentru demo punem static:
    return "Ne poți contacta la contact@firma-exemplu.com sau la telefon +373 600 00000."

def send_telegram_notification(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, data=data)
    print("Notificare Telegram:", response.status_code)

def send_to_hubspot(message, name, response):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    token = os.getenv("HUBSPOT_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "properties": {
            "email": f"{name.lower().replace(' ', '')}@gmail.com",
            "firstname": name,
            "message": message,
            "reply": response  # adăugat răspunsul AI în CRM
        }
    }

    response_hs = requests.post(url, headers=headers, json=data)
    print("Lead trimis în HubSpot:", response_hs.status_code)
