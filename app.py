from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Ruta raíz para comprobar estado
@app.route('/', methods=['GET'])
def home():
    return "SL JUJUY TOURS BOT ACTIVO EN HEROKU."

# Ruta de verificación para el webhook de Meta
@app.route('/webhook', methods=['GET'])
def webhook_verify():
    verify_token = "SL_JUJUY_TOUR_VERIF"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return challenge, 200
    else:
        return "Token inválido o método no permitido", 403

# Ruta POST (opcional para pruebas actuales, no usada en verificación)
@app.route('/webhook', methods=['POST'])
def webhook():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run()
