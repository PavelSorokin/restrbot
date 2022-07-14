from telebot.handler_backends import State, StatesGroup

class cls_call_staff(StatesGroup):
    jobs = State()
    table = State()
    desc = State()

class cls_call_admin(StatesGroup):
    table = State()
    desc = State()

class cls_reserved(StatesGroup):
    name = State()
    desc = State()

class cls_feedback(StatesGroup):
    desc = State()

class cls_msg():

    def msg_help(self):
        self.msg_help_txt = 'Привет, я чат-бот Паба Биржа!\nС помощь меня ты можешь:\n- посмотреть список акций, концертов и меню;\n- вызвать персонал;\n- оставить отзыв.\nЧтобы начать, отправь мне /start'
        return self.msg_help_txt

    def msg_start(self, first_name):
        self.first_name = first_name  
        self.msg_start_txt = 'Привет, {first_name}!\nЯ чат-бот Паба Биржа, чем я могу помочь?\nВыбери пункт меню ⬇️'.format(first_name=self.first_name)
        return self.msg_start_txt

    def msg_blacklist(self):
        self.msg_blacklist_txt = 'Вы в черном списке.\nУточните у администратора.'
        return self.msg_blacklist_txt

    def msg_back_menu(self):
        self.msg_back_menu_txt = 'Выход в главное меню 🙂'
        return self.msg_back_menu_txt

    def msg_cancel(self):
        self.msg_cancel_txt = 'Перезапуск бота, чтобы начать отправь /start'
        return self.msg_cancel_txt
    
    def msg_table_num(self):
        self.msg_table_num_txt = 'Отправь мне номер твоего столика ☺️'
        return self.msg_table_num_txt

    def msg_table_num_noint(self):
        self.msg_table_num_noint_txt = 'Напиши, пожалуйста, номер столика без букв, точек и пробелов.\nНомер можно посмотреть на столике или уточнить у официанта.\n*Пример:*\n1'
        return self.msg_table_num_noint_txt
    
    def msg_spam(self):
        self.msg_spam_txt = 'Отправлять сообщения персоналу можно не чаще, чем раз в минуту.\nНапиши, пожалуйста, чуть позже.'
        return  self.msg_spam_txt
    
    def msg_call_service(self,table_num, username, jobs,first_name):
        self.first_name = first_name
        self.username = username
        self.table_num = table_num
        self.jobs = jobs
        self.msg_call_service_txt = 'Стол №{table}\nСообщение: {jobs}\nКлиент: '.format(table=self.table_num,jobs=self.jobs) + self.first_name +' - <b>@' f"{self.username}" + '</b>'
        return self.msg_call_service_txt
    
    def msg_call_service_foruser(self,table_num):
        self.table_num = table_num
        self.msg_call_service_foruser_txt = "Cтол №{table}. Уведомление отправлено.".format(table=self.table_num)
        return self.msg_call_service_foruser_txt  

    def msg_error(self):
        self.msg_error_txt = 'Что то пошло не так, попробуй еще раз.' 
        return  self.msg_error_txt
    
    def msg_reserved_name(self):
        self.msg_reserved_name_txt = 'Напиши, пожалуйста, на чьё имя забронировать столик?'
        return self.msg_reserved_name_txt

    def msg_reserved_que(self):
        self.msg_reserved_que_txt = '*Напиши, пожалуйста:*\n1. На сколько человек нужен столик?\n2. На какое время?\nОтвет напиши в свободной форме.\n*Например:*\nСтолик на 6 вечера в эту субботу, 3 человека'
        return self.msg_reserved_que_txt
    
    def msg_reserver_phone(self):
        self.msg_reserver_phone_txt = 'Для потверждение бронирования нам нужно будет с тобой связаться.\nПожалуйста, отправь номер телефона по кнопке ниже ⬇️'
        return self.msg_reserver_phone_txt

    def msg_reserved(self, first_name, username, name, phone , desc):
        self.first_name = first_name
        self.username = username
        self.name = name
        self.phone = phone
        self.desc = desc
        self.msg_reserved_txt = 'Заявка на бронь\nКлиент: ' + self.first_name +  ' - <b>@' f"{self.username}" + '</b>\nСтол на имя: ' + self.name + '\nТелефон: ' + self.phone +'\nОписание: {desc}.'.format(desc=self.desc)
        return self.msg_reserved_txt

    def msg_reserved_foruser(self):
        self.msg_reserved_foruser_txt = 'Заявка на бронь отправлена! С Вами свяжется администратор 🏃‍♀️'
        return self.msg_reserved_foruser_txt
        
    def msg_staff(self):
        self.msg_staff_txt = 'Кого позвать?'
        return self.msg_staff_txt
    
    def msg_staff_jobs(self):
        self.msg_staff_txt = 'Что передать официанту?'
        return self.msg_staff_txt
    
    def msg_staff_admin(self):
        self.msg_staff_admin_txt = 'Какой у тебя вопрос?'
        return self.msg_staff_admin_txt
    
    def msg_feedback(self):
        self.msg_feedback_txt = 'Напиши отзыв сообщением в свободной форме ⬇️\nЕсли хочешь, чтобы мы с тобой связались, оставь, пожалуйста, контактные данные.\n*Пример:*\nБыл у вас в пабе в среду, все понравилось: пиво вкусное, официанты вежливые 🍻'
        return self.msg_feedback_txt

    def msg_feedback_mail(self,first_name, username , desc):
        self.first_name = first_name
        self.username = username  
        self.desc = desc  
        self.msg_feedback_mail_txt = 'Новый отзыв\nКлиент: ' + self.first_name + ' - <b>@' f"{self.username}" + '</b>' + '\nОтзыв:\n' + self.desc
        return self.msg_feedback_mail_txt

    def msg_free_form(self):
        self.msg_free_form_txt = 'Напиши сообщение в свободной форме.'
        return self.msg_free_form_txt
        
    def msg_feedback_foruser(self):
        self.msg_feedback_foruser_txt = 'Отзыв отправлен!'
        return self.msg_feedback_foruser_txt 