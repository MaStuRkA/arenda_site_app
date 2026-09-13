from django.urls import path
from .views import LoginUser, RegisterView, ResetPassword, EmailResetPassword, ChangePassword

app_name = 'account'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset_form/', EmailResetPassword.as_view(), name='reset_form'),
    path('reset/<str:email>/', ResetPassword.as_view(), name='reset_code'),
    path('reset_password/<str:email>/',ChangePassword.as_view(), name='change_password'), # придумать как обеспечить безопасность
]