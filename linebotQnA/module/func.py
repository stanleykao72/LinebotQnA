from django.conf import settings

import time
from datetime import timedelta, datetime
import twstock

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from imgurpython import ImgurClient

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage

import http.client
import json
from qnaapi.models import users

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)

host = settings.HOST  # 主機
endpoint_key = settings.ENDPOINT_KEY  # 授權碼
kb = settings.KB  # GUID碼

# -- upload
# imgur with account: your.mail@gmail.com
client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET


method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"


def sendUse(event):  # 使用說明
    try:
        text1 = '''
這是台大醫院的疑難解答，
請輸入關於台大醫院相關問題。
                '''
        message = TextSendMessage(
            text=text1
        )
        line_bot_api.reply_message(event.reply_token, message)

    except IndexError:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendQnA(event, mtext):  # QnA
    question = {
        'question': mtext,
    }
    print("question =", question)
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    print("headers =", headers)
    conn = http.client.HTTPSConnection(host)
    print("conn =", conn)
    conn.request("POST", method, content, headers)
    response = conn.getresponse()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    print("result1 =", result1)
    if 'No good match' in result1:
        text1 = '很抱歉，資料庫中無適當解答！\n請再輸入問題。'
        # 將沒有解答的問題寫入資料庫
        userid = event.source.user_id
        unit = users.objects.create(uid=userid, question=mtext)
        unit.save()
    else:
        result2 = result1[2:]  # 移除「A：」
        text1 = result2
    message = TextSendMessage(
        text=text1
    )
    line_bot_api.reply_message(event.reply_token, message)


def sendMe(event):
    content = str(event.source.user_id)
    message = TextSendMessage(
        text=content
    )
    line_bot_api.reply_message(event.reply_token, message)


def sendProfile(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    my_status_message = profile.status_message
    if not my_status_message:
        my_status_message = '_'
    message = [TextSendMessage(text='Display name: ' + profile.display_name),
               TextSendMessage(text='picture url: ' + profile.picture_url),
               TextSendMessage(text='status_message: ' + my_status_message)]
    line_bot_api.reply_message(event.reply_token, message)


def sendStockrt(event, mtext):
    mtext = mtext[1:]
    content = ''

    stock_rt = twstock.realtime.get(mtext)
    my_datetime = datetime.fromtimestamp(stock_rt['timestamp'] + 8 * 60 * 60)
    my_time = my_datetime.strftime('%H:%M:%S')

    content += '%s (%s) %s\n' % (
        stock_rt['info']['name'],
        stock_rt['info']['code'],
        my_time
    )
    content += '現價: %s / 開盤: %s\n' % (
        stock_rt['realtime']['latest_trade_price'],
        stock_rt['realtime']['open'])
    content += '最高: %s / 最低: %s\n' % (
        stock_rt['realtime']['high'],
        stock_rt['realtime']['low'])
    content += '量: %s\n' % (stock_rt['realtime']['accumulate_trade_volume'])

    stock = twstock.Stock(mtext)  # twstock.Stock('2330')
    content += '-----\n'
    content += '最近五日價格: \n'
    price5 = stock.price[-5:][::-1]
    date5 = stock.date[-5:][::-1]
    for i in range(len(price5)):
        # content += '[%s] %s\n' %(date5[i].strftime("%Y-%m-%d %H:%M:%S"), price5[i])
        content += '[%s] %s\n' % (date5[i].strftime("%Y-%m-%d"), price5[i])
    message = TextSendMessage(
        text=content
    )
    line_bot_api.reply_message(event.reply_token, message)


def sendStock(event, mtext):
    mtext = mtext[1:]
    fn = '%s.png' % (mtext)
    stock = twstock.Stock(mtext)
    my_data = {'close': stock.close, 'date': stock.date, 'open': stock.open}
    df1 = pd.DataFrame.from_dict(my_data)

    df1.plot(x='date', y='close')
    plt.title('[%s]' % (stock.sid))
    plt.savefig(fn)
    plt.close()

    print("Imgur upload")
    client = ImgurClient(client_id, client_secret)
    print("Uploading image... ")
    image = client.upload_from_path(fn, anon=True)

    url = image['link']
    print("url =", url)
    message = [
        TextSendMessage(
            text=url
        ),
        ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
    ]

    line_bot_api.reply_message(event.reply_token, message)
