from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ['chat_id', 'recipients']


admin.site.register(User, UserAdmin)
