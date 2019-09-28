"""Performance_Report_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path

from API.Report import views

urlpatterns = [
    # 页面数据
    path('person-group-name-data/', views.person_group_name_api),
    path('user-data/', views.person_data_api),
    path('group-data/', views.group_data_api),
    path('development-data/', views.development_data_api),
    path('return-data/', views.return_data_api),
    path('performance-data/', views.performance_data_api),

    # 数据计算
    path('statistical-rate-data/', views.data_conversion_rate),
    path('statistical-echarts-data/', views.statistical_echarts_data),

    # top榜
    path('top-data/', views.top_data_api),

    path('user-login/', views.user_login_api),
    path('user-logout/', views.logout_api),
    path('panel/', views.panel_api),
]
