from django.urls import path
from . import views

# urlConf
urlpatterns = [
    path('', views.index, name='index'),
    path('homepage', views.homepage, name='homepage'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('signup', views.signup, name='signup'),
    path('user_login', views.user_login, name='user_login'),
    path('logout', views.logout, name='logout'),
    path('delete_post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    # path('wink/<int:pk>', views.wink, name='wink'),
    # path('nu_context_for_wink', views.nu_context_for_winks, name='context_wink')
]
