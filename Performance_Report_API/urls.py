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
from django.contrib import admin
from django.urls import path
from API.Report.views import top_view, login_view, index_view, panel_view, user_view, group_view, development_data_view, performance_data_view, return_data_view, statistical_rate_view, statistical_echarts_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # views
    path('', index_view),
    path('login/', login_view),
    path('index/', index_view),
    path('panel/', panel_view),
    path('user/', user_view),
    path('group/', group_view),
    path('development-data/', development_data_view),
    path('performance-data/', performance_data_view),
    path('return-data/', return_data_view),
    path('statistical-rate/', statistical_rate_view),
    path('statistical-echarts/', statistical_echarts_view),
    path('top/', top_view),

    # api
    url(r'^api/', include('API.Report.urls')),
]
