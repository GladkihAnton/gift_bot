from django.db import models

from user.models import User


class Administrator(User):
    class Meta:
        proxy = True
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
