# from django.shortcuts import render
from .models import Todolist
from django.http import HttpResponse
import json
# Create your views here.


def addlist(request):
    if request.method == 'POST':
        list_content = request.POST.get('list_content')
        list_time = request.POST.get('list_time')
        user = request.user
        is_valid = 0

        todolist = Todolist(content=list_content, list_time=list_time, is_valid=is_valid, author=user)
        todolist.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def getlist(request):
    if request.method == 'GET':
        user = request.user
        lists = Todolist.objects.filter(author_id=user.id)

        todo_list = []
        for i in lists:
            todo_list.append({'list_id': i.list_id,
                              'list_content': i.content,
                              'list_time': i.list_time,
                              'is_valid': i.is_valid})

        res = {'num': len(todo_list),
               'lists': todo_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return


def finishlist(request):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        is_valid = 1

        todolist = Todolist.objects.get(list_id=list_id)
        todolist.is_valid = is_valid
        todolist.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return
