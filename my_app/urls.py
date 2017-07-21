from django.conf.urls import url
from my_app import views

app_name = 'my_app'

urlpatterns = [
    url('^/register/', views.register, name='register'),
    url('^/user_login/', views.user_login, name='user_login'),
    url(r'^/users_list/$', views.UsersListView.as_view(), name='users_list'),
    url(r'^/users_list/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='detail'),
    url(r'^/users_list/update/(?P<pk>\d+)/$', views.UserUpdateView.as_view(), name='update'),
    url(r'^/users_list/delete/(?P<pk>\d+)/$', views.UserDeleteView.as_view(), name='delete')
]
