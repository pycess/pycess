from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from process.models import *
from django.utils import timezone
from django.views.generic import View
from datetime import datetime
import json

# Serialize process steps with https://github.com/jdorn/json-editor


def process_index(request):
    processes = ProcessDef.objects.all()
    return HttpResponse(render(request, 'process/index.html', locals()))


def process_detail(request, process_id):
    process = get_object_or_404(ProcessDef, pk=process_id)
    return HttpResponse(render(request, 'process/detail.html', locals()))


def process_instance_create(request, process_id):
    process = get_object_or_404(ProcessDef, pk=process_id)
    instance = ProcInstance.objects.create(
        process=process,
        currentstep=process.first_step(),
        procdata=json.dumps({}), # FIXME: set initial data
        starttime=timezone.now(),
        stoptime=timezone.now(),
        status=3)
    return redirect('instance_detail', process_id=process.id, instance_id=instance.id)


class ProcessInstanceView(View):
    
    def get(self, request, process_id, instance_id):
        instance = get_object_or_404(ProcInstance, pk=instance_id)
        print(instance.procdata)
        current_json = instance.currentstep.json_data(instance)
        return HttpResponse(render(request, 'process/instance_index.html', locals()))
    
    def post(self, request, process_id, instance_id):
        instance = get_object_or_404(ProcInstance, pk=instance_id)
        # TODO: validate json
        instance.procdata = request.POST['json']
        instance.save()
        return self.get(request, process_id, instance_id)
    