from django.contrib import admin

from recipient.models import (
    Comment,
    Customer,
    Gift,
    GiftType,
    Hobby,
    Holiday,
    Order,
    OrderStatus,
    Package,
    Recipient,
    Sex,
)


class CustomerAdmin(admin.ModelAdmin):
    exclude = ['chat_id']
    filter_horizontal = ('recipients',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(account_status='customer')


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'sex')

    def sex(self, obj):
        return obj.sex.name


class SexAdmin(admin.ModelAdmin):
    pass


class HolidayAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'recipient', 'comment', 'voice')

    def username(self, obj):
        return obj.customer.username

    def recipient(self, obj):
        return obj.recipient.full_name

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class HobbyAdmin(admin.ModelAdmin):
    ordering = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'recipient', 'gift', 'holiday', 'status', 'package')
    search_fields = ['id', 'recipient__full_name']

    def username(self, obj):
        return obj.customer.username

    def recipient(self, obj):
        return obj.recipient.full_name

    def gift(self, obj):
        return obj.gift.name

    def holiday(self, obj):
        return obj.holiday.name

    def status(self, obj):
        return obj.status.name

    def package(self, obj):
        return obj.package.name


class GiftAdmin(admin.ModelAdmin):
    exclude = ['file_id']


class PackageAdmin(admin.ModelAdmin):
    exclude = ['file_id']


class OrderStatusAdmin(admin.ModelAdmin):
    pass


class GiftTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Gift, GiftAdmin)
admin.site.register(GiftType, GiftTypeAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(Hobby, HobbyAdmin)
admin.site.register(Sex, SexAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
