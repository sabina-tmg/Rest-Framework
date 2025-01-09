from django.urls import path
from.views import *
urlpatterns = [
path('students/create/',StudentCreateApi.as_view(),name='StudentCreateApi'),
path('student/list/',StudentListApi.as_view(),name='studentListApi'),
path('student/edit/',StudentEditApi.as_view(),name='StudentEditApi'),
path('student/<id>/delete/',StudentDeleteApiView.as_view(),name='StudentDeleteApiView')


]