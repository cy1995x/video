from django.conf import settings
from utils.sms import YunTongXun
from video.celery import app


@app.task
def send_sms(phone, code):
    obj = YunTongXun(settings.A_ID, settings.A_TOKEN, settings.AP_ID, settings.T_ID)
    res = obj.run(phone, code)
    return res
