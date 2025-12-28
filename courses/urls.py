from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:course_pk>/lesson/<int:lesson_pk>/', views.lesson_detail, name='lesson_detail'),
    path('create/', views.create_course, name='create_course'),
    path('edit/<int:pk>/', views.update_course, name='update_course'),
    path('manage/<int:pk>/', views.manage_course_content, name='manage_course_content'),
    path('course/<int:course_pk>/add_module/', views.add_module, name='add_module'),
    path('module/<int:module_pk>/add_lesson/', views.add_lesson, name='add_lesson'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('course/<int:course_pk>/add_quiz/', views.add_quiz, name='add_quiz'),
    path('quiz/<int:quiz_pk>/add_question/', views.add_question, name='add_question'),
    path('quiz/<int:quiz_pk>/add_question/', views.add_question, name='add_question'),
    path('certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
    path('enroll/<int:pk>/', views.enroll, name='enroll'),
    path('module/<int:pk>/edit/', views.edit_module, name='edit_module'),
    path('lesson/<int:pk>/edit/', views.edit_lesson, name='edit_lesson'),
]
