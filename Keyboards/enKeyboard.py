from telebot import types

def MainMenuKeyboard():
    Keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    MenuButton1 = types.KeyboardButton('Find picture')
    MenuButton2 = types.KeyboardButton('Change language')
    Keyboard.add(MenuButton1, MenuButton2)
    return Keyboard

def backButton():
    Keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    MenuButton1 = types.KeyboardButton('Back')
    Keyboard.add(MenuButton1)
    return Keyboard