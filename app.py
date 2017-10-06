# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


# -*- coding: utf-8 -*-
from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer'
)

chatbot.train([
    "Hi, can I help you?",
    "Sure, I'd to book a flight to Iceland.",
    "Your flight has been booked."
])
    
# 建立一個 ChatBot 物件
#chatbot = ChatBot("Ron Obvious")
#chatbot = ChatBot(
#   'Johnson Test' ,
#    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
#)

# 基於英文的自動學習套件
#chatbot.train("chatterbot.corpus.english")

#chatbot.train("chatterbot.corpus.chinese.greetings")

# 與 ChatBot 對話，並且取得回應
# chatbot.get_response("Hello, how are you today?")

#from chatterbot.trainers import ListTrainer



#chatbot.set_trainer(ListTrainer)
#chatbot.train(conversation)




app = Flask(__name__)

line_bot_api = LineBotApi('Renikv7AVXUcdHSeAlAISUTMMIi/pnGSDccD7jWL7vMWOUE75iBF/6rPQNuj3iWjoWfCTAIncsIdwzFq/Oy9RC5shrlPbgOR271tDSVRDbnmHzGA8CyS4pLBEuHjSzaKSxiIwv5ULvfNuajDzTa0CQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('4f0930a748a24428e8b089842d6f5c6d') #Your Channel Secret

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):   
    #text2 = '0'
    text = event.message.text #message from user
    bot_response = chatbot.get_response(text)
    #if bot_response == '1':
    #    text2 = 'ffffff'
    #else : 
    #    text2 = 'kerker'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= bot_response)) #reply the same message from user
   
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
