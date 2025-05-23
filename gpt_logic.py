import os
from openai import OpenAI
from dotenv import load_dotenv
from utils import is_qualified_lead, get_price_info_from_excel, get_contact_info_from_excel, send_to_hubspot, send_telegram_notification

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_response(message):
    # Răspunsuri predefinite pe baza mesajului
    if "cât costă" in message.lower() or "preț" in message.lower() or "servicii" in message.lower():
        return get_price_info_from_excel()

    if "contact" in message.lower() or "cum vă pot găsi" in message.lower():
        return get_contact_info_from_excel()

    # Folosește GPT pentru restul întrebărilor, cu prompt în română
    try:
        system_prompt = (
            "Ești un asistent AI care răspunde doar în limba română cand scrie in limba romana, cand scrie in limba rusa raspunzi in limba rusa. Cand scrie in limba engleza raspunzi in engleza "
            "Oferă informații clare despre servicii, prețuri, colaborare. "
            "Evită să răspunzi în alte limbi decat in care iti scrie sau la întrebări nelegate."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.6,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"A apărut o eroare: {e}"

def handle_user_message(user_message, user_name):
    gpt_reply = get_gpt_response(user_message)

    if is_qualified_lead(user_message):
        send_to_hubspot(user_message, user_name, gpt_reply)
        send_telegram_notification(f"Lead nou calificat!\nNume: {user_name}\nMesaj: {user_message}\nRăspuns: {gpt_reply}")

    return gpt_reply
