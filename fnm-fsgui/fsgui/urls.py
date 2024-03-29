from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("network/", views.network, name="network"),
    path("network_delete/", views.network_delete, name="network_delete"),
    path("flowspec/", views.flowspec, name="flowspec"),
    path("flowspec_toggle/", views.flowspec_toggle, name="flowspec_toggle"),
    path("flowspec_delete/", views.flowspec_delete, name="flowspec_delete"),
    path("flowspec_flush/", views.flowspec_flush, name="flowspec_flush"),
    path("flowspec_redeploy/", views.flowspec_redeploy, name="flowspec_redeploy"),
    path("help/", views.help, name="help"),
]
