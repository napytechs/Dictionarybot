import json
import urllib
import os
from difflib import get_close_matches
from telebot import TeleBot,types
from flask import Flask,request 
DICTIONARY = urllib.request.urlopen("https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json")
file = ''
for i in DICTIONARY:
    file+=i.decode()
TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
DICTIONARY = json.loads(file)   
bot = TeleBot(TOKEN)
app = Flask(__name__)
@bot.message_handler(commands=['start'],chat_types=['private'])
def start(msg):
    bot.send_message(msg.chat.id,"👋 Hey there {name} i am dictionary bot. I have more than 100k words\n"
                                 "✨ send me any english word, i will send you the definition then.\n"
                                 "🌷 I wish good time to here :)".format(name=msg.from_user.first_name))
@bot.message_handler(chat_types=['private'])
def on_message(msg):
    word = msg.text
    keys = [key for key in DICTIONARY]
    match = get_close_matches(word,keys)
    if word in keys:
        bot.send_message(msg.chat.id,'<code>{text}</code>'.format(text=DICTIONARY[word]),parse_mode='html')
    elif match:
        vals = []
        text = "_Did you mean ?_\n"
        btn = types.InlineKeyboardMarkup(row_width=1)
        if isinstance(match,list):
            print(len(match))
            if len(match) > 1:
                for i in range(len(match)):
                    vals.append(types.InlineKeyboardButton(text=match[i],callback_data=match[i]))
                    text+=f"_{str(i+1)}_ {match[i]}\n\n"
                btn.add(*vals)
        else:
            text+=match
            btn.add(types.InlineKeyboardButton(text="Yes ✅ ",callback_data=match),types.InlineKeyboardButton(text="No ❌ ",callback_data="no"))
        bot.send_message(msg.chat.id,text,reply_markup=btn,parse_mode="Markdown")
    else:
        bot.send_message(msg.chat.id,"Sorry this word doesn't exist my word list :(\nplease try another word...")
@bot.callback_query_handler(func=lambda call:True)
def on_callback(call):
    if call.data == "no":
        bot.send_message(call.message.chat.id,"Sorry this word doesn't exist my word list :(\nplease try another word...")
    elif call.data == call.data:
        bot.send_message(call.message.chat.id,f"<code>{DICTIONARY[call.data]}</code>",parse_mode='html')
    bot.delete_message(call.message.chat.id,call.message.message_id)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    print("Webhook Connected.....")
    return "!", 200



while True:
    try:
        print("Bot is running")
        app.run(host="localhost",port=9999)
    except:continue
    
    
