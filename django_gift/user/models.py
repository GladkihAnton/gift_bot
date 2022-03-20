from django.db import models


class User(models.Model):
    username = models.CharField(
        max_length=256, primary_key=True, verbose_name='Телеграм логин'
    )
    password = models.CharField(max_length=128, null=False, verbose_name='Пароль')

    chat_id = models.IntegerField(null=True, blank=True)

    account_status = models.CharField(
        max_length=32, null=True, blank=True, verbose_name='Роль', default='customer'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    recipients = models.ManyToManyField(
        'recipient.Recipient',
        symmetrical=False,
        default=[],
        related_name='customers',
        blank=True,
        verbose_name='Получатели',
    )

    def __str__(self):
        return '%s' % self.username

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


