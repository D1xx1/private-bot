from telebot import types

class RuKeyboard():
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

class EnKeyboard():
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

    def adminKeyboard():
        Keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        Button1 = types.KeyboardButton('Add')
        Button2 = types.KeyboardButton('Back')
        Keyboard.add(Button1,Button2)
        return Keyboard

class StartKeyboard():
    def startKeyboard():
        Keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        Button1 = types.KeyboardButton('Русский',)
        Button2 = types.KeyboardButton('English')
        Keyboard.add(Button1, Button2)
        return Keyboard

    def removeKeyboard():
        Keyboard = types.ReplyKeyboardRemove()
        return Keyboard
