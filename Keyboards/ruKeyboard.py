from telebot import types

def MainMenuKeyboard():
    Keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    MenuButton1 = types.KeyboardButton('Поиск картинок')
    MenuButton2 = types.KeyboardButton('Сменить язык')
    Keyboard.add(MenuButton1, MenuButton2)
    return Keyboard

def backButton():
    Keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    MenuButton1 = types.KeyboardButton('Назад')
    Keyboard.add(MenuButton1)
    return Keyboard
    