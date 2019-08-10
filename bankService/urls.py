from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bank', views.getBankDetails, name='bank-details'),
    path('branches', views.getBranchDetails, name='branch-details'),
]
