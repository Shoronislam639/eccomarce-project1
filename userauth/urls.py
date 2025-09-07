from django.urls import path
from userauth import views

app_name = 'userauth'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.Login_view, name='sign-in'),
    path('log-out/', views.logout_view, name='log-out'),

]
