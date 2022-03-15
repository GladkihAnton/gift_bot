from django.db import models


class Customer(models.Model):
    username = models.CharField(
        max_length=256, primary_key=True, verbose_name='Телеграм логин'
    )
    password = models.CharField(max_length=128, null=False, verbose_name='Пароль')

    chat_id = models.IntegerField(null=True, blank=True)

    account_status = models.CharField(
        max_length=32, null=True, blank=True, verbose_name='Роль'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    recipients = models.ManyToManyField(
        'Recipient',
        symmetrical=False,
        default=[],
        related_name='customers',
        blank=True,
        verbose_name='Получатели',
    )

    def __str__(self):
        return '%s' % self.username

    class Meta:
        db_table = 'customer'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Recipient(models.Model):
    full_name = models.CharField(max_length=256, null=False, verbose_name='ФИО')

    company_name = models.CharField(max_length=256, null=False, verbose_name='Компания')
    position = models.CharField(max_length=256, null=False, verbose_name='Должность')

    birthday = models.DateField(null=False, verbose_name='Дата рождения')
    sex = models.ForeignKey('Sex', on_delete=models.CASCADE, verbose_name='Пол')

    contact_info = models.CharField(
        max_length=256, null=False, verbose_name='Контактная информация'
    )
    delivery_address = models.CharField(
        max_length=256, null=False, verbose_name='Адрес доставки'
    )

    hobbies = models.ManyToManyField(
        'Hobby', related_name='recipients', verbose_name='Интересы'
    )
    holidays = models.ManyToManyField(
        'Holiday', related_name='recipients', verbose_name='Праздники'
    )

    gifts = models.ManyToManyField(
        'Gift', related_name='recipients', through='SuggestedGift'
    )

    def __str__(self):
        return '%s' % self.full_name

    class Meta:
        db_table = 'recipient'
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Gift(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    image = models.ImageField(upload_to='img_cache/gifts', verbose_name='Картинка')
    file_id = models.CharField(max_length=256, null=True, blank=True)

    hobbies = models.ManyToManyField(
        'Hobby', related_name='gifts', verbose_name='Интересы'
    )
    package = models.ForeignKey('Package', models.CASCADE, verbose_name='Упаковка')
    description = models.CharField(max_length=256, verbose_name='Описание')
    type = models.ForeignKey(
        'GiftType', on_delete=models.PROTECT, verbose_name='Тип подарка'
    )
    sex = models.ForeignKey('Sex', on_delete=models.PROTECT, verbose_name='Пол')
    coolness = models.IntegerField(verbose_name='Прикольность')
    price = models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Цена')
    link = models.CharField(max_length=256, verbose_name='Ссылка')

    def __str__(self):
        return '%s' % self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.file_id = None
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'gift'
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'


class GiftType(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'gift_type'
        verbose_name = 'Тип подарка'
        verbose_name_plural = 'Типы подарков'


class Package(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='img_cache/packages', verbose_name='Картинка')
    file_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.file_id = None
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'package'
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'


class SuggestedGift(models.Model):
    gift = models.ForeignKey(Gift, models.CASCADE, verbose_name='Подарок')
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name='Отправитель')
    recipient = models.ForeignKey(Recipient, models.CASCADE, verbose_name='Получатель')
    checked = models.BooleanField()
    presented = models.BooleanField(default=False, verbose_name='Подарен?')

    class Meta:
        db_table = 'suggested_gift'
        constraints = [
            models.UniqueConstraint(
                fields=['gift_id', 'recipient_id'], name='unique suggested gift'
            )
        ]


class Sex(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'sex'
        verbose_name = 'Пол'
        verbose_name_plural = 'Пола'


class Hobby(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'hobby'
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique hobby name')
        ]


class Holiday(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    active = models.BooleanField(default=True, verbose_name='Активен?')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'holiday'
        verbose_name = 'Праздник'
        verbose_name_plural = 'Праздники'


class OrderStatus(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'order_status'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Comment(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='Отправитель'
    )
    recipient = models.ForeignKey(
        Recipient, on_delete=models.CASCADE, verbose_name='Получатель'
    )
    comment = models.CharField(max_length=128, null=True, verbose_name='Комментарий')
    voice = models.FileField(upload_to='voice_cache/', null=True, verbose_name='Аудио')

    def __str__(self):
        return '%s для %s' % (self.customer.username, self.recipient.full_name)

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Order(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name='Отправитель')
    recipient = models.ForeignKey(Recipient, models.CASCADE, verbose_name='Получатель')

    gift = models.ForeignKey(Gift, models.CASCADE, verbose_name='Подарок')
    holiday = models.ForeignKey(Holiday, models.CASCADE, verbose_name='Праздник')

    status = models.ForeignKey(
        OrderStatus, models.PROTECT, verbose_name='Статус заказа'
    )

    delivered_at = models.DateField(null=True, blank=True, verbose_name='Отправлен в')
    recipient_score = models.IntegerField(null=True, blank=True)

    order_address = models.CharField(
        max_length=128, null=True, blank=True
    )  # TODO maybe not null field

    package = models.ForeignKey(
        Package, models.PROTECT, null=True, blank=True, verbose_name='Упаковка'
    )

    class Meta:
        db_table = 'order'
        constraints = [
            models.UniqueConstraint(
                fields=['gift_id', 'recipient_id'], name='unique ordered gift'
            )
        ]

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
