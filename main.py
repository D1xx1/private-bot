'''This is main file of bot. Use settings.py to access bot.'''
from icrawler.builtin import GoogleImageCrawler as gic
from settings import token, quantity
from telebot import TeleBot
import Localisation.en as en
import Localisation.ru as ru
import Localisation.kz as kz
import Keyboards.ruKeyboard as rukb
import Keyboards.startKeyboard as stkb
import Keyboards.enKeyboard as enkb
import sqlite3
import os
import random
import datetime

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
        cursor.execute(f"SELECT chat_id FROM users WHERE chat_id = '{chat_id}'")
        if cursor.fetchone() is None:
            bot.send_message(chat_id, 'Приветствую! Для начала нужно выбрать желаемый язык.', reply_markup=stkb.startKeyboard())
            cursor.execute(f"INSERT INTO users VALUES (?,?,?,?)", (chat_id,'default','ru',0))
            db.commit()
            bot.register_next_step_handler_by_chat_id(chat_id, language)
        else:
            cursor.execute(f"SELECT * FROM users WHERE chat_id = '{message.from_user.id}'")
            rows = cursor.fetchone()
            lang = rows['language']
            if lang == 'ru':
                bot.send_message(chat_id, 'Это основное меню.', reply_markup=rukb.MainMenuKeyboard())
                bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)
            if lang == 'en':
                bot.send_message(chat_id, 'Main menu.', reply_markup=enkb.MainMenuKeyboard())
                bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)
    else:
        bot.send_message(chat_id, '/start')

def language(message):
    command = message.text
    chat_id = message.from_user.id
    if command == 'Русский':
        bot.send_message(chat_id, ru.changeLanguage)
        bot.send_message(chat_id, 'Это основное меню.', reply_markup=rukb.MainMenuKeyboard())
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?",('ru',chat_id))
        db.commit()
        bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)

    if command == 'English':
        bot.send_message(chat_id, en.changeLanguage, reply_markup=enkb.MainMenuKeyboard())
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?", ('en',chat_id))
        db.commit()
        bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)

    if command == 'Казахский':
        bot.send_message(chat_id, kz.startMessage)
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?", ('kz',chat_id))
        db.commit()
        data = cursor.fetchone()
        print(data)

def ruMainMenu(message):
    chat_id = message.from_user.id
    command = message.text
    if command == 'Поиск картинок':
        bot.send_message(chat_id, 'Поиск картинок по запросу. Введите в чат любой запрос и бот найдет для Вас картинку.', reply_markup=rukb.backButton())
        bot.register_next_step_handler_by_chat_id(chat_id, pictFinder)
    elif command == 'Сменить язык':
        bot.send_message(chat_id, 'Выберите язык.', reply_markup=stkb.startKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, language)
    else:
        bot.send_message(chat_id, ru.menuAction)
        bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)


def enMainMenu(message):
    chat_id = message.from_user.id
    command = message.text
    if command == 'Find picture':
        bot.send_message(chat_id, 'pictFinder', reply_markup=enkb.backButton())
        bot.register_next_step_handler_by_chat_id(chat_id, pictFinder)
    elif command == 'Change language':
        bot.send_message(chat_id, 'Choose language.', reply_markup=stkb.startKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, language)
    else:
        bot.send_message(chat_id,'Choose comand from keyboard.')
        bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)

def pictFinder(message):
    command = message.text
    chat_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE chat_id = '{message.from_user.id}'")
    rows = cursor.fetchone()
    lang = rows['language']
    if command == 'Назад':
        bot.send_message(chat_id, ru.mainMenu, reply_markup=rukb.MainMenuKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)
    elif command == 'Back':
        bot.send_message(chat_id, en.mainMenu, reply_markup=enkb.MainMenuKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)
    else:
        try:
            if not os.path.isdir('Downloads'):
                os.mkdir('Downloads')
            directory = f'{os.getcwd()}\Downloads\{chat_id}'
            google_crawler = gic(storage={'root_dir':f'{directory}'})
            if lang == 'ru':
                bot.send_message(chat_id, ru.waitMessage, reply_markup=stkb.removeKeyboard())
            if lang == 'en':
                bot.send_message(chat_id, en.waitMessage, reply_markup=stkb.removeKeyboard())
            google_crawler.crawl(keyword=command, max_num=quantity)
            with open(os.path.join(directory, random.choice(os.listdir(directory))),'rb') as photo:
                photo = photo
                if lang == 'ru':
                    bot.send_photo(chat_id, photo, reply_to_message_id=message.id, reply_markup=rukb.MainMenuKeyboard())
                    bot.register_next_step_handler_by_chat_id(chat_id, ruMainMenu)
                if lang == 'en':
                    bot.send_photo(chat_id, photo, reply_to_message_id=message.id, reply_markup=enkb.MainMenuKeyboard())
                    bot.register_next_step_handler_by_chat_id(chat_id, enMainMenu)
            today = datetime.datetime.today()
            newName = f'{chat_id}_{today.strftime(f"%Y-%m-%d-%H.%M.%S")}_{command}'
            os.chdir('Downloads')
            os.rename(f'{chat_id}', newName)
            os.chdir(mainDir)
        except FileExistsError:
            if lang == 'ru':
                bot.send_message(chat_id, ru.waitMessage)
            if lang == 'en':
                bot.send_message(chat_id, en.waitMessage)

bot.polling(True)