from django.db import models

from user.models import User


class Deliver(User):
    class Meta:
        proxy = True
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'
