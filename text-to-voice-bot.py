import telebot
from gtts import gTTS
import os
import json


bot_token = '' #Bot token 
admin_id = '' # admin id
bot = telebot.TeleBot(bot_token)


user_data_file = 'user_data.json'
if not os.path.exists(user_data_file):
    with open(user_data_file, 'w') as file: # if any error in file just make file like this name and replace the w to a
        json.dump({}, file)

@bot.message_handler(func=lambda message: True)
def text_to_voice(message):
    text = message.text
    

    language_code = detect_language_code(text)
    

    tts = gTTS(text, lang=language_code)
    

    audio_file = "voice.mp3"
    tts.save(audio_file)
    

    with open(audio_file, 'rb') as audio:
        bot.send_voice(message.chat.id, audio)
    

    os.remove(audio_file)

    update_user_data(message)

    send_user_info_to_admin(message)

def detect_language_code(text):
    
    if any(char in 'اأبتثجحخدذرزسشصضطظعغفقكلمنهوي' for char in text):
        return "ar"
    else:

        return "en"

def update_user_data(message):
    user_id = message.from_user.id
    

    with open(user_data_file, 'r') as file:
        user_data = json.load(file)

    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            'username': message.from_user.username,
            'used_count': 0
        }
    else:
    	pass
    user_data[str(user_id)]['used_count'] += 1
    with open(user_data_file, 'w') as file:
        json.dump(user_data, file)

def send_user_info_to_admin(message):
    
    with open(user_data_file, 'r') as file:
        user_data = json.load(file)
    
 
    user_count = len(user_data)
    user_id = message.from_user.id
    us = message.from_user.username

    bot.send_message(admin_id, f"Number of users who used the bot: {user_count} \n username : @{us} ch : @rhpwhx dev : @MrRaph")


if __name__ == "__main__":
    bot.infinity_polling()
