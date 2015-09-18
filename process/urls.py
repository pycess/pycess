from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from lazysignup.decorators import allow_lazy_user

from . import views

urlpatterns = [
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^convert/', include('lazysignup.urls')),
    
    url(r'^$', allow_lazy_user(views.process_index), name='index'),
    url(r'^overview$', allow_lazy_user(views.process_overview), name='overview'),
    url(r'^(?P<process_id>\d+)/create$',
        login_required(views.process_instance_create), name='instance_create'),
    url(r'^(?P<process_id>\d+)/(?P<instance_id>\d+)/?$',
        login_required(views.ProcessInstanceEditView.as_view()), name='instance_detail'), # REFACT rename instance_edit
]


