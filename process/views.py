from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from process.models import *
from django.utils import timezone
from django.views.generic import View
from datetime import datetime
import json

# Serialize process steps with https://github.com/jdorn/json-editor

# REFACT: introduce some sort of pagination?
def process_index(request):
    processes = ProcessDefinition.objects.all()
    instances_by_process = dict(
        (process, process.instances.filter(currentstep__role__role_instance__pycuser=request.user))
        for process in processes
    )
    return HttpResponse(render(request, 'process/process_index.html', locals()))

# REFACT: introduce some sort of pagination?
def process_overview(request):
    processes = ProcessDefinition.objects.all()
    instances_by_process = dict(
        (process, process.instances.filter(process__steps__role__role_instance__pycuser=request.user))
        for process in processes
    )
    return HttpResponse(render(request, 'process/process_overview.html', locals()))

def process_instance_create(request, process_id):
    process = get_object_or_404(ProcessDefinition, pk=process_id)
    # REFACT: use process.create_instance(creator=request.user)?
    instance = ProcessInstance.objects.create(
        process=process,
        currentstep=process.first_transition(),
        procdata=json.dumps({}), # FIXME: set initial data from somewhere
        starttime=timezone.now(),
        stoptime=timezone.now(),
        status=3)
    return redirect('instance_detail', process_id=process.id, instance_id=instance.id)


class ProcessInstanceView(View):
    
    def get(self, request, process_id, instance_id):
        instance = get_object_or_404(ProcessInstance, pk=instance_id)
        json_schema = instance.currentstep.json_schema
        current_json = instance.currentstep.json_data(instance)
        return HttpResponse(render(request, 'process/process_instance_detail.html', locals()))
    
    def post(self, request, process_id, instance_id):
        instance = get_object_or_404(ProcessInstance, pk=instance_id)
        # FIXME: validate json and then update procdata with it
        instance.procdata = request.POST['json']
        # FIXME: validate requested_transition
        if 'requested_transition_id' in request.POST:
            status = get_object_or_404(StatusScheme, pk=request.POST['requested_transition_id'])
            instance.transition_with_status(status)
            # TODO: consider adding information. Who will be responsible, what time frame, perhaps even how to follow along?
            messages.success(request, "Transitioned to status %s: %s" % (status.name, status.remark))
        else:
            messages.info(request, "Saved")
        instance.save()
        
        if instance.currentstep.is_editable_by_user(request.user):
            return self.get(request, process_id, instance_id)
        else:
            return redirect('index')
    