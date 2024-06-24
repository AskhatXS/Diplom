from django.urls import path
from . import views
from .views import unauthenticated

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('base/', views.base, name='base'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('create_test/', views.TestCreateView.as_view(), name='create_test'),
    path('add_questions/<int:test_id>/', views.add_questions, name='add_questions'),
    path('add_answers/<int:test_id>/<int:question_id>/', views.add_answers, name='add_answers'),
    path('edit_test/<int:test_id>/', views.edit_test, name='edit_test'),
    path('delete_test/<int:test_id>/', views.delete_test, name='delete_test'),
    path('retake_test/<int:test_id>/', views.retake_test, name='retake_test'),
    path('take_test/<int:test_id>/', views.take_test, name='take_test'),
    path('results/<int:user_id>/<int:test_id>/', views.test_results, name='test_results'),
    path('test_list/', views.test_list, name='test_list'),
    path('test_detail/<int:test_id>/', views.test_detail, name='test_detail'),
    path('unauthenticated/', unauthenticated, name='unauthenticated'),
]




