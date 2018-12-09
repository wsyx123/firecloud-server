from django.conf.urls import url
from webapp.paas.paas import Kubernetes,K8sOverview,K8sDetail,\
Mesos,MesosOverview,MesosDetail,MesosCreate,MesosAdd,ListNetwork,ListStorage,RepoHost,RepoImage

urlpatterns = [
    url(r'^kubernetes/list/$',Kubernetes.as_view(),name='kubernetes'),
    url(r'kubernetes/detail/(?P<clsname>.+)/$',K8sDetail.as_view(),name='k8sdetail'),
    url(r'kubernetes/overview/(?P<clsname>.+)$',K8sOverview.as_view(),name='k8soverview'),
    #mesos
    url(r'^mesos/detail/(?P<clsname>.+)$',MesosDetail.as_view(),name='mesosdetail'),
    url(r'^mesos/overview/(?P<clsname>.+)/$',MesosOverview.as_view(),name='mesosoverview'),
    url(r'^mesos/create/$',MesosCreate.as_view(),name='mesoscreate'),
    url(r'^mesos/add/$',MesosAdd.as_view(),name='mesosadd'),
    url(r'^mesos/list/$',Mesos.as_view(),name='mesos'),
    
    url(r'^network/list/$',ListNetwork.as_view(),name='network'),
    url(r'^volume/list/$',ListStorage.as_view(),name='volume'),
    
    url(r'^repohost/list/$',RepoHost.as_view(),name='repohost'),
    url(r'^repoimage/list/$',RepoImage.as_view(),name='repoimage'),
]
