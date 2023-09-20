import json
import requests
from decouple import config
import mysecrets
import time

def type_of_message(message):
    if 'type' not in message:
        text = 'message not recognized'
        return text

    type_message = message['type']
    if type_message == 'text':
        text = message['text']['body']
        print('te', text)
    
    elif type_message == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']

    elif type_message == 'interactive' and message['interactive']['type'] == 'button_reply':
        # Extract content from the interactive button message
        text = message['interactive']['button_reply']['title']
        print('text', text)



    else:
        text = 'Unrecognized message'
    return text

def whatsapp_api(data):
    try:
        whatsapp_token = mysecrets.Whatsapp_Token
        whatsapp_url = mysecrets.Whatsapp_Url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        response = requests.post(whatsapp_url, 
                                 headers=headers, data=data)
        
        print('API Request Data:', data)
        print('API Response Status Code:', response.status_code)
        print('API Response Content:', response.content)

        if response.status_code == 200:
            return 'message sent', 200
        else:
            return 'An error occured.', response.status_code
    except Exception as e:
        print('API Request Error:', str(e))
        return str(e), 403

def text_Message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to":number,
            "type": "text",
            "text":{
                "body": text
            }

        }
    )
    print('data', data)
    return data

def button_reply_message(number, options, body, footer, sedd, messageId):
    buttons = []

    for index, option in enumerate(options):
        buttons.append(
            {
            "type": "reply",
            "reply":{
                "id": sedd + "_btn_" + str(index+1),
                "title": option,
            }
            }
        )

    data = json.dumps(
        {
            
            "messaging_product":"whatsapp",
            "recipient_type": "individual",
            "to":number,
            "type": "interactive",
            "interactive":{
                "type": "button",

                    "body": {
                        "text": body
                    },
                    "footer": {
                        "text": footer
                    },
                    "action":{
                        "buttons": buttons
                    }

                }
        }

    )
    return data

def list_reply_message(number, options, body, footer, sedd, messageId):
    rows = []

    for index, option in enumerate(options):
        rows.append(
            {
            "id": sedd + "_row_" + str(index+1),
            "title": option,
            }
        )

    data = json.dumps(
        {      
            "messaging_product":"whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",

                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "All Sections",
                    "sections": [
                        {
                            "title": "Section",
                            "rows": rows
                        },
                    ]
                }
            }
        }
    )
    return data

def document_message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type":"individual",
            "to": number,
            "type": "document",
            "document":{
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_message(number,sticker_id):
    data = json.dumps(
        {
           "messaging_product": "whatsapp",
            "recipient_type":"individual",
            "to": number,
            "type": "sticker",
            "document":{
                "id": sticker_id,
            }
        }
    )
    return data

def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "image":
        media_id = mysecrets.image.get(media_name,None)
    elif media_type == "video":
        media_id = mysecrets.video.get(media_name,None)
    elif media_type == "audio":
        media_id = mysecrets.audio.get(media_name,None)
    elif media_type == "sticker":
        media_id = mysecrets.stickers.get(media_name,None)
    return media_id

def reply_with_emoji(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type":"individual",
            "to": number,
            "type": "reaction",
            "reaction":{
                "message_id": messageId,
                "emoji": emoji,
            }
        }
    )
    return data    

def reply_text(number,messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to":number,
            "context": {"message_id": messageId},
            "type": "text",
            "text":{
                "body": text
            }
        }
    )
    print('data', data)
    return data

def mark_read(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId

        }
    )
    print('data', data)
    return data

def chatbot_admin(text, number, messageId, name):
    text = text.lower()
    list = []

    mark_as_read = mark_read(messageId)
    list.append(mark_as_read)
    time.sleep(2)
    try:

        if "hello" in text:
            body = "Hello there!, I'm Bukky , Austine's special assistant, Austine is currently offline, Can i be of help today?"
            footer = "Austine Ebogu"
            options = ["Chat with me", "Call Austine?"]

            reply = button_reply_message(number, options, body, footer, "sed1", messageId)

            reply_reaction = reply_with_emoji(number, messageId, "😎" )
            print('reply', reply)
            print('reply_reaction', reply_reaction)

            list.append(reply_reaction)
            list.append(reply)
        
        elif "chat with me" in text:
            body = "You made the right choice, Ask me anything you will love to know about"
            footer = "Austine Ebogu"
            options = ["We can play a game?", "I can ask you a question"]

            reply = list_reply_message(number, options, body, footer, "sed2", messageId)

            reply_reaction = sticker_message(number, get_media_id("perro_traje", "sticker"))

            list.append(reply)
            list.append(reply_reaction )
        
        elif "we can play a game" in text:
            body = "Let's play a guess game? Guess an alphabet on my mind between A - E, Hint: It is a vowel"
            footer = "Austine Ebogu"
            options = ["I don't know 🤦‍♂️", "There's no vowel between them 🤷‍♀️"]

            reply = button_reply_message(number, options, body, footer, "sed3", messageId)

            reply_reaction = reply_with_emoji(number, messageId, "💖" )

            list.append(reply_reaction)
            list.append(reply)
        
        elif "i don't know" in text:
            # sticker = sticker_message(number, get_media_id("poyo_feliz", "sticker"))
            text_message = text_Message(number, "If you selected the second button, You could've won, Meanwhile take your gift for playing")
            # whatsapp_api(sticker)
            whatsapp_api(text_message)
            time.sleep(3)

            document = document_message(number, 'https://res.cloudinary.com/de8gwnof9/image/upload/v1692787659/Sme_header_photos/ijeml6jl9w6twhaiu3cw.jpg', "Reward ❤", "Your gift.jpg")
            whatsapp_api(document)
            time.sleep(3)

            body = "Thank you very much"
            footer = "Austine Ebogu"
            options = ["🌹Play again", "Call Austine🌹"]

            reply = button_reply_message(number, options, body, footer, "sed4", messageId)

            reply_reaction = reply_with_emoji(number, messageId, "💖" )

            list.append(reply_reaction)
            list.append(reply)
        
        elif "play again" in text:
            body = "Let's play a guess game? Guess an alphabet on my mind between A - E, Hint: It is a vowel"
            footer = "Austine Ebogu"
            options = ["I don't know 🤦‍♂️", "There's no vowel 🤷‍♀️"]

            reply = button_reply_message(number, options, body, footer, "sed5", messageId)

            reply_reaction = reply_with_emoji(number, messageId, "💖" )

            list.append(reply_reaction)
            list.append(reply)
        
        elif "there's no vowel between them" in text:
            body = "You're right, That was not hard, Your Turn?"
            footer = "Austine Ebogu"
            options = ["Play Another One 👏", "I don't want to play 😒"]

            reply = list_reply_message(number, options, body, footer, "sed6", messageId)
            list.append(reply)

        elif "i don't want to play" in text:
            body = "_Austine will be with you shortly_, *Bye for now* 👌"
            reply = text_Message(number, body)
            list.append(reply)

        else:
            data = text_Message(number, "Invalid Selection, Choose from the option or re-type verbatim")
            list.append(data)
            print(data)

        for data in list:
            whatsapp_api(data)
    except Exception as e:
         print("Unhandled error:", str(e))

