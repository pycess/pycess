from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.process_index, name='index'),
    url(r'^overview$', views.process_overview, name='overview'),
    
    url(r'^(?P<process_id>\d+)/create$',
        views.process_instance_create, name='instance_create'),
    url(r'^(?P<process_id>\d+)/(?P<instance_id>\d+)/?$',
        views.ProcessInstanceView.as_view(), name='instance_detail'),
    
    url('^accounts/', include('django.contrib.auth.urls')),
]


