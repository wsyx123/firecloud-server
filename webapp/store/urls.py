from django.conf.urls import url
from store import ListWeb,ListLogic,ListStorage

urlpatterns = [
    url(r'^web/$', ListWeb.as_view(),name='listweb'),
    url(r'^logic/$', ListLogic.as_view(),name='listlogic'),
    url(r'^storage/$', ListStorage.as_view(),name='liststorage'),    
    
   
]
