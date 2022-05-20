from telebot import types
from telebot.types import KeyboardButton

def keyboard_remove():

    markup = types.ReplyKeyboardRemove()
    return markup

def keyboard_back():

    rest = ['Назад']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    return markup

def keyboard_staff():

    rest = ['🤵‍♂️Официант','👩‍💼Администратор','Назад']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    return markup

def keyboard_staff_go():

    rest = ['📕Принести меню','💵Принести счёт', '🍻Сделать заказ', '✉️Написать сообщение']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    markup.add('Назад')
    return markup

def keyboard_go():

    rest = ['🛎️Вызвать персонал','🗓Забронировать стол', '📕Меню', '✍️Написать отзыв']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    markup.add('🔥Акции','🎸Концерты')
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    return markup
    
def keyboard_menu():

    rest = ['🥪Еда', '🍻Напитки']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    markup.add('Назад')
    return markup

def keyboard_send_contact():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Отправить телефон", request_contact=True))
    markup.add("Назад")
    return markup