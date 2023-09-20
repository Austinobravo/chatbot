from flask import Flask, request
from decouple import config
import services
import mysecrets

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'My Special Assisstant'

@app.route('/webhook', methods=['GET'])
def verify_token():
    if request.method == 'GET':
        try:
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            
            if token == mysecrets.Token and challenge != None:
                return challenge
            else:
                return 'Incorrect token', 403
        except Exception as e:
            return str(e), 403
        
@app.route('/webhook', methods=['POST'])
def receive_messages():
        try:
            body = request.json
            entry = body['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            message = value['messages'][0]
            number = message['from']
            messageId = message['id']
            contacts = value['contacts'][0]
            name = contacts['profile']['name']
            text = services.type_of_message(message)
            services.chatbot_admin(text, number, messageId, name)

            return 'Sent'
        
        except Exception as e:
            app.logger.error("Error in receive_messages: %s", str(e))
            return 'Not sent' + str(e)




    

if __name__ == '__main__':
    app.run(debug=True)