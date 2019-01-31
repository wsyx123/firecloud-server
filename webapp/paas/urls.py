from django.conf.urls import url
from webapp.paas.paas import Kubernetes,K8sOverview,K8sDetail
#idle host
from webapp.paas.paas import MesosIdleHostAdd,MesosIdleHostList,MesosIdleHostDelete
#mesos class
from webapp.paas.paas import MesosClusterList,MesosOverview,MesosAddCluster,MesosAddNode,ListNetwork,\
ListStorage,MesosDeployCluster,MesosDeleteNode,MesosDeleteCluster,MesosCleanCluster,\
MesosMasterDetail,MesosHaproxyDetail,MesosSlaveDetail,MesosMarathonDetail,MesosClusterDeployResult
#mesos func
from webapp.paas.paas import cluster_node_update,cluster_node_log

from webapp.paas.repository import RepositoryHostList,RepositoryImageList,\
RepositoryHostAdd,RepositoryHostDelete,repositor_refresh

urlpatterns = [
    url(r'^kubernetes/list/$',Kubernetes.as_view(),name='kubernetes'),
    url(r'kubernetes/detail/(?P<clsname>.+)/$',K8sDetail.as_view(),name='k8sdetail'),
    url(r'kubernetes/overview/(?P<clsname>.+)$',K8sOverview.as_view(),name='k8soverview'),
    #mesos
    url(r'^mesos/list/idle/$',MesosIdleHostList.as_view(),name='MesosIdleHostList'),
    url(r'^mesos/list/$',MesosClusterList.as_view(),name='MesosClusterList'),
    url(r'^mesos/list/node/log/$',cluster_node_log),
    url(r'^mesos/list/overview/(?P<clsname>.+)/$',MesosOverview.as_view(),name='MesosOverview'),
    url(r'^mesos/list/master/(?P<clsname>.+)/$',MesosMasterDetail.as_view(),name='MesosMasterDetail'),
    url(r'^mesos/list/marathon/(?P<clsname>.+)/$',MesosMarathonDetail.as_view(),name='MesosMarathonDetail'),
    url(r'^mesos/list/slave/(?P<clsname>.+)/$',MesosSlaveDetail.as_view(),name='MesosSlaveDetail'),
    url(r'^mesos/list/haproxy/(?P<clsname>.+)/$',MesosHaproxyDetail.as_view(),name='MesosHaproxyDetail'),
    url(r'^mesos/add/cluster/$',MesosAddCluster.as_view(),name='MesosAddCluster'),
    url(r'^mesos/add/deploy/$',MesosDeployCluster.as_view()),
    url(r'^mesos/add/clean/$',MesosCleanCluster.as_view()),
    url(r'^mesos/update/container/$',cluster_node_update),
    url(r'^mesos/delete/$',MesosDeleteCluster.as_view()),
    url(r'^mesos/add/deploy/result/$',MesosClusterDeployResult.as_view()),
    url(r'^mesos/add/node/$',MesosAddNode.as_view(),name='MesosAddNode'),
    url(r'^mesos/add/idle/$',MesosIdleHostAdd.as_view()),
    url(r'^mesos/delete/idle/(?P<pk>.+)$',MesosIdleHostDelete.as_view()),
    url(r'^mesos/delete/node/$',MesosDeleteNode.as_view()),
    
    
    url(r'^network/list/$',ListNetwork.as_view(),name='network'),
    url(r'^volume/list/$',ListStorage.as_view(),name='volume'),
    
    url(r'^repohost/list/$',RepositoryHostList.as_view(),name='RepositoryHostList'),
    url(r'^repohost/add/$',RepositoryHostAdd.as_view(),name='RepositoryHostAdd'),
    url(r'repohost/update/$',repositor_refresh),
    url(r'^repohost/delete/(?P<pk>.+)$',RepositoryHostDelete.as_view(),name='RepositoryHostDelete'),
    url(r'^repoimage/list/$',RepositoryImageList.as_view(),name='RepositoryImageList'),
]
