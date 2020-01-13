import configparser
import logging
import telegram
import telebot
import re

from telebot import types
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from search_weather import search_weather_data
from flask import Flask,request
from telegram.ext import Dispatcher,MessageHandler,CommandHandler, CallbackQueryHandler,Filters


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

#Enable logging 
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',level = logging.INFO)
logger = logging.getLogger(__name__)

#Initial Flask app
app = Flask(__name__)

#Initial bot by Telegeam access token
bot = telegram.Bot(token = (config['TELEGRAM']['ACCESS_TOKEN']))


@app.route('/hook',methods = ['POST','GET'])
def webhook_handler():
    '''Set route /hook with POST method will trigger this method'''
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True),bot)


        #Update dispatcher  process that hander to process this message
        dispatcher.process_update(update)
    return 'ok'

def replay_handler(bot,update):
    '''Replay message'''
    text = update.message.text
    if text == 'kevin':
        update.message.reply_text('Hi '+text)
    else:
        update.message.reply_text(text)


def start(bot,update):
    City1_DIC = {
        '基隆市':'Keelung_City','臺北市':'Taipei_City','新北市':'New_Taipei_City','桃園市':'Taoyuan_City',
        '新竹市':'Hsinchu_City','新竹縣':'Hsinchu_County'
    }
    City2_DIC = {
        '苗栗縣':'Miaoli_County','臺中市':'Taichung_City','彰化縣':'Changhua_County','南投縣':'Nantou_County',
        '雲林縣':'Yunlin_County','嘉義市':'Chiayi_City'
    }
    City3_DIC = {
        '嘉義縣':'Chiayi_County','宜蘭縣':'Yilan_County','花蓮縣':'Hualien_County','台東縣':'Taitung_County',
        '台南市':'Tainan_City','高雄市':'Kaohsiung_City'
    }
    City4_DIC = {
        '屏東縣':'Pingtung_County','連江縣':'Lienchiang_County','金門縣':'Kinmen_County','澎湖縣':'Penghu_County'
    }

    update.message.reply_text(
        '請輸入想要查詢的縣市天氣概況:',
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(str(city), callback_data= city_value ) for city,city_value in City1_DIC.items()],
            [InlineKeyboardButton(str(city), callback_data= city_value ) for city,city_value in City2_DIC.items()],
            [InlineKeyboardButton(str(city), callback_data= city_value ) for city,city_value in City3_DIC.items()],
            [InlineKeyboardButton(str(city), callback_data= city_value ) for city,city_value in City4_DIC.items()]
        ])
    )


       

def result(bot,update):
    #update.callback_query.edit_message_text(update.callback_query.data)
    print(update.callback_query.data)

    search_City = update.callback_query.data
    t_heads,t_bodys,t_nums = search_weather_data(search_City)

    # print(t_heads)
    # print(t_bodys)
    # print(t_nums)

    result_text = t_heads[0][0]+' 目前天氣概況 : \n\n'+t_bodys[0][0]+'\n'

    for i in range(1,len(t_heads[0])):
        result_text += '{0} : {1}\n'.format(t_heads[0][i],t_bodys[0][i])

    for i in range(0,len(t_heads[2])):
        result_text += '{0} : {1}\n'.format(t_heads[2][i],t_nums[1][i])

    update.callback_query.edit_message_text(result_text)
        
      


#New a dispatcher for bot
dispatcher = Dispatcher(bot,None)


#Add handler for handing message,there are many kinds of message,For this handler,it particular handle text
#message
dispatcher.add_handler(MessageHandler(Filters.text,replay_handler))
dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(CallbackQueryHandler(result))


if __name__ == '__main__':
    #Running server
    #app.debug = True
    app.run()


