from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('instruction/', views.Instruction.as_view(), name='instruction'),

]