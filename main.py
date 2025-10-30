from flask import Flask, request, jsonify
from flask_cors import CORS
import pusher
import os

app = Flask(__name__)
CORS(app)

# Pusher (juan) - usa las credenciales que ya tienes
pusher_client = pusher.Pusher(
    app_id="2068346",
    key="5398827de005ac67b6b2",
    secret="342442a921382d60170b",
    cluster="us2",
    ssl=True
)

@app.route("/", methods=["POST"])
def send_message():
    data = request.get_json() or {}

    # soportar distintos formatos entrantes
    message = data.get("message", "")
    if isinstance(message, dict):
        # puede ser { message: "texto" } o { mensaje: "texto" }
        message = message.get("message") or message.get("mensaje") or ""
    sender_id = data.get("senderId")
    channel = data.get("channel", "josue-juanito")

    # trigger consistente: enviar { message: <texto>, senderId: <id> }
    try:
        pusher_client.trigger(channel, "my-event", {"message": message, "senderId": sender_id})
    except Exception as e:
        print("Pusher trigger error:", e)
        return jsonify({"status": "error", "error": str(e)}), 500

    return jsonify({"status": "ok", "channel": channel, "message": message}), 200

# opcional: endpoint para health
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True)