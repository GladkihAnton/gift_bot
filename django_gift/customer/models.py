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


class Gift(models.Model):
    name = models.CharField(max_length=256)

    image = models.ImageField('img', upload_to=settings.MEDIA_ROOT + 'img_cache/gifts')
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


class GiftType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'gift_type'


class Package(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(
        'package_img', upload_to=settings.MEDIA_ROOT + 'img_cache/packages'
    )
    file_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'package'


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


class Hobby(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'hobby'


class Holiday(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'holiday'


class OrderStatus(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'order_status'

    def __str__(self):
        return '%s' % self.name


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    comment = models.CharField(max_length=128, null=True)
    voice = models.FileField(upload_to=settings.MEDIA_ROOT + 'voice_cache/', null=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return '%s для %s' % (self.customer.username, self.recipient.full_name)


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
