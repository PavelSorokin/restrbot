import config as var
import telebot
from telebot import custom_filters
from datetime import datetime
from art import tprint
from scp import msg_handler, keyboard, classes, db
import logging
from logging.handlers import RotatingFileHandler

def main():
    log = logging.getLogger("bots.doc")
    log.setLevel(logging.INFO)
    handler = RotatingFileHandler('./log/main.log', maxBytes=10000, backupCount=10)
    log_format = f"%(asctime)s | [%(levelname)s] | %(name)s | (%(filename)s).%(funcName)s(%(lineno)d) | %(message)s"
    handler.setFormatter(logging.Formatter(log_format))
    log.addHandler(handler)
    print("БиржаBot is started!")
    tprint('BeerzhaBot')

    bot = telebot.TeleBot(var.main_bot_token, state_storage=var.state_storage)

    @bot.message_handler(commands=['help'])
    def help_cmd(message):
        bot.send_message(message.chat.id, classes.cls_msg().msg_help(), reply_markup=keyboard.keyboard_remove())

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        if message.from_user.username is None:
            bot.send_message(message.chat.id, classes.cls_msg().msg_start(''), reply_markup=keyboard.keyboard_go())
            msg_handler.new_user_func_noname(message)
        else:
            bot.send_message(message.chat.id, classes.cls_msg().msg_start(message.chat.first_name), reply_markup=keyboard.keyboard_go())
            msg_handler.new_user_func(message)

    @bot.message_handler(state="*", commands=['cancel'])
    def cancel_cmd(message):
        bot.send_message(message.chat.id, classes.cls_msg().msg_cancel(), reply_markup=keyboard.keyboard_remove())
        bot.delete_state(message.from_user.id, message.chat.id) 

    @bot.message_handler(commands=['ban'],func=lambda message: message.chat.id in var.admins)
    def ban(message):
        msg_handler.ban_user(bot, message)

    @bot.message_handler(commands=['banlist'],func=lambda message: message.chat.id in var.admins)   
    def banlist(message):
        msg_handler.banlist_user(bot, message)

    @bot.message_handler(commands=['unban'],func=lambda message: message.chat.id in var.admins)   
    def unban(message):
        msg_handler.unban_user(bot, message)

    @bot.message_handler(state="*", func=lambda message: message.text == "Назад")
    def back_to_start(message):
        bot.send_message(message.chat.id, classes.cls_msg().msg_back_menu(), reply_markup=keyboard.keyboard_go())
        bot.delete_state(message.from_user.id, message.chat.id) 

    @bot.message_handler(state=classes.cls_call_staff.desc)
    def to_desc_msg(message):
        msg_handler.safes_state(bot, message, 'desc')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg_for_channel = classes.cls_msg().msg_call_service(data['table'], message.chat.username, data['desc'], message.chat.first_name)
            msg_for_user = classes.cls_msg().msg_call_service_foruser(data['table'])
        msg_handler.update_timeout(message)
        msg_handler.send_msg_call(bot, message, msg_for_channel, var.bot_chat_id, msg_for_user)
        log.info('Send Call Staff' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )

    @bot.message_handler(state=classes.cls_call_staff.table, is_digit=False)
    def noint(message):
        bot.send_message(message.chat.id, classes.cls_msg().msg_table_num_noint(), parse_mode='Markdown', reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.cls_call_staff.table, message.chat.id) 

    @bot.message_handler(state=classes.cls_call_staff.table, is_digit=True)
    def yesint(message):
        msg_handler.safes_state(bot, message, 'table')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            check_jobs = data['jobs']
            msg_for_channel = classes.cls_msg().msg_call_service(data['table'], message.chat.username, data['jobs'], message.chat.first_name)
            msg_for_user = classes.cls_msg().msg_call_service_foruser(data['table'])
        if check_jobs == '✉️Написать сообщение':
            bot.send_message(message.chat.id, classes.cls_msg().msg_free_form(), reply_markup=keyboard.keyboard_back())
            bot.set_state(message.from_user.id, classes.cls_call_staff.desc, message.chat.id)
        else:
            msg_handler.update_timeout(message)
            msg_handler.send_msg_call(bot, message, msg_for_channel, var.bot_chat_id, msg_for_user)
            log.info('Send Call Staff' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )

    @bot.message_handler(state=classes.cls_call_admin.desc)
    def admin_desc(message):
        msg_handler.safes_state(bot, message, 'desc')
        bot.send_message(message.chat.id, classes.cls_msg().msg_table_num(), reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.cls_call_admin.table, message.chat.id) 

    @bot.message_handler(state=classes.cls_call_admin.table, is_digit=False)
    def admin_noint(message):
        bot.send_message(message.chat.id, classes.cls_msg().msg_table_num_noint(), parse_mode='Markdown', reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.cls_call_admin.table, message.chat.id)

    @bot.message_handler(state=classes.cls_call_admin.table, is_digit=True)
    def admin_yesint(message):
        msg_handler.safes_state(bot, message, 'table')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg_for_channel = classes.cls_msg().msg_call_service(data['table'], message.chat.username, data['desc'], message.chat.first_name)
            msg_for_user = classes.cls_msg().msg_call_service_foruser(data['table'])
        msg_handler.update_timeout(message)
        msg_handler.send_msg_call(bot, message, msg_for_channel, var.bot_chat_id_admin, msg_for_user)
        log.info('Send Call Admin' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )
    @bot.message_handler(state=classes.cls_feedback.desc)
    def feedback_send(message):
        msg_handler.safes_state(bot, message, 'desc')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg_for_channel = classes.cls_msg().msg_feedback_mail(message.chat.first_name,message.chat.username,data['desc'])
            msg_for_user = classes.cls_msg().msg_feedback_foruser()
        msg_handler.send_msg_call(bot, message, msg_for_channel, var.bot_chat_id_feedback, msg_for_user)
        log.info('Send Feedback' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )
    @bot.message_handler(state=classes.cls_reserved.name)
    def reserved_q_name(message):
        msg_handler.safes_state(bot, message, 'name')
        bot.send_message(message.chat.id, classes.cls_msg().msg_reserved_que(), parse_mode='Markdown', reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.cls_reserved.desc, message.chat.id)  
        
    @bot.message_handler(state=classes.cls_reserved.desc)
    def reserved_q_contact(message):
        msg_handler.safes_state(bot, message, 'desc')
        bot.send_message(message.chat.id, classes.cls_msg().msg_reserver_phone(), reply_markup=keyboard.keyboard_send_contact())

    @bot.message_handler(content_types=['contact'])
    def reserved_send(message):
        if message.contact is not None:       
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                msg_for_channel = classes.cls_msg().msg_reserved(message.contact.first_name, message.chat.username, data['name'], message.contact.phone_number,data['desc'])
                msg_for_user = classes.cls_msg().msg_reserved_foruser()
            
            msg_handler.send_msg_call(bot, message, msg_for_channel, var.bot_chat_id_admin, msg_for_user)
            db.update_phone(message.chat.id, message.contact.phone_number)
            log.info('Send Call Reserved' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )
            
                
    @bot.message_handler(state="*", func=lambda message: message.chat.type == 'private', content_types=['text'])
    def mesg_handler(message):
        if db.if_user_ban_2(message.chat.id) == 1:
            bot.send_message(message.chat.id, classes.cls_msg().msg_blacklist() , reply_markup=keyboard.keyboard_remove())
        else:
            if message.text == 'Назад':
                bot.send_message(message.chat.id, classes.cls_msg().msg_back_menu(), reply_markup=keyboard.keyboard_go())
                bot.delete_state(message.from_user.id, message.chat.id) 
            elif message.text == '🔥Акции':
                msg_handler.sends_photo(bot, message, var.sales_files)
                log.info('Send Sales' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )
            elif message.text == '🎸Концерты':
                msg_handler.sends_photo(bot, message, var.concert_files)
                log.info('Send Concert' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )
            elif message.text == '📕Меню':
                bot.send_message(message.chat.id, 'Выбери меню',reply_markup=keyboard.keyboard_menu())

            elif message.text == '🥪Еда':
                msg_handler.sends_doc(bot, message, var.menu_file)
                log.info('Send Food' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )

            elif message.text == '🍻Напитки':
                msg_handler.sends_doc(bot, message, var.bar_file)
                log.info('Send Bar' + ' | '+ str(message.chat.id) +' | ' + message.chat.username +' | '+ message.chat.first_name )

            elif message.text == '✍️Написать отзыв':
                bot.send_message(message.chat.id, classes.cls_msg().msg_feedback(), parse_mode='Markdown', reply_markup=keyboard.keyboard_back())
                bot.set_state(message.from_user.id, classes.cls_feedback.desc, message.chat.id)

            elif message.text == '🛎️Вызвать персонал':
                if msg_handler.timeout_check(message) == False:
                    bot.send_message(message.chat.id, classes.cls_msg().msg_spam(), reply_markup=keyboard.keyboard_go())
                    msg_handler.sends_doc(bot,message,var.timeout_gif)
                else:
                    bot.delete_state(message.from_user.id, message.chat.id)
                    bot.send_message(message.chat.id, classes.cls_msg().msg_staff(), reply_markup=keyboard.keyboard_staff())

            elif message.text == '🤵‍♂️Официант':  
                bot.send_message(message.chat.id, classes.cls_msg().msg_staff_jobs() , reply_markup=keyboard.keyboard_staff_go())
                bot.set_state(message.from_user.id, classes.cls_call_staff.jobs, message.chat.id)

            elif message.text in ['📕Принести меню','💵Принести счёт', '🍻Сделать заказ', '✉️Написать сообщение']:
                msg_handler.safes_state(bot, message, 'jobs')
                bot.send_message(message.chat.id, classes.cls_msg().msg_table_num(), reply_markup=keyboard.keyboard_back())
                bot.set_state(message.from_user.id, classes.cls_call_staff.table, message.chat.id)  

            elif message.text == '👩‍💼Администратор':  
                bot.send_message(message.chat.id, classes.cls_msg().msg_staff_admin(), reply_markup=keyboard.keyboard_back())
                bot.set_state(message.from_user.id, classes.cls_call_admin.desc, message.chat.id)

            elif message.text == '🗓Забронировать стол':
                bot.send_message(message.chat.id,classes.cls_msg().msg_reserved_name(), reply_markup=keyboard.keyboard_back())
                bot.set_state(message.from_user.id, classes.cls_reserved.name, message.chat.id) 
            else:
                start_cmd(message)
        
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())

    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    main()