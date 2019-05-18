from django.conf.urls import url
from views import WebList,WebCreate,WebDetail,LogicList,StorageList

urlpatterns = [
    url(r'^web/list/$', WebList.as_view(),name='WebList'),
    url(r'^web/create/$', WebCreate.as_view(),name='WebCreate'),
    url(r'^web/detail/$', WebDetail.as_view(),name='WebDetail'),
    url(r'^logic/list/$', LogicList.as_view(),name='LogicList'),
    url(r'^storage/list/$', StorageList.as_view(),name='StorageList'),    
    
   
]
