from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('base/', views.base, name='base'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('document/', views.document, name='document'),
    path('profile/', views.profile_view, name='profile'),
    path('create_test/', views.TestCreateView.as_view(), name='create_test'),
    path('add_questions/<int:test_id>/', views.add_questions, name='add_questions'),
    path('add_answers/<int:test_id>/<int:question_id>/', views.add_answers, name='add_answers'),
    path('delete_test/<int:test_id>/', views.delete_test, name='delete_test'),
    path('take_test/<int:test_id>/', views.take_test, name='take_test'),
    path('results/<int:user_id>/<int:test_id>/', views.test_results, name='test_results'),
    path('test_list/', views.test_list, name='test_list'),
    path('test_detail/<int:test_id>/', views.test_detail, name='test_detail'),
    path('delete_answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('user_profile/<int:pk>/', views.profile_view, name='profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('test/<int:test_id>/delete/', views.delete_test, name='delete_test'),
    path('article1/', views.article1, name='article1'),
    path('article2/', views.article2, name='article2'),
    path('article3/', views.article3, name='article3'),
    path('not_authorized', views.not_authorized, name='not_authorized'),
    path('about_us/', views.about_us, name='about_us'),
    path('about_survey/', views.survey, name='about_survey'),
    path('about_us2/', views.about_us2, name='about_us2'),
]







