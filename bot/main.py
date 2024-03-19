import telebot
import logging
import requests
import replies
# import datetime
from datetime import datetime
from api import CreateUser
from adminCommands import AdminCommands
from buttons import (inline_keys, main_button, adminButtons,
                        all_surah_buttons_1, all_surah_buttons_2, 
                        all_surah_buttons_3, all_surah_buttons_4
                     )

class QuranBot:
    def __init__(self, api_token) -> None:
        self.API_TOKEN = api_token
        self.bot = telebot.TeleBot(api_token)
        logging.basicConfig(level=logging.INFO)
        
        self.surahCount = 1
        self.surah_number = None
        self.dataArabic = None
        self.dataUzbek = None
        self.surah_arabic = {}
        self.surah_uzbek = {}
        self.admin_command_state = {}
        self.count = 1
        
        self.register_handlers()
        self.admin_commands = AdminCommands()
        
        
    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_command)
        self.bot.message_handler(commands=['help'])(self.help_command)
        self.bot.message_handler(commands=['adminCommands'])(self.adminCommands)

        self.bot.message_handler(func=lambda message: message.text == "Suralar ✨")(self.get_all_surah)
        # # self.bot.message_handler(func=lambda message: message.text == "Namoz vaqtlari ⌛️")(self.getNamazTimes)
        # # self.bot.message_handler(func=lambda message: message.text == "Allohning 99 ismi 💫")(self.getAllahNames)
        self.bot.message_handler(func=lambda message: message.text == 'Users info')(self.response_all_users)
        self.bot.message_handler(func=lambda message: message.text == 'Send message all users')(self.send_message_all_users)

        
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'prev')(self.previous_ayahs)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'next')(self.next_ayahs)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'audio')(self.get_valid_ahays_audios)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'surah_prev')(self.all_previous_surah)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'surah_next')(self.all_next_surah)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('surah_'))(self.get_selected_surah)
        # self.bot.message_handler(func=lambda callback_query: callback_query.data == 'checkAdmin')(self.checkAdmin)
        
        
        self.bot.message_handler(func=lambda message: True)(self.handle_user_response)
        
        
    def runBot(self):
        print("Bot polling...")
        self.bot.polling(non_stop=True)
            
    ## COMMANDS   
    def start_command(self, ms):
        fn = ms.from_user.first_name
        chatID = ms.chat.id
        reply = replies.start.format(firstName=fn)
        reply2 = replies.start2
        db = CreateUser(fn, ms.from_user.username, ms.from_user.id, datetime.now())
        res = db.get_user()
        print(res)
        
        self.bot.send_message(chatID, reply, parse_mode='html', reply_markup=main_button)
        self.bot.send_message(chatID, reply2, parse_mode='html')
    
    def help_command(self, ms):
        chatID = ms.chat.id
        msID = ms.message_id
        reply = replies.help
        self.bot.send_message(chatID, reply, reply_to_message_id=msID)
   
    def adminCommands(self, message):
        try:
            reply = replies.adminCommands
            self.bot.send_message(message.chat.id, reply, parse_mode='html')

            self.admin_command_state[message.chat.id] = "waiting_for_text"
            print(self.admin_command_state)
        except Exception as e:
            pass
    
    def handle_user_response(self, message):
        try:
            login = 'a'
            parol = 's'
            chat_id = message.chat.id
            reply = replies.admin
            if chat_id in self.admin_command_state and self.admin_command_state[chat_id] == "waiting_for_text":
                threat = message.text.split()
                if threat[0]==login and threat[1] == parol:
                    self.bot.send_message(chat_id, reply, reply_markup=adminButtons)

                else:
                    self.bot.send_message(chat_id, "Afsuski parol xato\nQayta urinib ko'rish uchun\n/adminCommands buyrug'ini yuboring")

                del self.admin_command_state[chat_id]
                
            if chat_id in self.admin_command_state and self.admin_command_state[chat_id] == 'waiting_for_all_users':
                text_for_users = message.text
                for i in self.admin_commands.send_message_to_all_users():
                    self.bot.send_message(i,text_for_users)
                    
                del self.admin_command_state[chat_id]
                self.bot.send_message(message.chat.id, "Barcha malumotlar foydalanuvchilarga muaffaqiyatli yuborildi.")
                    
        except Exception as e:
            self.bot.send_message(message.chat.id, f"ERROR: {e}")    
    ## /COMMANDS
    
    ## ADMIN BUTTONS
    def response_all_users(self, message):
        try:
            for i in self.admin_commands.users_info():
                timeStr = i['created_dt'].rstrip('Z')
                created_dt = datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%f")
                dataTime = created_dt.strftime("%Y-%m-%d %H:%M:%S")

                reply = replies.user_info.format(ID=i['user_id'], FN=i['name'], USERNM=i['username'], DATE=dataTime)
                self.bot.send_message(message.chat.id, reply, parse_mode='html')
        except Exception as e:
            self.bot.send_message(message.chat.id, f"ERROR: barcha userlarni chiqarishda xatolik bor {e}")
    def send_message_all_users(self, message):
        self.bot.send_message(message.chat.id, "Foydalanuvchilarga yubormoqchi bo'lgan matn: ")
        
        self.admin_command_state[message.chat.id] = "waiting_for_all_users"
        print(self.admin_command_state)
        # try:
        #     message_to_send = "This is a message from admin."
        #     for i in self.admin_commands.send_message_to_all_users():
        #         self.bot.send_message(i,message_to_send)
        # except Exception as e:
        #     print(e)
    
        
    def get_all_surah(self, message):
        self.bot.send_message(message.chat.id, "Quyidagi suralardan birini tanlang: ", reply_markup=all_surah_buttons_1)

        ## NEXT BUTTON FOR ALL SURAH
    def all_next_surah(self, callback_query):
        try:
            if self.surahCount == 4:
                self.surahCount = 0
            if self.surahCount < 4:
                self.surahCount += 1
                markup = None
                if self.surahCount == 1:
                    markup = all_surah_buttons_1
                elif self.surahCount == 2:
                    markup = all_surah_buttons_2
                elif self.surahCount == 3:
                    markup = all_surah_buttons_3
                elif self.surahCount == 4:
                    markup = all_surah_buttons_4
                if markup:
                    self.bot.edit_message_text("Quyidagi suralardan birini tanlang: ", 
                                            chat_id=callback_query.message.chat.id, 
                                            message_id=callback_query.message.message_id, 
                                            reply_markup=markup)
        
        except Exception as e:
            print(f"Surah Next ERROR: {e}")
        

        ## PREVIOUS BUTTON FOR ALL SURAH
    def all_previous_surah(self, callback_query):
        try:
            if self.surahCount > 1:
                self.surahCount -= 1
                markup = None
                if self.surahCount == 3:
                    markup = all_surah_buttons_3
                elif self.surahCount == 2:
                    markup = all_surah_buttons_2
                elif self.surahCount == 1:
                    markup = all_surah_buttons_1
                if markup:
                    self.bot.edit_message_text("Quyidagi suralardan birini tanlang: ", 
                                            chat_id=callback_query.message.chat.id, 
                                            message_id=callback_query.message.message_id, 
                                            reply_markup=markup)
        
        except Exception as e:
            print(f"Surah Previous ERROR: {e}")

        ## GET THE SURAH NUMBER AFTER INLINE BUTTONS CLICKED
    def get_selected_surah(self, callback_query):
        self.surah_number = int(callback_query.data.split('_')[1])
        self.get_valid_surah(callback_query.message)
       
        ## ALL SURAH SAVED IN DICT SECTION
    def get_valid_surah(self, message):
        try:   
            url = f"http://api.alquran.cloud/v1/surah/{self.surah_number}/ar.alafasy"
            urlUz = f"http://api.alquran.cloud/v1/surah/{self.surah_number}/uz.sodik"

            response = requests.get(url)
            self.dataArabic = response.json()

            respons = requests.get(urlUz)
            self.dataUzbek = respons.json()
                
            self.surah_arabic = {i['numberInSurah']: i['text'] for i in self.dataArabic['data']['ayahs']}
            self.surah_uzbek = {i['numberInSurah']: i['text'] for i in self.dataUzbek['data']['ayahs']}
            
            chat_id = message.chat.id
            message_id = message.message_id
            self.bot.delete_message(chat_id, message_id)            
            
            self.count = 1
            mes = f""" 
<b>Surah:</b> {self.dataArabic['data']['englishName']} ({self.dataArabic['data']['number']})
<b>Ayahs:</b> {self.count} out of {len(self.surah_arabic.keys())}

<u><b>Arabic:</b></u> <blockquote>{self.surah_arabic[self.count] if self.count in self.surah_arabic else "Error"}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{self.surah_uzbek[self.count] if self.count in self.surah_uzbek else "Xatolik"}</blockquote>  
        """
            self.bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=inline_keys)
        
        except Exception as e:
            print(f"Get Valid Surah ERROR: {e}")
        
        
        ## NEXT BUTTON SECTION
    def next_ayahs(self, callback_query):
        try:
            self.count += 1

            if self.count > 0 and self.count <= len(self.surah_arabic.keys()): 
                mes = f""" 
<b>Surah:</b> {self.dataArabic['data']['englishName']} ({self.dataArabic['data']['number']})
<b>Ayahs:</b> {self.count} out of {len(self.surah_arabic.keys())}

<u><b>Arabic:</b></u> <blockquote>{self.surah_arabic[self.count] if self.count in self.surah_arabic else "NimaduAr"}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{self.surah_uzbek[self.count] if self.count in self.surah_uzbek else "NimaduUz"}</blockquote>  
            """
                self.bot.edit_message_text(mes, chat_id=callback_query.message.chat.id, 
                                        message_id=callback_query.message.message_id, 
                                        parse_mode='html', 
                                        reply_markup=inline_keys)
            else:
                self.count -= 1
        
        except Exception as e:
            print(f"Ayahs Next Button ERROR: {e}")
        
        ## PREVIOUS BUTTON SECTION
    def previous_ayahs(self, callback_query):
        try:
            self.count -= 1
    
            if self.count > 0 and self.count <= len(self.surah_arabic.keys()): 
                mes = f""" 
<b>Surah:</b> {self.dataArabic['data']['englishName']} ({self.dataArabic['data']['number']})
<b>Ayahs:</b> {self.count} out of {len(self.surah_arabic.keys())}

<u><b>Arabic:</b></u> <blockquote>{self.surah_arabic[self.count] if self.count in self.surah_arabic else "NimaduAr"}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{self.surah_uzbek[self.count] if self.count in self.surah_uzbek else "NimaduUz"}</blockquote>  
            """
                self.bot.edit_message_text(mes, chat_id=callback_query.message.chat.id, 
                                        message_id=callback_query.message.message_id, 
                                        parse_mode='html', 
                                        reply_markup=inline_keys)
            else:
                self.count += 1
        
        except Exception as e:
            print(f"Ayahs previous button ERROR: {e}")
        
            
        ## AUDIOS SECTION
    def get_valid_ahays_audios(self, callback_query):
        try:
            for i in self.dataArabic['data']['ayahs']:
                if self.count == i['numberInSurah']:
                    self.bot.send_audio(callback_query.message.chat.id, i['audio'])
                    break
        except Exception as e:
            print(f"Ayahs Audio button ERROR: {e}")
            
        
if __name__ == '__main__':
    bot = QuranBot("6914186527:AAGCjIkdi4rk-cu80apjVXXts29lXJ12AAI")
    bot.runBot()
