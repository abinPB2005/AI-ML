"""
URL configuration for waterQ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),

# ------------------------admin-------------------------------------


    path('admin_home/',views.admin_home),
    path('admin_view_user/',views.admin_view_user),
    path('admin_view_predictions/',views.admin_view_predictions),


    path('admin_view_complaints/',views.admin_view_complaints),
    path('reply/<id>',views.reply),
    path('reply_post/',views.reply_post),
    path('admin_view_feedback/',views.admin_view_feedback),




# ------------------------user--------------------------------------

    path('user_register/',views.user_register),
    path('user_reqister_post/',views.user_reqister_post),
    path('user_home/',views.user_home),
    path('view_user_profile/',views.view_user_profile),
    path('edit_user_profile/',views.edit_user_profile),
    path('edit_user_profile_post/',views.edit_user_profile_post),

    path('check_quality/',views.check_quality),
    path('check_quality_post/',views.check_quality_post),
    path('result/',views.result),

    path('user_add_complaints/',views.user_add_complaints),
    path('user_add_complaints_post/',views.user_add_complaints_post),
    path('user_view_complaint/',views.user_view_complaint),

    path('user_add_feedback/',views.user_add_feedback),
    path('user_add_feedback_post/',views.user_add_feedback_post),
    path('user_view_feedback/',views.user_view_feedback),








]
