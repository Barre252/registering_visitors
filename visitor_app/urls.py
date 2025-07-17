from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('login_page', views.login_page, name="login_page"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('register_visitor', views.register_visitor, name="register_visitor"),
    path('after_registration', views.after_registration, name="after_registration"),
    path('api/today-visits/', views.get_today_visits, name='api_today_visits')
]
