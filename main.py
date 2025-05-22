from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/', methods=['GET'])
def home():
    return "SL JUJUY TOURS BOT ACTIVO EN HEROKU."


@app.route('/webhook', methods=['GET'])
def webhook_verify():
    verify_token = "SL_JUJUY_TOUR_VERIF"
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == verify_token:
            return challenge, 200
        else:
            return 'Token inválido', 403
    return 'Método no permitido', 405


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("[INFO][OK] Payload recibido:", data)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"error": str(e)}), 500


@app.route('/openai-clima', methods=['POST'])
def openai_clima():
    try:
        data = request.get_json()
        localidad = data.get("localidad", "")
        latitud = data.get("latitud", "")
        longitud = data.get("longitud", "")

        prompt = f"Frase de pronóstico del clima en {localidad}, latitud {latitud}, longitud {longitud}"

        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        mensaje = respuesta.choices[0].message["content"]
        print("[OPENAI] Respuesta enviada:", mensaje)
        return jsonify({"respuesta": mensaje}), 200

    except Exception as e:
        print("[ERROR OPENAI]", e)
        return jsonify({"error": str(e)}), 500
