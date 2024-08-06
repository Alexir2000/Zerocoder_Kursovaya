from django.urls import path
from django.contrib.auth import views as auth_views  # Импорт стандартных представлений аутентификации
from . import views
from .views import register, CustomLoginView, custom_logout_view, user_kabinet, repeat_order

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Используем кастомное представление для входа
    path('logout/', custom_logout_view, name='logout'),  # Используем кастомное представление для выхода
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'),
    path('user_kabinet/', user_kabinet, name='user_kabinet'),
    path('repeat_order/<int:order_id>/', repeat_order, name='repeat_order'),  # Маршрут для повторения заказа
]