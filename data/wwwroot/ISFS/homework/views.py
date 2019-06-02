# from django.shortcuts import render
from .models import Homework
from course.models import Courses
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
import datetime 
from django.db.models import Max, Avg
from todolist.models import Todolist
from course.views import isYourCourse
# Create your views here.

  
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  

        else:  
            return json.JSONEncoder.default(self, obj) 


def addHomework(request):
    if request.method == 'POST':
        myFile = request.FILES.get("filepath", None)
        if myFile == None:
          is_file = 0
        else:
          is_file = 1

        course_id = request.POST.get('course')
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')
            
        homework_name = request.POST.get('homework_name')
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        user = request.user
        
        re_homework = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(is_valid=1)
        if len(re_homework) == 1:
          for i in re_homework:
            print("renew")
            if is_file == 1:
              i.filepath = myFile            
            i.content = content
            i.deadline = deadline
            i.save()
          
          
        else:
          course_num = Homework.objects.filter(coid=course_id).filter(is_valid=1)
          num = len(course_num) + 1
          is_valid = 1
          is_correct = 0
          grade = 0
  
          homework = Homework(coid=course_id, is_valid=is_valid, is_file=is_file, author=user,
                              homework_name=homework_name, content=content, is_correct = is_correct,
                              filepath=myFile, num=num, grade=grade, deadline=deadline)
          homework.save()
  
          # add the homework-todolist to every course_user
          course = Courses.objects.get(course_id=course_id)
          course_name = course.course_name
          list_content = course_name+homework_name
          list_time = deadline
          is_valid = 0
  
          students = []
          course_users = course.users.all()
          for course_user in course_users:
              permission = course_user.user.profile.permission
              if permission == 1 or permission == 3:
                  students.append(course_user.user)
  
          for i in students:
              todolist = Todolist(content=list_content, list_time=list_time, is_valid=is_valid, author=i)
              todolist.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def submitHomework(request):
    if request.method == 'POST':      
        myFile = request.FILES.get("filepath", None)
        if myFile == None:
          is_file = 0
        else:
          is_file = 1

        course_id = request.POST.get('course')
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')
            
        homework_name = request.POST.get('homework_name')
        content = request.POST.get('content')
        deadline = "2000-01-01 00:00:00"
        user = request.user

        re_homework = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(author_id=user.id)
        if len(re_homework) == 1:
          for i in re_homework:
            print("renew")
            if is_file == 1:
              i.filepath = myFile 
            i.content = content
            i.save()
          
        else:      
          homework = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(is_valid=1)
          for i in homework:
            num = i.num
            
          is_valid = 0
          is_correct = 0
          grade = 0
  
          homework = Homework(coid=course_id, is_valid=is_valid, is_file=is_file, author=user,
                              homework_name=homework_name, content=content, is_correct = is_correct,
                              filepath=myFile, num=num, grade=grade, deadline=deadline)
          homework.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def getHomework(request):
    if request.method == 'POST':
    
        course_id = request.POST.get('course')
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')

        homeworks = Homework.objects.filter(coid=course_id).filter(is_valid=1)
          
        nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        homework_list = []
        for i in homeworks:
            if i.is_file == 1:
              path = i.filepath.path
              path = path[13:]
            else:
              path = None
            
            d = i.deadline
            ddl = (d+datetime.timedelta(hours=8)).strftime("%Y%m%d%H%M%S")
            flag = int(nowtime) - int(ddl)
            if flag > 0:
              passed = 1
            else:
              passed = 0
            homework_list.append({'homework_id': i.homework_id,
                                  'homework_name': i.homework_name,
                                  'content': i.content,
                                  'filepath': path,
                                  'passed':passed,
                                  'is_file':i.is_file})

        res = {'num': len(homework_list),
               'homeworks': homework_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return


def checkHomework(request):
    if request.method == 'POST':
    
        course_id = request.POST.get('course')
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')
            
        homework_name = request.POST.get('homework_name')

        homeworks = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(is_valid=0)
        homework_list = []
        for i in homeworks:
            if i.is_file == 1:
              path = i.filepath.path
              path = path[13:]
            else:
              path = None
              
            homework_list.append({'homework_id': i.homework_id,
                                  'id':i.author_id,
                                  'homework_name': i.homework_name,
                                  'content': i.content,
                                  'filepath': path,
                                  'is_file':i.is_file,
                                  'is_correct':i.is_correct})

        res = {'num': len(homework_list),
               'homeworks': homework_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return


def getoneHomework(request):
    if request.method == 'POST':
    
        course_id = request.POST.get('course')
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')
            
        homework_name = request.POST.get('homework_name')      

        homeworks = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(is_valid=1)
        for i in homeworks:        
            if i.is_file == 1:
              path = i.filepath.path
              path = path[13:]
            else:
              path = None
              
            homework = {'content': i.content,
                        'filepath': path,
                        'deadline': i.deadline,
                        'is_file':i.is_file}

        return HttpResponse(json.dumps(homework, cls=DateEncoder),content_type='application/json')
    return


def Homeworkcontent(request):
    if request.method == 'POST':
        homework_id = request.POST.get('hw_id')      
        homework = Homework.objects.get(homework_id=homework_id)
        course_id = homework.coid
        if not isYourCourse(request, course_id):
            return HttpResponse(json.dumps({'msg': 'no permission'}), content_type='application/json')             
        content = {'content': homework.content}

        return HttpResponse(json.dumps(content),content_type='application/json')
    return


def correctHomework(request):
    if request.method == 'POST':
    
        homework_id = request.POST.get('homework_id')
        grade = request.POST.get('grade')

        is_correct = 1
        homework = Homework.objects.get(homework_id=homework_id)       
        homework.grade = grade
        homework.is_correct = is_correct
        homework.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


# 学生查看所有作业成�?
def getstudentGrade(request):
    if request.method == 'GET':
        user = request.user
        homeworks = Homework.objects.filter(author_id=user.id)

        grade_list = []
        for i in homeworks:
            course_id = i.coid
            course = Courses.objects.get(course_id=course_id)
            course_name = course.course_name
            grade_list.append({'course_name': course_name,
                               'course_num': i.num,
                               'grade': i.grade})

        return HttpResponse(json.dumps(grade_list), content_type='application/json')
    return


# 老师查看所有学生的每次成绩
def getteacherGrade(request):
    if request.method == 'GET':
        user = request.user
        course_user = user.course_user
        courses = course_user.course.all()
        course = list(courses)

        grade_list = []
        # 老师教授的课�?
        for i in course:
            course_name = i.course_name
            course_id = i.course_id

            homeworks = Homework.objects.filter(coid=course_id).filter(is_valid=0)
            # 该课程下的每一次作�?
            for j in homeworks:
                user_id = j.author_id
                
                homework_user = User.objects.get(id=user_id)
                name = homework_user.username
                grade_list.append({'course_name': course_name,
                                   'stu_name': name,
                                   'course_num': j.num,
                                   'grade': j.grade})

        return HttpResponse(json.dumps(grade_list), content_type='application/json')
    return


# 老师查看教授课程的最高分/平均�?
def teacherGrade(request):
    if request.method == 'GET':
        user = request.user
        course_user = user.course_user
        courses = course_user.course.all()
        course = list(courses)

        best_grade_list = []
        average_grade_list = []
        for i in course:
            course_name = i.course_name
            course_id = i.course_id
            homeworks = Homework.objects.filter(coid=course_id).filter(is_valid=0)

            best = homeworks.aggregate(Max('grade'))
            average = homeworks.aggregate(Avg('grade'))
            best_grade_list.append({'course_name': course_name,
                                    'grade': best['grade__max']})
            average_grade_list.append({'course_name': course_name,
                                       'grade': average['grade__avg']})

        res = {'best': best_grade_list,
               'average': average_grade_list,
               }
        return HttpResponse(json.dumps(res), content_type='application/json')
    return


# 学生查看每门课程的最高分/平均�?
def studentGrade(request):
    if request.method == 'GET':
        user = request.user
        course_user = user.course_user
        courses = course_user.course.all()
        course = list(courses)

        best_grade_list = []
        average_grade_list = []
        
        for i in course:

            course_name = i.course_name
            course_id = i.course_id
            homeworks = Homework.objects.filter(coid=course_id).filter(author_id=user.id)

            best = homeworks.aggregate(Max('grade'))
            average = homeworks.aggregate(Avg('grade'))
            best_grade_list.append({'course_name': course_name,
                                    'grade': best['grade__max']})
            average_grade_list.append({'course_name': course_name,
                                       'grade': average['grade__avg']})

        res = {'best': best_grade_list,
               'average': average_grade_list,
               }
        return HttpResponse(json.dumps(res), content_type='application/json')
    return
