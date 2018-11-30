from .import views
from django.urls import path,include
from django.conf.urls import url

app_name = 'frontend'

# Authentication urls
urlpatterns  = [
                    url(r'^home/',views.home,name='home'),
                    url(r'^user_profile/',views.user_profile,name='user_profile'),
                    url(r'^add_post/',views.add_post,name='add_post'),
                    url(r'^add_details/(?P<ref_id>\d+)$',views.add_details,name='add_details'),
                    url(r'^likes_dislikes/',views.likes_dislikes,name='likes_dislikes'),
                   
                ]