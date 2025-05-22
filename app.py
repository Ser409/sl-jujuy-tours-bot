from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "SL JUJUY TOURS BOT ACTIVO - LISTO PARA RECIBIR MENSAJES"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print(f"[WEBHOOK] Payload recibido: {data}")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/openai-clima', methods=['POST'])
def openai_clima():
    data = request.get_json()
    localidad = data.get("localidad", "")
    telefono = data.get("telefono", "")
    latitud = data.get("latitud", "")
    longitud = data.get("longitud", "")

    prompt = f"Dame el pronóstico del clima en {localidad}, latitud {latitud}, longitud {longitud}"

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        mensaje = respuesta.choices[0].message["content"]
        print(f"[OPENAI] Respuesta enviada: {mensaje}")
        return jsonify({"telefono": telefono, "mensaje": mensaje})
    except Exception as e:
        print(f"[ERROR OPENAI] {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
