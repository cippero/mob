from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index')
	,path('login/', views.login_view, name="login")
	,path('logout/', views.logout_view, name="logout")
	,path('profile/', views.profile_view, name="profile")
	# ,path('<int:pk>/', views.party_detail, name='party_detail')
	# ,path('post_party/', views.PartyPost.as_view(), name="post_party")
]