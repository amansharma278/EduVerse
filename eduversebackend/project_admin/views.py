import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages

from project_admin.models import User, Course, Section, SubSection, Invoice, UserCourse


# Create your views here.
@csrf_exempt
def add_user(req):
    data =json.loads(req.body)

    name = data['name']
    email = data['email']
    contact_no= data['contact_no']
    password = data['password']
    account_type = data['account_type']
    gender = data['gender']
    dob = data['dob']
    about = data['about']

    if name and email and password and contact_no and account_type:
        is_user_exist = User.objects.filter(email=email).first()

        if account_type == 'admin':
            return JsonResponse({
                "messages" : "You are not permited",
                "status": "failure"
            })

        # finding dublicates value
        if not is_user_exist:
            user = User(name = name, email = email, contact_no=contact_no,password=password,account_type=account_type,gender=gender,dob=dob,about=about)
            user.save()

            return JsonResponse({
                "message": "You have successfully Registered",
                "status" : "success"
            }, status=200)
        else:
            return JsonResponse({
                "message": "User is already exist",
                "status": "failure"
            })


    else:
        return JsonResponse({
            "message": "check every filed should be field"
            "status" "failure"
        })

@csrf_exempt
def add_course(req):
    data = json.loads(req.body)
    course_name= data['course_name']
    course_description = data['course_description']
    instructor = data['instructor']
    what_you_will_learn = data['what_you_will_learn']
    price= data['price']
    thumbnail = data['thumbnail']

    if course_name and course_description and instructor and what_you_will_learn and price and thumbnail:
        course = Course(course_name=course_name, course_description=course_description,instructor=instructor,what_you_will_learn=what_you_will_learn,price=price,thumbnail=thumbnail)
        course.save()
        return JsonResponse({
            "message": "course is created",
            "status": "success"
        })
    else:
        return JsonResponse({
            "message": "check every field",
            "status": "false"
        })

@csrf_exempt
def add_section(req):
    data = json.loads(req.body)
    section_name = data['section_name']
    course_id = data['course_id']

    if course_id:
        course =Course.objects.filter(id = course_id).first()

        section = Section(sec_name = section_name,course=course )
        section.save()
        return JsonResponse({
        "message": "successfully created section",
        "id": section.id,
        "section_name": section.sec_name,
        "course": {
            "id":course.id,
            "name":course.course_name,
            "desc":course.course_description
        }
    })

    else:
        return JsonResponse({
            "message": "can't find the course id ",
            "success": "False"
        })


@csrf_exempt
def add_sub_section(req):
    data = json.loads(req.body)
    title = data['title']
    time_durastation=data['time_durastation']
    description=data['description']
    video_url=data['video_url']
    s_id = data['s_id']

    print(s_id)
    if s_id:
        section = Section.objects.filter(id = s_id).first()
        sub_section_response= SubSection(title=title,time_durastation=time_durastation, description=description,video_url=video_url,section=section)
        sub_section_response.save()
        return JsonResponse({
        "message": "successfully created section",
        "success": "True"
    })
    else:
        return JsonResponse({
            "message": "can't find the section id ",
            "success": "False"
        })
@csrf_exempt
def generate_invoice(req):
    data = json.loads(req.body)

    user_id = data['user_id']
    course_id = data['course_id']
    course_progress = data['course_progress']
    # address = data['address']
    # pi_code = data['pincode']


    if user_id and course_id:
        user = User.objects.filter(id = user_id).first()
        course = Course.objects.filter(id = course_id).first()
        # username = user.name
        price = course.price
        print(user)
        # print(price)

        invoices_res = Invoice(user = user, course = course, price = price)
        invoices_res.save()
        return successful_response("Invoice is successfully generate", "True")
    else:
        return failed_response("course id or user id are not found","False")



def successful_response(success_msg, success_status):
    return JsonResponse({
        "message": success_msg,
        "success":  success_status
    })
def failed_response(failed_msg, success_status):
    return JsonResponse({
        "message": failed_msg,
        "success":  success_status
    })

@csrf_exempt
def user_course(req):
    data = json.loads(req.body)
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    if not user_id or not user_id:
        return failed_response("provide failed user id and course id","False")
    else:
        course = Course.objects.filter(id = course_id).first()
        user = User.objects.filter(id = user_id).first()

        user_course_response= UserCourse.objects.create(
            user = user,
            course = course
        )

        return successful_response("course and user id are successfully created in database","True")


