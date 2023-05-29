pip install python-telegram-bot
关注@BotFather用户
/newbot    		#创建
yunwei2020 		#用户名
yunwei2020_bot 		#id


生成的token
1226928487:AAFmmT4qQv31ZTHTxZuvPZNss6ejJ5PDnKs
创建channel 设置为@yunweijiqiren 邀请机器人设为管理

import telegram
bot=telegram.Bot(token="1226928487:AAFmmT4qQv31ZTHTxZuvPZNss6ejJ5PDnKs")
bot.send_message(chat_id='@yunweijiqiren',text='okok no problem')
