from django.shortcuts import render
from .models import Courses, CourseUsers, AssistantApplication, Assistants
from users.models import User, UserProfile
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

# Create your views here.


def test(request):
    # user = User.objects.get(id=8)
    # course_user = Course_users(user=user)
    # course_user.save()

    # course = Courses(course_name="this is a test", is_valid=0)
    # course.save()
    # course = Courses(course_name="this is a test2", is_valid=1)
    # course.save()

    course = Courses.objects.first()
    course_user = CourseUsers.objects.first()
    course.users.add(course_user)
    course_user.course.add(course)

    return HttpResponse(json.dumps({'emm': 'emmm'}), content_type='application/json')


def test2(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # teacher = Teachers(user=user)
    # teacher.save()
    return HttpResponse(json.dumps({'emm': 'emmmmm'}), content_type='application/json')


def addCourse(request):
    if(request.method == 'POST'):
        course_name = request.POST['name']
        details = request.POST['details']
        course_time = request.POST['course_time']
        course_loc = request.POST['course_loc']
        teacher_name = request.POST['teacher_name']

        is_valid = 0
        course = Courses(course_name=course_name, is_valid=is_valid, details=details, course_time=course_time, course_loc=course_loc, teacher_name=teacher_name)
        course.save()

        user_id = request.user.id
        user = User.objects.get(id=user_id)
        course_user = user.course_user

        course.users.add(course_user)
        course_user.course.add(course)

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    return render(request, 'courses/testAddCourse.html')


def getCourses(request):
    if(request.method == 'GET'):
        # user_id = request.session['id']
        user_id = request.user.id
        print(user_id)
        user = User.objects.get(id=user_id)
        permission = user.profile.permission

        if permission == 4:
            courses = Courses.objects.all().values('course_id', 'course_name', 'is_valid', 'course_time', 'course_loc', 'teacher_name')
        else:
            course_user = user.course_user
            courses = course_user.course.values('course_id', 'course_name', 'is_valid', 'course_time', 'course_loc', 'teacher_name')
        # print(courses)
        # print(list(courses))
        # data = serializers.serialize('json', courses)
        # print(data)

        data = list(courses)

        res = {'num': len(data), 'courses': data, 'name': user.username}

        if permission == 3:
            assistant = user.course_assistant
            a_courses = assistant.course.values('course_id', 'course_name')
            a_data = list(a_courses)

            courses_all = Courses.objects.all().values('course_id', 'course_name', 'is_valid')
            data_all = list(courses_all)

            res = {'num': len(data), 'courses': data, 'a_num': len(a_data), 'a_courses': a_data, 'all_num': len(data_all), 'all_courses': data_all, 'name': user.username}

        return HttpResponse(json.dumps(res), content_type='application/json')


def applyAssistant(request):
    if request.method == 'POST':
        user_id = request.user.id
        # user_id = request.session['id']
        user = User.objects.get(id=user_id)

        course_id = request.POST['course_id']
        course = Courses.objects.get(course_id=course_id)

        application = AssistantApplication(course=course, user=user)

        application.save()

        return HttpResponse(json.dumps({'user_id': application.user.id, 'course_id': application.course.course_id}), content_type='application/json')
    return render(request, 'courses/testApplyAssist.html')


def getAssistApplications(request):
    if request.method == 'GET':
        course_id = request.GET['course_id']
        # course_id = 10
        course = Courses.objects.get(course_id=course_id)

        applications = AssistantApplication.objects.filter(course=course).values('id', 'course_id', 'user_id')
        # print(list(applications))

        return HttpResponse(json.dumps(list(applications)), content_type='application/json')


def relateAssistant(request):
    if request.method == 'POST':
        application_id = request.POST['application_id']
        application = AssistantApplication.objects.get(id=application_id)

        course = application.course
        user = application.user

        if user.profile.permission == 1:
            user.profile.permission = 3
            user.profile.save()

        if user.profile.permission == 3:

            assistant = Assistants.objects.filter(user=user)

            if assistant.count() == 0:
                assistant = Assistants(user=user)
                assistant.save()
            else:
                assistant = assistant[0]

            course.assistants.add(assistant)
            assistant.course.add(course)

            application.delete()

            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    return render(request, 'courses/testRelateAssist.html')


def getCourseUsers(request):
    if request.method == 'GET':
        teachers = []
        students = []
        assistants = []
        course_id = request.GET['course_id']
        # course_id = 10
        course = Courses.objects.get(course_id=course_id)

        course_users = course.users.all()
        # profile = UserProfile.objects.filter(user_id__in=list(students)).values('permission')
        for course_user in course_users:
            permission = course_user.user.profile.permission
            if permission == 1 or permission == 3:
                students.append(course_user.user)
            elif permission == 2:
                teachers.append(course_user.user)

        course_assistants = course.assistants.all()
        for course_assistant in course_assistants:
            assistants.append(course_assistant.user)

        # print('-----')
        # print(students)
        # print('-----')
        # print(teachers)
        # print('-----')
        # print(assistants)

        student_infos = []
        for student in students:
            student_info = {
                'username': student.username,
                'no': student.profile.no
            }
            student_infos.append(student_info)
        # print(student_infos)

        teacher_infos = []
        for teacher in teachers:
            teacher_info = {
                'username': teacher.username,
                'no': teacher.profile.no
            }
            teacher_infos.append(teacher_info)

        assistant_infos = []
        for assistant in assistants:
            assistant_info = {
                'username': assistant.username,
                'no': assistant.profile.no
            }
            assistant_infos.append(assistant_info)

        return HttpResponse(json.dumps({'students': student_infos, 'teachers': teacher_infos, 'assistants': assistant_infos}), content_type='application/json')


def getss(request):
    if request.method == 'GET':
        # user_id = request.session['id']
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.profile.permission == 4:
            ss_profiles = UserProfile.objects.filter(permission__in=[1, 3])
            ss = User.objects.filter(profile__in=ss_profiles)

            ss_infos = list(ss.values('id', 'username'))
            for ss_info in ss_infos:
                ss_info['no'] = User.objects.get(id=ss_info['id']).profile.no
            # print(ss_infos)

            return HttpResponse(json.dumps(ss_infos), content_type='application/json')
        elif user.profile.permission == 2:
            # course_id = request.POST['course_id']
            course_id = 10
            course = Courses.objects.get(course_id=course_id)

            course_ss = list(course.users.values('user_id'))
            course_ss_id = []
            for css in course_ss:
                course_ss_id.append(css['user_id'])
            print(course_ss_id)

            ss_profiles = UserProfile.objects.filter(permission__in=[1, 3]).exclude(user_id__in=course_ss_id)

            ss = list(ss_profiles.values('no'))
            for s in ss:
                s['username'] = UserProfile.objects.get(no=s['no']).user.username

            return HttpResponse(json.dumps(ss), content_type='application/json')


def relatess(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        # course_id = 10
        course = Courses.objects.get(course_id=course_id)

        userno = request.POST['userno']
        # userno = '123456'
        userprofile = UserProfile.objects.get(no=userno)
        user = User.objects.get(profile=userprofile)
        course_user = user.course_user

        course.users.add(course_user)
        course_user.course.add(course)

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    return JsonResponse({'msg': 'emmmm'})


def checkCourse(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        # course_id = 10
        course = Courses.objects.get(course_id=course_id)

        course.is_valid = True
        course.save()

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')