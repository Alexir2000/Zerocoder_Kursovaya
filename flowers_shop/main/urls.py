from django.urls import path
from django.contrib.auth import views as auth_views  # Импорт стандартных представлений аутентификации
from . import views
from .views import register, CustomLoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', next_page='index'), name='login'),  # Используйте стандартное представление
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Используйте стандартное представление выхода
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'),
]
