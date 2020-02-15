import logging

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

logger = logging.getLogger("django")

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)
parser = WebhookParser(settings.CHANNEL_SECRET)
print("line_bot_api=", settings.CHANNEL_ACCESS_TOKEN)
print("handler=", settings.CHANNEL_SECRET)


@csrf_exempt
@require_POST
def webhook(request: HttpRequest):
    signature = request.headers["X-Line-Signature"]
    body = request.body.decode()
    print("signature =", signature)
    try:
        handler.handle(body, signature)
        events = parser.parse(body, signature)
        print("try....")
    except InvalidSignatureError:
        print("try error....")
        messages = (
            "Invalid signature. Please check your channel access token/channel secret."
        )
        logger.error(messages)
        return HttpResponseForbidden(messages)
    except LineBotApiError:
        return HttpResponseBadRequest()
    print("response before")
    return HttpResponse("OK")


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    print("handl....")
    print("handl_message....1")
    reply_token = event.reply_token
    print("handl_message....2")
    mtext = event.message.text
    print("handl_message....3")
    # if mtext == '@使用說明':
    #     print("if mtext")
    #     func.sendUse(event)

    # else:
    #     print("else")
    #     func.senQnA(event, mtext)

    messages = TextSendMessage(mtext)
    print("handl_message....4")
    line_bot_api.reply_message(reply_token, messages)
    print("handl_message....5")
