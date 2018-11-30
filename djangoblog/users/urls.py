from .import views
from django.urls import path,include
from django.conf.urls import url


# Authentication urls
urlpatterns  = [
                    url(r'^register/',views.register,name='register'),
                    url(r'^login/', views.login,name='login'),
                    url(r'^logout/', views.logout,name='logout'),
                    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
                    url(r'^forgot_pass/', views.forgot_password,name='forgot_pass'),
                    url(r'^change_pass/', views.change_password,name='change_pass'),
                    url(r'^req_chang_pass/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.req_chang_pass, name='req_chang_pass'),
                ]