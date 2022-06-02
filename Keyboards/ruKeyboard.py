from telebot import types

def MainMenuKeyboard():
    Keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    Button1 = types.KeyboardButton('Поиск картинок')
    Button2 = types.KeyboardButton('Сменить язык')
    Button3 = types.KeyboardButton('Статус')
    Keyboard.add(Button1, Button2, Button3)
    return Keyboard

def backButton():
    Keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Button1 = types.KeyboardButton('Назад')
    Keyboard.add(Button1)
    return Keyboard

def adminKeyboard():
    Keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    Button1 = types.KeyboardButton('Добавить')
    Button2 = types.KeyboardButton('Назад')
    Keyboard.add(Button1,Button2)
    return Keyboard
    