from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),#index page
    url(r'^login/auth/$', views.auth_view),#logic for login authentication
    url(r'^loggedin/in/$', views.loggedin_view),
    url(r'^register/$', views.register_view),#register page
    url(r'^registered/$', views.registered_view),
    url(r'^logged/$', views.loggedin_view),

    #dashboard urls-----------------------------------------
    url(r'^dash/$', views.dash_view),# dashboard view/page
    url(r'^gophish/$', views.phish_view),#function to send an attack
    url(r'^gophish/hooked/(?P<user_id>[0-9]+)/$', views.record_click_view),#this is function that records the view
    url(r'^logout/$', views.logout_view),#logic for logging a user out
    #user stuff urls-------------------------------------------
    url(r'^user/$', views.users_view),
    url(r'^new_user/$', views.new_user_view),#to add new user
    url(r'^adduser/$', views.add_user_view),#logic for adding a new user
    url(r'^user_list/$', views.user_list_view),#shows list of users
    url(r'^btngroup/$', views.btngroup_view),#add group
]




