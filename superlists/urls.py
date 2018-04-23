"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from lists import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    re_path(r'^$', views.home_page, name='home'),
    re_path(r'^lists/new$', views.new_list, name='new_list'),
    # 我们调整URL的正则表达式以包含捕获组， 该捕获组(.+)将匹配任何字符，
    # 直至以下内容/。捕获的文本将作为参数传递给视图。
    re_path(r'^lists/(\d+)/$', views.view_list, name='view_list'),
    re_path(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),
]
