from flask import Flask, request, jsonify
from flask_cors import CORS
import pusher

app = Flask(__name__)
CORS(app)

pusher_client = pusher.Pusher(
  app_id = "2068346",
  key = "5398827de005ac67b6b2",
  secret = "342442a921382d60170b",
  cluster = "us2",
  ssl = True
)

@app.route('/', methods=['POST'])  # Cambiar a ruta raíz
def send_message():
    data = request.get_json()
    message = data.get('message')
    if isinstance(message, dict):
        message = message.get('message')  # Extraer mensaje anidado
    sender_id = data.get('senderId')
    channel = data.get('channel', 'josue-juanito')

    # Corregir el formato del trigger
    pusher_client.trigger(channel, 'my-event', {
        'message': message,  # Enviar solo el texto, sin anidación
        'senderId': sender_id
    })
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)