from django.contrib import admin
from django.urls import path
from login import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.register_student, name='signup'),
    path('login/', views.login_student, name='login'),
    path('home/', views.home, name='home'),
    path('data/', views.data_page, name='data'),
    path('data/verify/', views.verify_data_access, name='verify_data_access'),
    path('get_student_data/', views.get_student_data, name='get_student_data'),
]