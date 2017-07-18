from django.conf.urls import url, include
from my_app import views

app_name = 'my_app'

urlpatterns = [
    url('^register', views.register, name='register'),
    url('^login', views.user_login, name='user_login'),
]