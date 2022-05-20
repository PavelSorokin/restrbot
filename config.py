from telebot.storage import StateMemoryStorage

main_bot_token = '5320419353:AAEPbL94lz3PG7blljjwqT4K0f0FRCyabdI'
notify_bot_token = '5320419353:AAEPbL94lz3PG7blljjwqT4K0f0FRCyabdI'
bot_chat_id = '-1001640458092'
bot_chat_id_admin = '-1001640458092'
bot_chat_id_feedback = '-1001640458092'

user_json = {  'chat_id' : '',
                'login' : '',
                'first_name' : ''}

timeout = {}
timeout_seconds = 60

admins = [394011279,396471113,420553555] 

menu_file = './files/food.pdf'
bar_file = './files/bar.pdf'
sales_files = './files/sales*.jpg'
concert_files = './files/concert*.jpg'
timeout_gif = './files/timeout_cat.mp4'

state_storage = StateMemoryStorage()