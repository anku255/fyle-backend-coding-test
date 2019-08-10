from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.getJWTToken, name='get-jwt-token'),
    path('bank', views.getBankDetails, name='bank-details'),
    path('branches', views.getBranchDetails, name='branch-details'),
]
