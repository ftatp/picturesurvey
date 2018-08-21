from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
	path('', views.index, name='index'),
	path('picture_select/', views.picture_select, name='picture_select'),
	path('done/', views.done, name='done'),
]
