from django.urls import path
from .views import LoginApiView,UserRegisterApiView

urlpatterns=[
path("login/",LoginApiView.as_view(),name='login'),
path('register/',UserRegisterApiView.as_view(), name='register')

]
