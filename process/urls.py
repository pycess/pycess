from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.process_index, name='index'),
    url(r'^index_all_roles$', views.process_index_all_roles, name='index_all_roles'),
    
    url(r'^(?P<process_id>\d+)/?$', views.process_detail, name='detail'),
    url(r'^(?P<process_id>\d+)/create$',
        views.process_instance_create, name='instance_create'),
    url(r'^(?P<process_id>\d+)/(?P<instance_id>\d+)/?$',
        views.ProcessInstanceView.as_view(), name='instance_detail'),
]
