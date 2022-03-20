from django.contrib import admin

from administrator.models import Administrator


class AdministratorAdmin(admin.ModelAdmin):
    exclude = ['chat_id', 'recipients']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(account_status='admin')


admin.site.register(Administrator, AdministratorAdmin)
