import json
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.utils import timezone
from django.views.generic import View
from django.utils.translation import ugettext as _

from . import models
from .utils import LoginRequiredMixin

# Serialize process steps with https://github.com/jdorn/json-editor

# REFACT: introduce pagination
def process_index(request):
    processes = models.ProcessDefinition.objects.all()
    instances_by_process = dict(
        (process, process.instances.filter(currentstatus__role__role_instance__pycuser=request.user))
        for process in processes
    )
    return render(request, 'process/process_index.html', locals())

# REFACT: introduce pagination
def process_overview(request):
    if not request.user.is_staff:
        processes = models.ProcessDefinition.objects.all()
        instances_by_process = dict(
            (process, process.instances.filter(process__status_list__role__role_instance__pycuser=request.user))
            for process in processes
        )
    else: # show everything to admins
        processes = models.ProcessDefinition.objects.all()
        instances_by_process = dict((process, process.instances.all) for process in processes)
    return render(request, 'process/process_overview.html', locals())

def process_instance_create(request, process_id):
    process = get_object_or_404(models.ProcessDefinition, pk=process_id)
    instance = process.create_instance(request.user)
    return redirect('instance_detail', process_id=process.id, instance_id=instance.id)


class ProcessInstanceView(View):
    
    def get(self, request, process_id, instance_id):
        instance = get_object_or_404(models.ProcessInstance, pk=instance_id)
        json_schema = instance.currentstatus.step.json_schema
        current_json = instance.currentstatus.step.json_data(instance)
        return render(request, 'process/process_instance_detail.html', locals())
    
    def post(self, request, process_id, instance_id):
        instance = get_object_or_404(models.ProcessInstance, pk=instance_id)
        if request.user not in instance.responsible_users() and not request.user.is_staff:
            return self.get(request, process_id, instance_id)
        
        # FIXME: validate json and then update procdata with it
        instance.procdata = request.POST['json']
        # FIXME: validate requested_transition
        if 'requested_transition_id' in request.POST:
            status = get_object_or_404(models.StatusTransition, pk=request.POST['requested_transition_id'])
            instance.transition_with_status(status)
            # TODO: consider adding information. Who will be responsible, what time frame, perhaps even how to follow along?
            messages.success(request, _("Transitioned to status %(status_name)s: %(status_remark)s") 
                % dict(status_name=status.name, status_remark=status.remark) ) 
        else:
            # translators: Confirms that record was saved
            messages.info( request, _("Saved") )
        instance.save()
        
        if instance.currentstatus.is_editable_by_user(request.user):
            return self.get(request, process_id, instance_id)
        else:
            return redirect('index')
    
