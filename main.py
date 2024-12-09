import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
from helpers import get_nba_schedule, get_stats

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    
    markup         = types.ReplyKeyboardMarkup(resize_keyboard=True)
    schedule_btn   = types.KeyboardButton("Расписание матчей")
    statistics_btn = types.KeyboardButton("Статистика")
    info_btn       = types.KeyboardButton("Информация")
    markup.add(schedule_btn, statistics_btn, info_btn)

    bot.send_message(message.chat.id,
"""
Привет, любитель баскетбола! 
        
Я бот, который может показать тебе расписание матчей NBA.
Нажми на кнопку ниже, чтобы получить расписание.
""",
        reply_markup=markup
    )

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    
    if message.text == "Расписание матчей":
        
        markup           = types.ReplyKeyboardMarkup(resize_keyboard=True)
        one_day_btn      = types.KeyboardButton("Расписание матчей на сегодня")
        three_days_btn   = types.KeyboardButton("Расписание матчей на 3 дня")
        seven_days_btn   = types.KeyboardButton("Расписание матчей на 7 дней")
        back_btn         = types.KeyboardButton("Вернуться назад")
        markup.add(one_day_btn, three_days_btn, seven_days_btn, back_btn)

        bot.send_message(message.chat.id, 
            """
            Выберите нужную вам опцию
            """,
            reply_markup=markup)
        # games = get_nba_schedule()
        # if games:
        #     pass
    

    elif message.text == 'Информация':
        bot.send_message(message.chat.id,
            """
    Бот создан в рамках курсовой работы.
    Вся информация берется с сайта: championat.com
    Создатель: @pashasha1
            """)
    

    elif message.text == 'Расписание матчей на сегодня':
        answer = get_nba_schedule(1)
        bot.send_message(message.chat.id, f'Предстоящие матчи на сегодня\n\n\n{answer}')


    elif message.text == "Расписание матчей на 3 дня":
        answer = get_nba_schedule(3)
        bot.send_message(message.chat.id, f'Предстоящие матчи на следующие 3 дня\n\n\n{answer}')


    elif message.text == "Расписание матчей на 7 дней":
        answer = get_nba_schedule(7)
        bot.send_message(message.chat.id, f'Предстоящие матчи на следующие 7 дня\n\n\n{answer}')


    elif message.text == 'Статистика':
        markup           = types.ReplyKeyboardMarkup(resize_keyboard=True)
        points_btn       = types.KeyboardButton("Статистика по очкам")
        rebounds_btn     = types.KeyboardButton("Статистика по подборам")
        assists_btn      = types.KeyboardButton("Статистика по передачам")
        back_btn         = types.KeyboardButton("Вернуться назад")
        markup.add(points_btn, rebounds_btn, assists_btn, back_btn)
        bot.send_message(message.chat.id, 'Выберите интересующую вас статистику', reply_markup=markup)

    
    

    elif message.text == 'Статистика по подборам':
        bot.send_message(message.chat.id, get_stats('reb'))

    elif message.text == 'Статистика по передачам':
        bot.send_message(message.chat.id, get_stats('ast'))    

    elif message.text == 'Статистика по очкам':
        bot.send_message(message.chat.id, get_stats('pts'))

        
    elif message.text == "Вернуться назад":
        markup         = types.ReplyKeyboardMarkup(resize_keyboard=True)
        schedule_btn   = types.KeyboardButton("Расписание матчей")
        statistics_btn = types.KeyboardButton("Статистика")
        info_btn       = types.KeyboardButton("Информация")
        markup.add(schedule_btn, statistics_btn, info_btn)
        bot.send_message(message.chat.id, 'Выберите интересующую вас опцию', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Пожалуйста, введите команду /start.")




if __name__ == '__main__':
    bot.polling(none_stop=True)
