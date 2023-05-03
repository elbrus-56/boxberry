from typing import Optional

import requests
from django.core.mail import EmailMessage
from loguru import logger
from requests import Response

from config.settings import SMSC_LOGIN, SMSC_PASSWORD

logger.add("orders.log")


class NotifyService:
    SMSC_URL = "https://smsc.ru/sys/send.php"

    @staticmethod
    def send_email(subject: Optional[str] = None, message: Optional[str] = None) -> int:
        """Отправка уведомлений на электронную почту

            :param subject: тема письма.
            :param message: сообщение для отправки.
            :return: 1, если письмо отправлено, иначе 0
        """
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email="sender@test.test",
            to=["recepient@test.test"],
        )

        if email.send(fail_silently=False) == 1:
            return 1
        else:
            logger.error(f'NotifyService: send_email: Возникла ошибка при отправке email сообщения')
            return 0

    @classmethod
    def send_sms(cls, message: str, phone_number: str) -> Optional[Response]:
        """
        Функция отправляет СМС уведомления

            :param message: текст сообщения.
            :param phone_number: номер телефона получателя в формате 79998887766
            :return: :class:`Response <Response>` object или None

        """
        data = {
            "login": SMSC_LOGIN,
            "psw": SMSC_PASSWORD,
            "phones": phone_number,
            "mes": message
        }
        try:
            r = requests.post(cls.SMSC_URL, data=data)
        except Exception as e:
            logger.error(f"SMSC: send_sms: {cls.SMSC_URL}  with {data}- {e}")
            return
        else:
            if "ERROR" not in r.text:
                return r
            else:
                logger.error(f"SMSC: send_sms: {r.text}")
                return
