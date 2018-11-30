from .import views
from django.urls import path,include
from django.conf.urls import url

app_name = 'dahboard'

# Authentication urls
urlpatterns  = [
                    url(r'',views.home,name='home'),
                ]