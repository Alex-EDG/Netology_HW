import random

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

from SQL.Processor import SqlProcessor
from App.Common import Config

class TgBot:
    def __init__(self):
        self.db = SqlProcessor()
        print('Start telegram bot...')
        config = Config('settings.ini')
        state_storage = StateMemoryStorage()
        self.token_bot = config.read_config()['Telebot']['token']
        self.bot = TeleBot(self.token_bot, state_storage=state_storage)
        self.username = self.bot.get_me().username
        self.bot.add_custom_filter(custom_filters.StateFilter(self.bot))

        self.known_users = []
        self.userstep = {}

        @self.bot.message_handler(commands=['start'])
        def start(message):
            cid = message.chat.id
            global buttons
            buttons = []
            if cid not in self.known_users:
                self.known_users.append(cid)
                self.userstep[cid] = 0
                self.bot.send_message(cid, f"Привет {self.username}👋 Давай попрактикуемся в английском языке."
                                           f" Тренировки можешь проходить в удобном для себя темпе.\n"
                                           "У тебя есть возможность использовать тренажёр, как конструктор,"
                                           " и собирать свою собственную базу для обучения.\n"
                                           " Для этого воспользуйся инструментами:\n\n"
                                           "импорт слов из JSON ✍,\n"
                                           "добавить слово ➕,\n"
                                           "удалить слово ✂.")

            markup = types.ReplyKeyboardMarkup(row_width=2)
            help_btn = types.KeyboardButton(Command.HELP)
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            buttons = [help_btn, add_word_btn, next_btn]
            markup.add(*buttons)
            self.bot.send_message(message.chat.id, 'Ну что, начнём', reply_markup=markup)

        @self.bot.message_handler(commands=['cards'])
        def create_cards(message):
            global buttons
            buttons = []
            markup = types.ReplyKeyboardMarkup(row_width=2)
            select_db = self.db.select_4_random_words(self.username)
            target_word = select_db.get('target_word')  # Взято из БД
            translate = select_db.get('translate_word')  # Взято из БД
            target_word_btn = types.KeyboardButton(target_word)
            buttons.append(target_word_btn)
            others = select_db.get('other_words')  # Взято из БД

            other_words_btns = [types.KeyboardButton(word) for word in others]
            buttons.extend(other_words_btns)
            random.shuffle(buttons)
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            buttons.extend([add_word_btn, delete_word_btn, next_btn])
            markup.add(*buttons)
            greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
            self.bot.send_message(message.chat.id, greeting, reply_markup=markup)
            self.bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
            with self.bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['target_word'] = target_word
                data['translate_word'] = translate
                data['other_words'] = others

        @self.bot.message_handler(func=lambda message: message.text == Command.HELP)
        def send_help(message):
            self.bot.reply_to(message, 'Привет!!! Я знаю команды:\n/start - Бот стартует\n'
                                       '/help - справка по командам\n/cards - Вывести слово\n'
                                       '/import - ТОЛЬКО для первоначального внесения данных из файла Data/import.json')

        @self.bot.message_handler(commands=['help'])
        def help_(message):
            send_help(message)

        @self.bot.message_handler(commands=['import'])
        def import_data(message):
            self.bot.register_next_step_handler(message, self.db.import_user_data())
            self.bot.send_message(message.chat.id, f"Данные из Data/import.json импортированы в БД")
            help_(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.NEXT)
        def next_cards(message):
            create_cards(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
        def delete_word(message):
            with self.bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                del_w = data['translate_word'] # удалить из БД
                self.db.delete_word(self.username, del_w)
                self.bot.send_message(message.chat.id, f"Слово {del_w} удалено из базы пользователя {self.username}")

        @self.bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
        def add_word(message):
            self.userstep[message.chat.id] = 1
            msg = self.bot.send_message(message.chat.id, "Введи Ru_word=En_word(=En_word2 - если есть)")
            self.bot.register_next_step_handler(msg, add_w)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def message_reply(message):
            text = message.text
            markup = types.ReplyKeyboardMarkup(row_width=2)
            with self.bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                target_word = data['target_word']

                if text == target_word:
                    hint = show_target(data)
                    hint_text = ["Отлично!❤", hint]
                    hint = show_hint(*hint_text)

                else:
                    for btn in buttons:
                        if btn.text == text:
                            btn.text = text + '❌'
                            break
                    hint = show_hint("Допущена ошибка!",
                                     f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
            markup.add(*buttons)
            self.bot.send_message(message.chat.id, hint, reply_markup=markup)

        class Command:
            ADD_WORD = 'Добавить слово ➕'
            DELETE_WORD = 'Удалить слово ✂'
            NEXT = 'Дальше ⏭'
            HELP = 'Помощь ?'
            IMPORT = 'Импорт данных ✍'

        class MyStates(StatesGroup):
            target_word = State()
            translate_word = State()
            another_words = State()

        def show_hint(*lines):
            return '\n'.join(lines)

        def show_target(data):
            return f"{data['target_word']} -> {data['translate_word']}"

        def add_w(message):
            add_data = message.text.split(sep='=')
            if len(add_data) == 3:
                self.db.add_word(self.username, add_data[0], add_data[1], add_data[2])
            elif len(add_data) == 2:
                self.db.add_word(self.username, add_data[0], add_data[1])
            self.bot.send_message(message.chat.id, f"Есть {self.db.count_words(self.username)}"
                                                   f" слов для изучения в базе пользователя {self.username}")

    def run(self):
        self.bot.infinity_polling(skip_pending=True)

    def get_user_step(self, uid):
        if uid in self.userstep:
            return self. userstep[uid]
        else:
            self.known_users.append(uid)
            self.userstep[uid] = 0
            print("New user detected, who hasn't used \"/start\" yet")
            return 0

if __name__ == '__main__':

    tb = TgBot()
    tb.run()