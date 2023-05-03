import os
from django.test import SimpleTestCase
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from orders.services.notify import NotifyService


class NotifyServiceTest(SimpleTestCase):

    def setUp(self) -> None:
        # данные для емайл
        self.subject = "Ваш заказ прибыл в пункт выдачи"
        self.body = "Здравствуйте, заказ AAP114630687 прибыл в пункт выдачи по адресу: Челябинск, ул.Ленина 5." \
                    "Заберите его в течение 5 дней."
        # данные для смс
        self.message = "Заказ № {AAP114630687} готов к выдаче. Телефон: 88001005441. МК Электро"
        self.phone = "+79828887665"

    def test_send_email(self):
        n = NotifyService()
        response = n.send_email(self.subject, self.body)
        self.assertEqual(1, response)

    def test_send_sms(self):
        """
        Тест с некорректными данными
        """
        n = NotifyService()
        response = n.send_sms(self.message, self.phone)
        # self.assertEqual("OK - <n> SMS, ID - <id>", response)
        self.assertEqual(None, response)

