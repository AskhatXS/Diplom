from django.urls import path
from . import views
from .views import unauthenticated

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_test/', views.create_test, name='create_test'),
    path('edit_test/<int:test_id>/', views.edit_test, name='edit_test'),
    path('delete_test/<int:test_id>/', views.delete_test, name='delete_test'),
    path('retake_test/<int:test_id>/', views.retake_test, name='retake_test'),
    path('take_test/<int:test_id>/', views.take_test, name='take_test'),
    path('test_results/<int:test_id>/', views.test_results, name='test_results'),
    path('test_list/', views.test_list, name='test_list'),
    path('test_detail/<int:test_id>/', views.test_detail, name='test_detail'),
    path('unauthenticated/', unauthenticated, name='unauthenticated'),
]




