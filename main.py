'''This is main file of bot. Use settings.py to access bot.'''
from settings import token
from telebot import types
from telebot import TeleBot
import Localisation.en as en
import Localisation.ru as ru
import Localisation.kz as kz
import sqlite3
import os

mainDir = os.getcwd()
if not os.path.isdir('UserInfo'):
    os.mkdir('UserInfo')
''' DataBase Creation'''
db = sqlite3.connect('UserInfo/userInfo.db', check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    chat_id INT PRIMARY KEY,
    status VARCHAR,
    menuPage INT,
    language VARCHAR,
    cash BIGINT
)''')
db.commit()

'''Start Keyboard'''
startKeyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
removeKeyboard = types.ReplyKeyboardRemove()
startButton1 = types.KeyboardButton('Русский',)
startButton2 = types.KeyboardButton('English')
startKeyboard.add(startButton1, startButton2)

'''Main menu RU buttons'''
ruKeyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
ruMenuButton1 = types.KeyboardButton('Поиск картинок')
ruMenuButton2 = types.KeyboardButton('Сменить язык')
ruKeyboard.add(ruMenuButton1, ruMenuButton2)

'''BOT Code'''
bot = TeleBot(token)
@bot.message_handler(content_types=['text'])
def start(message):
    command = message.text
    chat_id = message.from_user.id
    if command == '/start':
        cursor.execute(f"SELECT chat_id, language FROM users WHERE chat_id = '{message.from_user.id}'")
        if cursor.fetchone() is None:
            bot.send_message(chat_id, 'Учетная запись создана.')
            bot.send_message(chat_id, 'Приветствую! Для начала нужно выбрать желаемый язык. Выбери желаемый язык на клавиатуре ниже.', reply_markup=startKeyboard)
            cursor.execute(f"INSERT INTO users VALUES (?,?,?,?,?)", (chat_id,'default',0,'ru',0))
            db.commit()
        else:
            cursor.execute(f"SELECT * FROM users WHERE chat_id = '{message.from_user.id}'")
            rows = cursor.fetchone()
            lang = rows['language']
            if lang == 'ru':
                bot.send_message(chat_id, f'Ваша запись найдена.')
                bot.send_message(chat_id, 'Это основное меню.', reply_markup=ruKeyboard)
                bot.register_next_step_handler_by_chat_id(chat_id, mainMenuRu)

    if command == 'Русский':
        bot.send_message(chat_id, ru.changeLanguage, reply_markup=removeKeyboard)
        bot.send_message(chat_id, 'Это основное меню.', reply_markup=ruKeyboard)
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenuRu)

    if command == 'English':
        bot.send_message(chat_id, en.changeLanguage, reply_markup=removeKeyboard)

    if command == 'Казахский':
        bot.send_message(chat_id, kz.startMessage, reply_markup=removeKeyboard)

def mainMenuRu(message):
    chat_id = message.from_user.id
    command = message.text
    if command == 'Поиск картинок':
        bot.send_message(chat_id, 'Поиск картинок по запросу. Введите в чат любой запрос и бот найдет для Вас нартинку.', reply_markup=removeKeyboard)
    if command == 'Сменить язык':
        bot.send_message(chat_id, 'Выберите язык.', reply_markup=startKeyboard)

      
bot.polling(True)