'''This is main file of bot. Use settings.py to access bot.'''
from settings import token
from telebot import TeleBot
import Localisation.en as en
import Localisation.ru as ru
import Localisation.kz as kz
import Keyboards.ruKeyboard as rukb
import Keyboards.startKeyboard as stkb
import Keyboards.enKeyboard as enkb
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
            bot.send_message(chat_id, 'Приветствую! Для начала нужно выбрать желаемый язык. Выбери желаемый язык на клавиатуре ниже.', reply_markup=stkb.startKeyboard())
            cursor.execute(f"INSERT INTO users VALUES (?,?,?,?,?)", (chat_id,'default',0,'ru',0))
            db.commit()
        else:
            cursor.execute(f"SELECT * FROM users WHERE chat_id = '{message.from_user.id}'")
            rows = cursor.fetchone()
            lang = rows['language']
            page = rows['menuPage']
            if lang == 'ru':
                bot.send_message(chat_id, f'Ваша запись найдена.')
                bot.send_message(chat_id, 'Это основное меню.', reply_markup=rukb.MainMenuKeyboard())
                bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)
            if lang == 'en':
                bot.send_message(chat_id, 'Found your account.')
                bot.send_message(chat_id, 'This is main menu.', reply_markup=enkb.MainMenuKeyboard())
                bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)

    if command == 'Русский':
        bot.send_message(chat_id, ru.changeLanguage)
        bot.send_message(chat_id, 'Это основное меню.', reply_markup=rukb.MainMenuKeyboard())
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?",('ru',chat_id))
        db.commit()
        bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)
        data = cursor.fetchone()
        print(data)

    if command == 'English':
        bot.send_message(chat_id, en.changeLanguage, reply_markup=enkb.MainMenuKeyboard())
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?", ('en',chat_id))
        db.commit()
        data = cursor.fetchone()
        print(data)
        bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)

    if command == 'Казахский':
        bot.send_message(chat_id, kz.startMessage)
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?", ('kz',chat_id))
        db.commit()
        data = cursor.fetchone()
        print(data)
    else:
        bot.send_message(chat_id, '/start')

def ruMainMenu(message):
    chat_id = message.from_user.id
    command = message.text
    if command == 'Поиск картинок':
        bot.send_message(chat_id, 'Поиск картинок по запросу. Введите в чат любой запрос и бот найдет для Вас нартинку.', reply_markup=rukb.backButton)
    if command == 'Сменить язык':
        bot.send_message(chat_id, 'Выберите язык.', reply_markup=stkb.startKeyboard())

def enMainMenu(message):
    chat_id = message.from_user.id
    command = message.text
    if command == 'Find picture':
        bot.send_message(chat_id, 'pictFinder', reply_markup=enkb.backButton)
    if command == 'Change language':
        bot.send_message(chat_id, 'Choose language.', reply_markup=stkb.startKeyboard())

      
bot.polling(True)