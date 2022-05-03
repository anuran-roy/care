import requests
from django.conf import settings

from care.users.models import phone_number_regex


def _opt_in(phone_number):
    url_data = {
        "method": "OPT_IN",
        "auth_scheme": "plain",
        "v": "1.1",
        "phone_number": phone_number,
        "password": settings.WHATSAPP_API_PASSWORD,
        "userid": settings.WHATSAPP_API_USERNAME,
        "channel": "whatsapp",
    }
    return requests.post(settings.WHATSAPP_API_ENDPOINT, params=url_data)


def _send(phone_number, message, notification_id):
    _opt_in(phone_number)
    url_data = {
        "method": "SendMessage",
        "auth_scheme": "plain",
        "v": "1.1",
        "send_to": phone_number,
        "msg": message["message"],
        "isHSM": "True",
        "buttonUrlParam": str(notification_id),
        "msg_type": "HSM",
        "password": settings.WHATSAPP_API_PASSWORD,
        "userid": settings.WHATSAPP_API_USERNAME,
        "isTemplate": "true",
        "header": message["header"],
        "footer": message["footer"],
    }
    return requests.post(settings.WHATSAPP_API_ENDPOINT, params=url_data)


def sendWhatsappMessage(phone_numbers, message, notification_id, many=False):
    if not many:
        phone_numbers = [phone_numbers]
    phone_numbers = list(set(phone_numbers))
    for phone in phone_numbers:
        try:
            phone_number_regex(phone)
        except Exception:
            continue
        _send(phone, message, notification_id)
    return True

