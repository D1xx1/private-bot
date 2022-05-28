from telebot import types

def startKeyboard():
    Keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    Button1 = types.KeyboardButton('Русский',)
    Button2 = types.KeyboardButton('English')
    startKeyboard.add(Button1, Button2)
    return Keyboard

def removeKeyboard():
    removeKb = types.ReplyKeyboardRemove()
    return removeKb