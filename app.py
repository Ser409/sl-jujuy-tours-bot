from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Endpoint base para verificar despliegue
@app.route("/", methods=['GET'])
def home():
    return "SL JUJUY TOURS BOT ACTIVO EN HEROKU."

# Endpoint para verificación del webhook con GET
@app.route("/webhook", methods=['GET'])
def webhook_verify():
    verify_token = "SL_JUJUY_TOUR_VERIF"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return challenge, 200
    else:
        return "Token inválido o método no permitido", 403

# Endpoint para recepción de mensajes con POST
@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("[INFO][OK] Payload recibido:", data)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"error": str(e)}), 500
