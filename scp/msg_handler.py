from datetime import datetime
import glob, os
from scp import keyboard, db
from config import timeout_seconds

def sends_photo(bot, message, photo):
    for filename in sorted(glob.glob(photo)):
        with open(os.path.join(os.getcwd(), filename), 'rb') as f:
            photo_s = open(filename, 'rb')       
            bot.send_photo(message.chat.id, photo_s)

def sends_doc(bot, message, doc):
    docs = open(doc, 'rb')
    bot.send_document(message.chat.id, docs)

def safes_state(bot, message, state):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data[state] = message.text

def send_msg_call(bot, message, msg_for_channel, chat_id, msg_for_user):
    bot.send_message(chat_id, msg_for_channel, parse_mode='HTML')
    bot.send_message(message.chat.id, msg_for_user, reply_markup=keyboard.keyboard_go())
    bot.delete_state(message.from_user.id, message.chat.id)

def new_user_func(message):
    if not db.if_user_exists(message.chat.id):
        db.new_user(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)

def new_user_func_noname(message):
    if not db.if_user_exists(message.chat.id):
        db.new_user(message.chat.id, message.chat.id, message.from_user.first_name, message.from_user.last_name)

def update_timeout(message):
    timeouts = datetime.now()
    db.update_timeout_on(timeouts, message.chat.id)

def timeout_check(message):
    now = datetime.now()
    if db.get_timeout(message.chat.id) == 0:        
        return True
    else:
        if (now-datetime.strptime(db.get_timeout(message.chat.id),"%Y-%m-%d %H:%M:%S.%f")).seconds < timeout_seconds:
            return False
        else:
            return True

def ban_user(bot, message):
    login = (message.text.strip('/ban '))
    if db.if_user_ban(login) == 0:
        db.update_ban(login)
        bot.send_message(message.chat.id, 'Добавил в черный список: ' + str(message.chat.id) + ' - ' + login, reply_markup=keyboard.keyboard_go())
    else:
        bot.send_message(message.chat.id, 'Этот персонаж в черном списке', reply_markup=keyboard.keyboard_go())
    
def unban_user(bot, message):
    login = (message.text.strip('/unban '))
    if db.if_user_ban(login) == 1:
        db.update_unban((login))
        bot.send_message(message.chat.id, 'Этот персонаж '+ login +' удален', reply_markup=keyboard.keyboard_go())
    else:
        bot.send_message(message.chat.id, 'Eго нет в черном списке', reply_markup=keyboard.keyboard_go())

def banlist_user(bot, message):
    msg = 'BanList:\n'
    msg1 = ''
    banlist = db.banlist()
    for key,value in banlist:            
        msg1 = msg1 + str(key) + ' - ' + value +'\n'
    bot.send_message(message.chat.id, msg + msg1 , reply_markup=keyboard.keyboard_remove())