from eskiz.client.sync import ClientSync
from django.conf import settings


def get_eskiz_client():
    """
    EskizSMS clientni login bilan qaytaradi.
    """
    client = ClientSync(email=settings.ESKIZ_EMAIL, password=settings.ESKIZ_PASSWORD)
    client.login()
    return client


def send_sms(phone, message):
    """
    Telefon raqamga SMS yuboradi. phone: `998901234567` formatida bo'lishi kerak.
    """
    client = get_eskiz_client()
    response = client.send_sms(
        phone_number=phone,
        message=message,
        # from_whom="4546",
        # callback_url="http://eskiz.uz"
    )
    return response
