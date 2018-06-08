from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index')
	,path('login/', views.login_view, name="login")
	,path('logout/', views.logout_view, name="logout")
	,path('signup/', views.signup_view, name="signup")
	,path('user/<username>/', views.profile_view, name='profile')
	,path('entry/<entry_title>/', views.entry_view, name='entry')
	,path('tip/<entry_title>/', views.tip_view, name='tip')
	,path('tip/<t>/vote/<p>', views.tip_vote_view, name='tip')
]