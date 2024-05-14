"""
URL configuration for CinemaApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from cinema.views import views, api_views, admin_views, client_views
from django.views.generic.base import TemplateView
from cinema.views.views import *

from django.conf.urls.static import static
from django.conf import settings


from django.contrib.auth import views as auth_views
from cinema.views import account_views, views, pages


urlpatterns = [



    path('admin/', admin.site.urls),
    # path('register/', UserRegistrationView.as_view(), name='register'),
    # path('login/', UserAuthorizationView.as_view(), name='login'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),

    # path('', TemplateView.as_view(template_name='cinema/home.html'), name='home'),

    
    path('', include('cinema.urls')),
    # path('cinema/', include('django.contrib.auth.urls')),


    # path('', views.index, name='home')
    # path('', views.index_last_session, name='home'),
    re_path(r'^accounts/register/$', account_views.register, name='register'),
    re_path(r'^accounts/login/$', account_views.login, name='login'),
    re_path(r'^accounts/logout/$', account_views.logout, name='logout'),
    re_path(r'^accounts/profile/$', account_views.profile, name='profile'),
    re_path(r'^main/$', views.index_last_session, name='main'),
    re_path(r'^about/$', views.about_company, name='about'),


    re_path(r'^news/$', api_views.news, name='news'),
    re_path(r'^cat_facts/$', api_views.cats, name='cats'),


    re_path(r'^faq/$', views.terms, name='faq'),
    re_path(r'^contacts/$', views.contacts, name='contacts'),
    re_path(r'^vacancies/$', views.vacancies, name='vacancies'),
    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^add_review/$', views.add_review, name='add_review'),
    re_path(r'^coupons/$', views.coupons, name='coupons'),

    path('', pages.home, name='home'),


    #Client
    re_path(r'^tickets/$', client_views.to_tickets, name='to_tickets'),


    #Admin panel
    re_path(r'^home_admin/$', admin_views.to_admin, name='to_admin'),
    re_path(r'^list_movies_admin/$', admin_views.index_admin_movies, name='index_admin_movies'),
    re_path(r'^list_tickets_admin/$', admin_views.index_admin_tickets, name='index_admin_tickets'),
    re_path(r'^list_sessions_admin/$', admin_views.index_admin_sessions, name='index_admin_sessions'),
    re_path(r'^list_halls_admin/$', admin_views.index_admin_halls, name='index_admin_halls'),
    re_path(r'^list_employees_admin/$', admin_views.index_admin_employees, name='index_admin_employees'),
    re_path(r'^add_movie_admin/$', admin_views.movie_new, name='movie_new'),
    # re_path(r'^edit_movie_admin/(?P<pk>\d+)/$', admin_views.movie_edit, name='movie_edit'),
    re_path(r'^edit_movie_admin/$', admin_views.movie_edit, name='movie_edit'),
    re_path(r'^delete_movie_admin/$', admin_views.movie_delete, name='movie_delete'),
    re_path(r'^add_ticket_admin/$', admin_views.ticket_new, name='ticket_new'),
    re_path(r'^edit_ticket_admin/$', admin_views.ticket_edit, name='ticket_edit'),
    re_path(r'^delete_ticket_admin/$', admin_views.ticket_delete, name='ticket_delete'),
    re_path(r'^add_session_admin/$', admin_views.session_new, name='session_new'),
    re_path(r'^edit_session_admin/$', admin_views.session_edit, name='session_edit'),
    re_path(r'^delete_session_admin/$', admin_views.session_delete, name='session_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)