from django.urls import path, include
from .views import login_view,logout_view,index_view, form_view, landing_view, delete_emp, download_vcf, qr_code_view,landing_view2,search, withmobile, withoutmobile, iadmin, visitcard

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('',index_view,name ='index'),
    # path('protected',include([
    #     path('', form_view, name='form'),
    #     path('iadmin/', iadmin, name='iadmin'),
    # ])),
    path('form', form_view, name='form'),
    path('iadmin/', iadmin, name='iadmin'),
    path('qr_code/<int:id>/',qr_code_view, name='qr_code'),
    path('details/<int:data_id>/', landing_view, name='details'),
    path('details2/<int:data_id>/', landing_view2, name='details2'),
    path('delete/<int:id>/', delete_emp, name='delete'),
    path('download/<int:id>/', download_vcf, name='download_vcf'),
    
    path('search/', search, name='search'),
    path('withmobile/<int:id>', withmobile, name='withmobile'),
    path('withoutmobile/<int:id>', withoutmobile, name='withoutmobile'),
    path('visitcard/<int:id>', visitcard, name='visitcard')
]