from django.conf import settings
from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=256, primary_key=True)
    password = models.CharField(max_length=128, null=False)

    chat_id = models.IntegerField(null=True, blank=True)

    account_status = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    recipients = models.ManyToManyField(
        'Recipient', symmetrical=False, default=[], related_name='customers', blank=True
    )

    def __str__(self):
        return '%s' % self.username

    class Meta:
        db_table = 'customer'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Recipient(models.Model):
    full_name = models.CharField(max_length=256, null=False)

    company_name = models.CharField(max_length=256, null=False)
    position = models.CharField(max_length=256, null=False)

    birthday = models.DateField(null=False)
    sex = models.ForeignKey('Sex', on_delete=models.CASCADE)

    contact_info = models.CharField(max_length=256, null=False)
    delivery_address = models.CharField(max_length=256, null=False)

    hobbies = models.ManyToManyField('Hobby', related_name='recipients')
    holidays = models.ManyToManyField('Holiday', related_name='recipients')

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
    name = models.CharField(max_length=256)

    image = models.ImageField('img', upload_to='img_cache/gifts')
    file_id = models.CharField(max_length=256, null=True, blank=True)

    hobbies = models.ManyToManyField('Hobby', related_name='gifts')
    package = models.ForeignKey('Package', models.CASCADE)
    description = models.CharField(max_length=256)
    type = models.ForeignKey('GiftType', on_delete=models.PROTECT)
    sex = models.ForeignKey('Sex', on_delete=models.PROTECT)
    coolness = models.IntegerField()
    price = models.DecimalField(decimal_places=3, max_digits=10)
    link = models.CharField(max_length=256)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'gift'
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'


class GiftType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'gift_type'
        verbose_name = 'Тип подарка'
        verbose_name_plural = 'Типы подарков'


class Package(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(
        'package_img', upload_to='img_cache/packages'
    )
    file_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'package'
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'


class SuggestedGift(models.Model):
    gift = models.ForeignKey(Gift, models.CASCADE)
    customer = models.ForeignKey(Customer, models.CASCADE)
    recipient = models.ForeignKey(Recipient, models.CASCADE)
    checked = models.BooleanField()
    presented = models.BooleanField(default=False)

    class Meta:
        db_table = 'suggested_gift'
        constraints = [
            models.UniqueConstraint(
                fields=['gift_id', 'recipient_id'], name='unique suggested gift'
            )
        ]


class Sex(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'sex'
        verbose_name = 'Пол'
        verbose_name_plural = 'Пола'


class Hobby(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'hobby'
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'


class Holiday(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'holiday'
        verbose_name = 'Праздник'
        verbose_name_plural = 'Праздники'


class OrderStatus(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'order_status'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    comment = models.CharField(max_length=128, null=True)
    voice = models.FileField(upload_to='voice_cache/', null=True)

    def __str__(self):
        return '%s для %s' % (self.customer.username, self.recipient.full_name)

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Order(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE)
    recipient = models.ForeignKey(Recipient, models.CASCADE)

    gift = models.ForeignKey(Gift, models.CASCADE)
    holiday = models.ForeignKey(Holiday, models.CASCADE)

    status = models.ForeignKey(OrderStatus, models.PROTECT)

    delivered_at = models.DateField(null=True, blank=True)
    recipient_score = models.IntegerField(null=True, blank=True)

    order_address = models.CharField(
        max_length=128, null=True, blank=True
    )  # TODO maybe not null field

    package = models.ForeignKey(Package, models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'order'
        constraints = [
            models.UniqueConstraint(
                fields=['gift_id', 'recipient_id'], name='unique ordered gift'
            )
        ]

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


