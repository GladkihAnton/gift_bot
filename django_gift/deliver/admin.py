from django.contrib import admin

from deliver.models import Deliver


class DeliverAdmin(admin.ModelAdmin):
    exclude = ['chat_id', 'recipients']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(account_status='deliver')


admin.site.register(Deliver, DeliverAdmin)
