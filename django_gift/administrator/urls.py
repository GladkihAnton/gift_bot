from django.urls import path

from . import views

urlpatterns = [
    path('upload_file', views.FileUploadView.as_view(), name='file_upload_template'),
    path('upload_recipients', views.RecipientUploadView.as_view(), name='recipient_upload_file'),
    path('upload_gifts', views.GiftUploadView.as_view(), name='gift_upload_file'),
]
