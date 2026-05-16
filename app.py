from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except:
        pass

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return "Invalid", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if data and 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    if change.get('field') == 'leadgen':
                        lead = change['value']
                        name = lead.get('full_name') or 'Noma\'lum'
                        phone = lead.get('phone_number') or 'Yo\'q'
                        message = f"""
🔔 <b>YANGI LID!</b>

👤 Ism: {name}
📞 Tel: {phone}
                        """
                        send_telegram(message.strip())
    except:
        pass
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)