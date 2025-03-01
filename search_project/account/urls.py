from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name ='account'

urlpatterns=[
	path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='search_app:search_view'), name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]