from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_secure_token_123")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == os.getenv('VERIFY_TOKEN'):
        return request.args.get('hub.challenge'), 200
    return "Invalid verify token", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Yangi Lead kelganda"""
    try:
        data = request.get_json()
        
        if data and 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    if change.get('field') == 'leadgen':
                        lead = change['value']
                        
                        name = lead.get('full_name') or lead.get('name') or 'Noma\'lum'
                        phone = lead.get('phone_number') or 'Yo\'q'
                        email = lead.get('email') or 'Yo\'q'
                        ad_name = lead.get('ad_name') or 'Noma\'lum'
                        created_time = lead.get('created_time') or datetime.now().strftime("%Y-%m-%d %H:%M")

                        message = f"""
🔔 <b>YANGI LID!</b>

👤 <b>Ism:</b> {name}
📞 <b>Telefon:</b> {phone}
✉️ <b>Email:</b> {email}
🕒 <b>Vaqt:</b> {created_time}
📢 <b>Reklama:</b> {ad_name}
                        """.strip()

                        send_message(message)
                        print("✅ Lid yuborildi!")
    except Exception as e:
        print("Xato:", e)
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)