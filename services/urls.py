from django.conf.urls import url
from . import views

#------------------------resused stuff
#adding obj
#removing obj
#Saving obj
urlpatterns = [
    #index urls----------------------------------------------------------------------------------------
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),#index page

    #login/register urls----------------------------------------------------------------------------------------
    url(r'^login/auth/$', views.auth_view),#logic for login authentication
    ##url(r'^loggedin/in/$', views.loggedin_view),#points to dash
    url(r'^logout/$', views.logout_view),  # logic for logging a user out
    url(r'^register/$', views.register_view),#register page
    url(r'^registered/$', views.registered_view),

    url(r'^confirm/$', views.registered_view),
    url(r'^confirm/(?P<user_id>[\w\-]+)/$', views.email_confirm) , # logic for reseting vulnerability status
    url(r'^not_confirmed//$', views.not_confirmed_view),
    #dashboard urls----------------------------------------------------------------------------------------

    url(r'^dash/$', views.dash_view),# dashboard view/page
    url(r'^reset/(?P<user_id>[\0-9]+)/$', views.reset_view) , # logic for reseting vulnerability status
    url(r'^details/(?P<click_id>[0-9]+)/$', views.detail_view),  # logic for reseting vulnerability status
    #url(r'^details/$', views.detail_page_view),
    url(r'^remove/(?P<click_id>[0-9]+)/$', views.remove_view),  # logic for reseting vulnerability status
    url(r'^gophish/$', views.phish_view),  # function to send an attack
    # url(r'^gophish/hooked/(?P<user_id>[0-9]+)/$', views.record_click_view),#this is function that records the view
    url(r'^gophish/hooked/(?P<user_id>[\w\-]+)/$', views.record_click_view),
    url(r'^gophish/hook/(?P<url_id>[\w\-]+)/(?P<page_id>[0-9]+)/$', views.campaign_click_view),



    #email template---------------------------------------------------------------------------------------
    #url(r'^send/$', views.email_send),  # dashboard view/page
    url(r'^send/$', views.email_sender),  # dashboard view/page
    #url(r'^sender/$', views.email_sender),  # dashboard view/page

    # campaign urls---------------------------------------------------------------------------------------
    url(r'^campaign/$', views.campaign_view),
    url(r'^campaign/new/$', views.new_campaign_view),
    url(r'^campaign/add/$', views.add_campaign_view),
    url(r'^campaign/save/$', views.save_campaign_view),
    url(r'^campaign/remove/(?P<campaign_id>[0-9]+)/$', views.campaign_remove_view),
    url(r'^campaign/remove/group/(?P<campaign_id>[0-9]+)/(?P<group_id>[0-9]+)/$', views.campaign_remove_group_view),

    url(r'^campaign/results/(?P<campaign_id>[0-9]+)/$', views.campaign_results_view),#campaing results
    url(r'^campaign/config/(?P<campaign_id>[0-9]+)/$', views.campaign_config_view),#campaing details--groups and such
    url(r'^campaign/start/(?P<campaign_id>[0-9]+)/$', views.campaign_start_view),#campaing
    url(r'^set/profile/landing/(?P<campaign_id>[0-9]+)/$', views.set_profile_landing_view),#campaing
    url(r'^campaign/stop/(?P<campaign_id>[0-9]+)/$', views.campaign_stop_view),#campaing
    #url(r'^campaign/details/(?P<campaign_id>[0-9]+)/$', views.campaign_details_view),#campain config

    #url(r'^campaign/new/group/(?P<campaign_id>[0-9]+)/$', views.add_camp_group_view),
    url(r'^campaign/new/group/(?P<campaign_id>[0-9]+)/$', views.new_group_view),
    url(r'^campaign/group/import/(?P<campaign_id>[0-9]+)/$', views.import_group_view),#import group
    url(r'^group/import/(?P<campaign_id>[0-9]+)/(?P<group_id>[0-9]+)/$', views.group_import_view),#import group


    url(r'^campaign/details/users/(?P<group_id>[0-9]+)/$', views.campign_users_view),
    url(r'^campaign/new/user/(?P<group_id>[0-9]+)/$', views.new_user_view), #crate new group user
    url(r'^campaign/user/import/(?P<campaign_id>[0-9]+)/$', views.import_user_view),#import users
    url(r'^campaign/user/details/(?P<group_id>[0-9]+)/(?P<user_id>[0-9]+)/$', views.campign_users_detail_view),
    # group stuff urls-------------------------------------------
    url(r'^groups/$', views.group_view),
    url(r'^groups/new/$', views.new_group_view), #   new group page
    url(r'^groups/add/$', views.add_group_view),  # logic to add new user profile/done/"
    url(r'^groups/details/(?P<group_id>[0-9]+)/$', views.group_detail_view),
    # user stuff urls-------------------------------------------
    url(r'^user/$', views.users_view),
    url(r'^user/new/$', views.new_user_view),  # to add new user
    url(r'^user/add/$', views.add_user_view),  # logic for adding a new user
    #url(r'^user_list/$', views.user_list_view),  # shows list of users
    #url(r'^btngroup/$', views.btngroup_view),  # add group


    #landing page urls---------------------------------------------------------------------------------------
    url(r'^langing/$', views.landing_pages),
    url(r'^landing/new/$', views.new_page),
    url(r'^landing/add/$', views.add_landing_pages),
    url(r'^addpage/$',views.add_landing_pages),

    # sending profiles stuff urls-------------------------------------------
    url(r'^profiles/$', views.profile_view),
    url(r'^profiles/new/$', views.new_profile),
    url(r'^profiles/add/$', views.add_profile),
    url(r'^profiles/details/(?P<profile_id>[\w\-]+)$', views.profile_details_view),
    url(r'^profiles/edit/(?P<profile_id>[\w\-]+)$', views.edit_profile_view),

    url(r'^profile/done/$', views.done_profile),

    url(r'^profile/done/$', views.done_profile),

    url(r'^print/$', views.see),

    #Popular urls---------------------------------------------------------------------------------------
    # My profile urls---------------------------------------------------------------------------------------
    url(r'^userprofile/$', views.user_profile),
    url(r'^saveprofile/$', views.save_user_profile),
    url(r'^test/$', views.test_mail),
]
