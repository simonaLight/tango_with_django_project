from django.conf.urls import url
from rango import views

app_name = 'rango'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page$', views.add_page, name='add_page'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^profile_registration/$', views.profile_registration, name='profile_registration'),
    url(r'^profile/(?P<username>[\w@\-]+)/$', views.profile, name='profile'),
    url(r'^delete/(?P<username>[\w@\-]+)/$', views.user_delete, name='user_delete'),
    url(r'^profiles/$', views.list_profiles, name='list_profile'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.log_out, name='logout'),
]
