from django.urls import path
from .views import form_view, landing_view, delete_emp, download_vcf

urlpatterns = [
    path('', form_view, name='form'),
    path('details/<int:data_id>/', landing_view, name='details'),
    path('delete/<int:id>/', delete_emp, name='delete'),
    path('download/<int:id>/', download_vcf, name='download_vcf'),
]