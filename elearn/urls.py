from . import views
from django.urls import path, include
from django.views.generic import TemplateView 
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('', TemplateView.as_view(template_name="elearn/index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_request, name= 'logout'),
    path('signup/', views.signup_request, name='signup'),
    path('login/', views.login_request, name='login'),
    path('about/', views.about, name='about'),
    path('delete/<int:id>',views.deletenoti, name='deletenoti'),
    
    path('courselist/', views.courselist, name='courselist'),
    path('createsubject/', views.createsubject, name='createsubject'),
    path('upload/file/', views.uploadfile, name='uploadfile'),
    path('upload/video/', views.uploadvideo, name='uploadvideo'),
    path('courselists/<int:subjectid>', views.eachsubject, name='eachsubject'),
    path('addcomment/<int:subjectid>', views.commenteachsubject, name='commenteachsubject'),
    
    path('courselist/<int:subjectid>', views.bookcourselist, name='bookcourselist'),
    path('searchcourse/', views.searchcourse, name='searchcourse'),
    path('searcheachsubject/<int:subjectid>', views.searcheachsubject, name='searcheachsubject'),
    path('profile/edit/', views.editprofile, name='editprofile'),
    # path('upload/video/inprogress', views.savevideo, name='savevideo'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="elearn/password/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="elearn/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="elearn/password/password_reset_complete.html"), name='password_reset_complete'),   
    # path('password_reset/', views.password_reset_request, name='password_reset'), 
]