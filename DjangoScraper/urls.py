"""DjangoScraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from app.views import HomePage, DashboardPage
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePage.as_view()),
    url(r'^dashboard/', DashboardPage.as_view(), name='dashboard'),
    url(r'^ajax/unsubscribe/', views.ajax_unsubscribe, name='unsubscribe'),
    url(r'^ajax/subscribe/', views.ajax_subscribe),

    url(r'^ajax/filter/', views.ajax_filter, name='ajax_filter'),
    url(r'^ajax/get/', views.ajax_get_news, name='ajax_get_news'),
    url(r'^ajax/submit-report/', views.submit_report, name='submit_report'),
    url(r'^ajax/report-weekly-news/', views.report_weekly_news, name='report-weekly-news'),
    url(r'^ajax/get-subscribers/', views.ajax_get_subscribers),
    url(r'^ajax/run-crawl/', views.ajax_run_crawl),


    url(r'^news/', views.NewsList.as_view()),
    url(r'^ajax/edit-news/', views.NewsUpdate.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
