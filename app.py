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

line_bot_api = LineBotApi('P+we2j4wXb1v9mkAc05nbbLgG/eR6xWJP9zC6ysOBe4UHIve81uvbLwx+qvNxL6U31BbSTSmccIjwuwBt0WG8bpIMpaeb9tq83L3XJh+kRAZUp1KpoOkSbv0MPFq9hQFQfPP4High409X9iZe6c3RgdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('8f1d406e2fc3b4a61bec51ba95751a1f') #Your Channel Secret

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
    text = event.message.text #message from user
    bot_response = chatbot.get_response(text)
    line_bot_api.reply_message(
     event.reply_token,
     TextSendMessage(text= "123")) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
