import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseServerError
from django.views import View
from django.shortcuts import render

from administrator.forms import UploadFileForm
from recipient.models import Recipient, Sex, Gift


class FileUploadView(View):

    def get(self, request):
        return render(request, 'administrator/upload_file.html', {'form': UploadFileForm})


class RecipientUploadView(View):
    COLUMNS = ['full_name', 'company_name', 'position', 'sex', 'birthday', 'contact_info', 'delivery_address']

    def post(self, request):
        _, files = request.FILES.popitem()
        file: InMemoryUploadedFile = files[0]
        try:
            df = pd.read_csv(file, usecols=self.COLUMNS, iterator=True, chunksize=1000)
        except ValueError:
            return HttpResponseServerError('Ошибка при обработке файла, проверьте формат сsv')
        errors = []
        total = success = 0

        for chunk_num, chunk in enumerate(df, start=1):
            total += len(chunk)
            recipients = []

            for row_num, recipient_info in enumerate(chunk.to_dict(orient='records'), start=1):
                sexes = Sex.objects.filter(name__istartswith=recipient_info.pop('sex')[:3])
                if len(sexes) != 1:
                    errors.append((chunk_num - 1) * 1000 + row_num)
                    continue

                success += 1
                sex = sexes[0]
                recipients.append(Recipient(**recipient_info, sex=sex))

            Recipient.objects.bulk_create(recipients)

        return HttpResponse(content_type='text/plain',
                            content=f'File uploaded. \n'
                                    f'Total: {total} \n'
                                    f'Success: {success} \n'
                                    f'Error rows: {errors}')


class GiftUploadView(View):
    COLUMNS = ['name', 'description', 'sex', 'coolness', 'price', 'link']

    def post(self, request):
        _, files = request.FILES.popitem()
        file: InMemoryUploadedFile = files[0]
        try:
            gift_df = pd.read_csv(file, usecols=self.COLUMNS, iterator=True, chunksize=1000)
        except ValueError:
            return HttpResponseServerError('Ошибка при обработке файла, проверьте формат сsv')
        errors = []
        total = success = 0

        for chunk_num, chunk in enumerate(gift_df, start=1):
            total += len(chunk)
            gifts = []

            for row_num, gift_info in enumerate(chunk.to_dict(orient='records'), start=1):
                sexes = Sex.objects.filter(name__istartswith=gift_info.pop('sex')[:3])
                if len(sexes) != 1:
                    errors.append((chunk_num - 1) * 1000 + row_num)
                    continue

                success += 1
                sex = sexes[0]
                gifts.append(Gift(**gift_info, sex=sex))

            Gift.objects.bulk_create(gifts)

        return HttpResponse(content_type='text/plain',
                            content=f'File uploaded. \n'
                                    f'Total: {total} \n'
                                    f'Success: {success} \n'
                                    f'Error rows: {errors}')
