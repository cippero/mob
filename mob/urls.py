from django.contrib import admin
from django.urls import path, include
from mob_tracker import views

urlpatterns = [
    path('admin/', admin.site.urls)
    ,path('', include('mob_tracker.urls'))
]
