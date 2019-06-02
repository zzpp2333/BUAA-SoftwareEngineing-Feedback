# from django.shortcuts import render
from .models import Resource
from django.http import HttpResponse
import json
# Create your views here.


def addResource(request):
    if request.method == 'POST':
        myFile = request.FILES.get("filepath", None)

        course_id = request.POST.get('course_name')
        resource_name = request.POST.get('resource_name')
        user = request.user

        resource = Resource(coid=course_id, author=user, resource_name=resource_name, filepath=myFile)
        resource.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def getResource(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')

        resources = Resource.objects.filter(coid=course_id)
        resource_list = []
        for i in resources:
            resource_list.append({'resource_id': i.resource_id,
                                  'resource_name': i.resource_name,
                                  'filepath': i.filepath.path})

        res = {'num': len(resource_list),
               'resources': resource_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return
