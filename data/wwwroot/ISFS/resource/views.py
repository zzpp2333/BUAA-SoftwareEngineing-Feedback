# from django.shortcuts import render
from .models import Resource
from django.http import HttpResponse
from course.views import isYourCourse
import json
# Create your views here.


def addResource(request):
    if request.method == 'POST':        
        course_id = request.POST.get('course_name')
        if not isYourCourse(request, course_id):
          return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')
          
        myFile = request.FILES.get("filepath", None)          
        if myFile == None:
          return HttpResponse(json.dumps({'res': 'No file!'}), content_type='application/json')
         
        else:                  
          resource_name = request.POST.get('resource_name')
          user = request.user
  
          re_resource = Resource.objects.filter(coid=course_id).filter(resource_name=resource_name)
          if len(re_resource) == 1:
            for i in re_resource:
              print("renew")
              i.filepath = myFile
              i.save()
            
          else:      
            resource = Resource(coid=course_id, author=user, resource_name=resource_name, filepath=myFile)
            resource.save()
  
          return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def getResource(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')

        resources = Resource.objects.filter(coid=course_id)
        resource_list = []
        for i in resources:
            path = i.filepath.path
            path = path[13:]
            resource_list.append({'resource_id': i.resource_id,
                                  'resource_name': i.resource_name,
                                  'filepath': path})

        res = {'num': len(resource_list),
               'resources': resource_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return
