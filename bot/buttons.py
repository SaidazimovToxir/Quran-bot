from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

class BotButtons:
    @staticmethod
    def main_button():
        """Returns the main reply keyboard markup."""
        return ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Suralar ✨"),
            # KeyboardButton("Namoz vaqtlari ⌛️"),
            # KeyboardButton("Allohning 99 ismi 💫")
        )
    
    @staticmethod
    def surah_inline_keys():
        """Returns the inline keyboard markup for surah navigation."""
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Oldingi oyat", callback_data='prev'),
            InlineKeyboardButton(text="Keyingi oyat", callback_data='next'),
            InlineKeyboardButton(text="Oyat audiosi", callback_data='audio')
        )
        
    @staticmethod
    def all_surah_buttons(surah_names, start_index):
        """Returns inline keyboard markup for displaying surahs."""
        markup = InlineKeyboardMarkup()
        row = []
        for i, name in enumerate(surah_names, start=start_index):
            callback_data = f"surah_{i}"
            button = InlineKeyboardButton(text=f"{i} {name}", callback_data=callback_data)
            row.append(button)
            if len(row) == 3:
                markup.row(*row)
                row = []
        if row:
            markup.row(*row)
        markup.row(
            InlineKeyboardButton(text="Oldingi suralar", callback_data="surah_prev"),
            InlineKeyboardButton(text="Keyingi suralar", callback_data="surah_next")
        )
        return markup
        
    @staticmethod
    def adminButtons():
        return ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Users info"),
            KeyboardButton("Send message all users")
        )



all_surah_names_1 = ["Al-Fatihah", "Al-Baqarah", "Ali 'Imran", "An-Nisa", "Al-Ma'idah", "Al-An'am", "Al-A'raf", "Al-Anfal", "At-Tawbah", "Yunus", "Hud", "Yusuf", "Ar-Ra'd", "Ibrahim", "Al-Hijr", "An-Nahl", "Al-Isra", "Al-Kahf", "Maryam", "Taha", "Al-Anbya", "Al-Hajj", "Al-Mu'minun", "An-Nur", "Al-Furqan", "Ash-Shu'ara", "An-Naml", "Al-Qasas", "Al-'Ankabut", "Ar-Rum", "Luqman", "As-Sajdah", "Al-Ahzab"] 
all_surah_names_2 = ["Saba", "Fatir", "Ya-Sin", "As-Saffat", "Sad", "Az-Zumar", "Ghafir", "Fussilat", "Ash-Shuraa", "Az-Zukhruf", "Ad-Dukhan", "Al-Jathiyah", "Al-Ahqaf", "Muhammad", "Al-Fath", "Al-Hujurat", "Qaf", "Adh-Dhariyat", "At-Tur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi'ah", "Al-Hadid", "Al-Mujadila", "Al-Hashr", "Al-Mumtahanah", "As-Saf", "Al-Jumu'ah", "Al-Munafiqun", "At-Taghabun", "At-Talaq", "At-Tahrim"]
all_surah_names_3 = ["Al-Mulk", "Al-Qalam", "Al-Haqqah", "Al-Ma'arij", "Nuh", "Al-Jinn", "Al-Muzzammil", "Al-Muddaththir", "Al-Qiyamah", "Al-Insan", "Al-Mursalat", "An-Naba", "An-Nazi'at", "'Abasa", "At-Takwir", "Al-Infitar", "Al-Mutaffifin", "Al-Inshiqaq", "Al-Buruj", "At-Tariq", "Al-A'la", "Al-Ghashiyah", "Al-Fajr", "Al-Balad", "Ash-Shams", "Al-Layl", "Ad-Duhaa", "Ash-Sharh", "At-Tin", "Al-'Alaq", "Al-Qadr", "Al-Bayyinah", "Az-Zalzalah"] 
all_surah_names_4 = ["Al-'Adiyat", "Al-Qari'ah", "At-Takathur", "Al-'Asr", "Al-Humazah", "Al-Fil", "Quraysh", "Al-Ma'un", "Al-Kawthar", "Al-Kafirun", "An-Nasr", "Al-Masad", "Al-Ikhlas", "Al-Falaq", "An-Nas"]

main_button = BotButtons.main_button()
inline_keys = BotButtons.surah_inline_keys()
adminButtons = BotButtons.adminButtons()

all_surah_buttons_1 = BotButtons.all_surah_buttons(all_surah_names_1, start_index=1)
all_surah_buttons_2 = BotButtons.all_surah_buttons(all_surah_names_2, start_index=34)
all_surah_buttons_3 = BotButtons.all_surah_buttons(all_surah_names_3, start_index=67)
all_surah_buttons_4 = BotButtons.all_surah_buttons(all_surah_names_4, start_index=100)

