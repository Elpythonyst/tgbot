import logging
import ephem
import datetime
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level = logging.INFO)


PROXY={'proxy_url': settings.PROXY_URL,
 'urllib3_proxy_kwargs':{'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def main():
    mybot = Updater(settings.API_KEY,
     use_context= True, request_kwargs= PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) 
    dp.add_handler(CommandHandler("planet", planet_info))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    

def greet_user (update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def planet_info(update, context):
    user_text = update.message.text.split()[1]
    planet_list = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    current_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d')
    print(user_text)
    try:
        update.message.reply_text(ephem.constellation(getattr(ephem, user_text)(current_date)))
    except AttributeError:
        update.message.reply_text('Введено неправильное название планеты (либо Земля)')    

if __name__ == '__main__':
    main()