'''This is main file of bot. Use settings.py to access bot.'''
try:
    import Localisation.ru as ru
    import Localisation.kz as kz
    import Keyboards.ruKeyboard as rukb
    import Keyboards.startKeyboard as stkb
    import Keyboards.enKeyboard as enkb
except ModuleNotFoundError as error:
    input(f'Возникла ошибка: {error}\nОтсутствует файл локалицации.\nНажмите Enter для выхода из программы.')
    quit()
print('Файлы локализации успешно закружены!')
from icrawler.builtin import GoogleImageCrawler as gic
from telebot import TeleBot
import Localisation.en as en
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

if os.path.isfile('settings.txt') == False:
    with open('settings.txt','w') as config:
        config.write(input('Введите токен: '))
        
with open('settings.txt', 'r') as config:
    config = config.readlines()
    if len(config) == 1:
        global token
        token = config[0].strip()
        
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
                bot.send_message(chat_id, ru.mainMenu, reply_markup=rukb.MainMenuKeyboard())
            if lang == 'en':
                bot.send_message(chat_id, en.mainMenu, reply_markup=enkb.MainMenuKeyboard())
            bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)
    else:
        bot.send_message(chat_id, '/start')

def language(message):
    command = message.text
    chat_id = message.from_user.id
    if command == 'Русский':
        bot.send_message(chat_id, ru.changeLanguage, reply_markup=rukb.MainMenuKeyboard())
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?",('ru',chat_id))
        db.commit()
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

    elif command == 'English':
        bot.send_message(chat_id, en.changeLanguage, reply_markup=enkb.MainMenuKeyboard())
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?", ('en',chat_id))
        db.commit()
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

    elif command == 'Казахский':
        bot.send_message(chat_id, kz.startMessage)
        cursor.execute("UPDATE users SET language = ? WHERE chat_id = ?", ('kz',chat_id))
        db.commit()
        data = cursor.fetchone()

    else:
        bot.send_message(chat_id, 'Выберите язык.')
        bot.register_next_step_handler_by_chat_id(chat_id, language)

def mainMenu(message):
    chat_id = message.from_user.id
    command = message.text
    cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
    rows = cursor.fetchone()
    status = rows['status']
    lang = rows['language']
    cash = rows['cash']

    if (command == 'Поиск картинок' or command == 'Find picture'):
        if lang == 'ru':
            bot.send_message(chat_id, ru.pictFinderStart, reply_markup=rukb.backButton())
        elif lang == 'en':
            bot.send_message(chat_id, en.pictFinderStart, reply_markup=enkb.backButton())
        bot.register_next_step_handler_by_chat_id(chat_id, pictFinder)

    elif (command == 'Сменить язык' or command == 'Change language'):
        if lang == 'ru':
            bot.send_message(chat_id, ru.chooseLanguage, reply_markup=stkb.startKeyboard())
        elif lang == 'en':
            bot.send_message(chat_id, en.chooseLanguage, reply_markup=stkb.startKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, language)

    elif (command == 'Статус' or command == 'Status'):
        if lang == 'ru':
            bot.send_message(chat_id, ru.status+status)
        if lang == 'en':
            bot.send_message(chat_id, en.status+status)
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

    elif command == '/admin':
        '''AdminPanel'''
        if status == 'admin':
            bot.send_message(chat_id, 'Переход в админ-панель...', reply_markup=rukb.adminKeyboard())
            bot.register_next_step_handler_by_chat_id(chat_id, adminPanel)
        else:
            bot.send_message(chat_id, 'У вас нет доступа!')
            bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

    else:
        if lang == 'ru':
            bot.send_message(chat_id, ru.menuAction)
        elif lang == 'en':
            bot.send_message(chat_id, en.menuAction)
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

def pictFinder(message):
    command = message.text
    chat_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE chat_id = '{message.from_user.id}'")
    rows = cursor.fetchone()
    lang = rows['language']

    if (command == 'Назад' or command == 'Back'):
        if lang == 'ru':
            bot.send_message(chat_id, ru.mainMenu, reply_markup=rukb.MainMenuKeyboard())
        if lang == 'en':
            bot.send_message(chat_id, en.mainMenu, reply_markup=enkb.MainMenuKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

    else:
        try:
            if not os.path.isdir('Downloads'):
                os.mkdir('Downloads')
            today = datetime.datetime.today()
            newName = f'{chat_id}_{today.strftime(f"%Y-%m-%d-%H.%M.%S")}_{command}'
            directory = f'{os.getcwd()}\Downloads\{chat_id}_{today.strftime(f"%Y-%m-%d-%H.%M.%S")}'
            google_crawler = gic(storage={'root_dir':f'{directory}'})
            if lang == 'ru':
                bot.send_message(chat_id, ru.waitMessage, reply_markup=stkb.removeKeyboard())
            if lang == 'en':
                bot.send_message(chat_id, en.waitMessage, reply_markup=stkb.removeKeyboard())
            google_crawler.crawl(keyword=command, max_num=10)
            with open(os.path.join(directory, random.choice(os.listdir(directory))),'rb') as photo:
                photo = photo
                if lang == 'ru':
                    bot.send_photo(chat_id, photo, reply_to_message_id=message.id, reply_markup=rukb.MainMenuKeyboard())
                if lang == 'en':
                    bot.send_photo(chat_id, photo, reply_to_message_id=message.id, reply_markup=enkb.MainMenuKeyboard())
                bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)
            os.chdir('Downloads')
            os.rename(f'{chat_id}_{today.strftime(f"%Y-%m-%d-%H.%M.%S")}', newName)
            os.chdir(mainDir)
        except FileExistsError:
            if lang == 'ru':
                bot.send_message(chat_id, ru.waitMessage)
            if lang == 'en':
                bot.send_message(chat_id, en.waitMessage)
            bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)

# AdminPanel нужно доработать
# =================================================================================================
def adminPanel(message):
    command = message.text
    chat_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
    rows = cursor.fetchone()
    lang = rows['language']
    if (command == 'Назад' or command == 'Back'):
        if lang == 'ru':
            bot.send_message(chat_id, ru.mainMenu, reply_markup=rukb.MainMenuKeyboard())
        elif lang == 'en':
            bot.send_message(chat_id, en.mainMenu, reply_markup=enkb.MainMenuKeyboard())
        bot.register_next_step_handler_by_chat_id(chat_id, mainMenu)
    elif (command == 'Добавить' or command == 'Add'):
        if lang == 'ru':
            bot.send_message(chat_id, 'Soon...')
        elif lang == 'en':
            bot.send_message(chat_id, 'Soon...')
        bot.register_next_step_handler_by_chat_id(chat_id, adminPanel)
    else:
        bot.send_message(chat_id, 'Не выполнено...')
        bot.register_next_step_handler_by_chat_id(chat_id, adminPanel)
# ================================================================================================

bot.polling(True)
