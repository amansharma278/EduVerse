import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages

from project_admin.models import User, Course, Section, SubSection, Invoice, UserCourse, Tag, CourseTag, Token
from project_admin.utils import generate_token


# Create your views here.
@csrf_exempt
def add_user(req):
    try:
        data = json.loads(req.body)
        name = data.get('name')
        email = data.get('email')
        contact_no = data.get('contact_no')
        password = data.get('password')
        account_type = data.get('account_type')
        gender = data.get('gender')
        dob = data.get('dob')
        about = data.get('about')
        if not all([name,email,contact_no,password,account_type,gender]):
            return JsonResponse({
            "message": "Check every input should be field",
            "success": "false"
            })
        user = User.objects.filter(email=email).first()
        if user:
            return JsonResponse({
            "message": 'This user is already exits',
            "success": "false"
        })
        print(data)
        User.objects.create(name = name,
                                        email = email,
                                        password= password,
                                        account_type=account_type,
                                        contact_no=contact_no,
                                        dob=dob,
                                        about=about,
                                        gender = gender

                                        )
        return JsonResponse({
        "message": "You have successfully registered",
        "success": "true" })
    except Exception as e:
        return JsonResponse({
            "message": str(e),
            "success": "false"

        },status=500)

    #
    # if name and email and password and contact_no and account_type:
    #     is_user_exist = User.objects.filter(email=email).first()
    #
    #     if account_type == 'admin':
    #         return JsonResponse({
    #             "messages" : "only authorized user can login to the admin pannel",
    #             "success": "false"
    #         })
    #
    #     # finding dublicates value
    #     if not is_user_exist:
    #         user = User(name = name, email = email, contact_no=contact_no,password=password,account_type=account_type,gender=gender,dob=dob,about=about)
    #         user.save()
    #
    #         return JsonResponse({
    #             "message": "You have successfully Registered",
    #             "success": "true"
    #         }, status=200)
    #     else:
    #         return JsonResponse({
    #             "message": "User is already exist",
    #             "success": "false"
    #         })
    #
    #
    # else:
    #     return JsonResponse({
    #         "message": "check every filed should be field",
    #         "success": "false"
    #     })

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
        return successful_response("Invoice is successfully generate")
    else:
        return failed_response("course id or user id are not found")



def successful_response(success_msg):
    return JsonResponse({
        "message": success_msg,
        "success":  "True"
    })
def failed_response(failed_msg):
    return JsonResponse({
        "message": failed_msg,
        "success":  "False"
    })

@csrf_exempt
def user_course(req):
    data = json.loads(req.body)
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    if not user_id or not course_id:
        return failed_response("User id and course id is required")

    course = Course.objects.filter(id = course_id).first()
    user = User.objects.filter(id = user_id).first()
    if not course:
        return failed_response("The course id is not not exists in database")
    if not user:
        return failed_response("This user id is not exist in the database")

    user_course_response= UserCourse.objects.create( user = user, course = course)

    return successful_response("course and user id are successfully created in database")

@csrf_exempt
def add_tag(req):
    data = json.loads(req.body)
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return failed_response("You need to Enter name or descriptions")
    else:
        add_tag_res = Tag.objects.create(name = name,description = description)

        return successful_response("You have create a tag successfully")

@csrf_exempt
def course_tag(req):
    data = json.loads(req.body)
    course_id = data.get('course_id')
    tag_id = data.get('tag_id')

    if not course_id or not tag_id:
        return JsonResponse({
            "message": "Please enter the course id and tag id",
            "success": "False"
        })
    else:
        course= Course.objects.filter(id = course_id).first()
        tag = Tag.objects.filter(id = tag_id).first()
        course_tag_res = CourseTag.objects.create(course = course, tag = tag)

        return successful_response("You have saved course id and Tag id")
@csrf_exempt
def get_all_user(req):

    users = User.objects.all()
    users_json =[]

    for user in users:

        user_json = {
            "id": user.id,
            "name":user.name,
            "email": user.email,
            "contact_no": user.contact_no,
            "password": user.password,
            "account_type": user.account_type,
            "is_active":user.is_active,
            "gender": user.gender,
            "dob": user.dob,
            "about": user.about
        }
        users_json.append(user_json)

    return JsonResponse({"users": users_json })


@csrf_exempt
def get_user_by_id(req):
    user_id = req.GET.get('user_id')
    print(user_id)
    if not user_id:
       return failed_response("User id is required")

    user = User.objects.filter(id=user_id).first()
    print(user)

    if not user:
        return failed_response("User does not exist in Database")

    user_obj={
            "id": user.id,
            "name":user.name,
            "email": user.email,
            "contact_no": user.contact_no,
            "account_type": user.account_type,
            "is_active":user.is_active,
            "gender": user.gender,
            "dob": user.dob,
            "about": user.about
        }
    return JsonResponse({
            "message": "user id is successfully found",
            "user": user_obj
        })


@csrf_exempt
def get_all_courses(req):
    courses = Course.objects.all()
    course_objs = []

    for course in courses:
        course_obj = {
            "id": course.id,
            "course_name": course.course_name,
            "course_description": course.course_description,
            "instructor": course.instructor,
            "what_you_will_learn": course.what_you_will_learn,
            "price":course.price,
            "thumbnail":course.thumbnail
        }
        course_objs.append(course_obj)
    return JsonResponse({"courses": course_objs})
@csrf_exempt
def get_course_by_id(req):
    course_id = req.GET.get('id')

    if not course_id:
      return failed_response("course id is required")

    course = Course.objects.filter(id = course_id).first()

    if not course:
      return failed_response("This course is not exist")

    course_objs = []

    course_obj = {
        "id": course.id,
        "course_name": course.course_name,
        "course_description": course.course_description,
        "instructor": course.instructor,
        "what_you_will_learn": course.what_you_will_learn,
        "price": course.price,
        "thumbnail": course.thumbnail
    }
    course_objs.append(course_obj)
    return JsonResponse({"courses":course_objs})
@csrf_exempt
def get_sections(req):

    sections = Section.objects.all()
    sec_objs =[]
    if not sections:
        return failed_response("There no sections")

    for section in sections:
        sec_obj = {
            "id": section.id,
            "section_name": section.sec_name,
            "course_id": section.course.id
        }
        sec_objs.append(sec_obj)
    return JsonResponse({"sections": sec_objs})
@csrf_exempt
def get_section_by_id(req):
    sec_id = req.GET.get('id')

    if not sec_id:
        return failed_response("Id failed is required")
    response = Section.objects.filter(id = sec_id).first()

    if not response:
        return failed_response("The id is not present in the db")

    return JsonResponse({
        "message": "Successfully fetched",
        "id": response.id
    })

@csrf_exempt
def get_sub_section(req):

    responses = SubSection.objects.all()

    if not responses:
        failed_response("No subsection are availaible in the database")
    sub_sec_jsons= []
    for resonse in responses:
        sub_json = {
            "id": resonse.id,
            "section_id": resonse.section.id,
            "title":resonse.title,
            "timeDuration": resonse.time_durastation,
            "descriptions": resonse.description,
            "videoUrl": resonse.video_url,

        }
        sub_sec_jsons.append(sub_json)

    return JsonResponse({
            "messages": "You have successfully fetched sub section data",
            "Subsections":sub_sec_jsons
        })

@csrf_exempt
def get_sub_section_by_id(req):
    sub_id = req.GET.get('id')

    if not sub_id:
        return failed_response("Id failed is required")
    response = SubSection.objects.filter(id = sub_id).first()

    if not response:
        return failed_response("No id present in the database")

    return JsonResponse({
        "message": "Id successfully fetched",
        "id": response.id
    })

@csrf_exempt
def get_all_invoices(req):

    responses = Invoice.objects.all()

    if not responses:
        return failed_response("No Invoices are in the database")

    invoice_objs = []

    for response in responses:
        invoice_obj = {
            "id": response.id,
            "user": response.user.id,
            "course": response.course.id,
            "price": response.price
        }
        invoice_objs.append(invoice_obj)

    return JsonResponse({
        "message:" :"successfully fetched all invoices",
        "responses": invoice_objs

    })
@csrf_exempt
def get_invoices_by_id(req):

    invoices_id = req.GET.get('id')
    if not invoices_id:
        return failed_response("Id failed is required")

    response = Invoice.objects.filter(id= invoices_id).first()

    if not response:
        return failed_response("This invoices id is not in the database")
    invoice_obj = {
        "id": response.id,
        "user": response.user.id,
        "course": response.course.id,
        "price": response.price
    }
    return JsonResponse({
        "message": "successfully fetched",
        "invoices": invoice_obj
    })
@csrf_exempt
def get_all_tag(req):
    responses = Tag.objects.all()

    if not responses:
        return failed_response("No Tag are present")
    tag_objs = []
    for response in responses:
        tag_obj = {
            "id": response.id,
            "name": response.name,
            "descriptions": response.description
        }
        tag_objs.append(tag_obj)

    return JsonResponse({
        "message": "successfully fetched the Tags",
        "Tags": tag_objs
    })
@csrf_exempt
def get_tag_by_id(req):
    tag_id = req.GET.get('id')

    if not tag_id:
        return failed_response("Id failed is required")
    response = Tag.objects.filter(id = tag_id).first()

    if not response:
        return failed_response("This tag is not in the Db")
    tag_obj = {
        "id": response.id,
        "name": response.name,
        "descriptions": response.description
    }

    return JsonResponse({
        "message": "successfully fetched the Tag",
        "Tag": tag_obj
    })
@csrf_exempt
def get_user_course_by_id(req):
    user_id = req.GET.get('id')
    responses = UserCourse.objects.filter(user = user_id).all()

    if not responses:
        return failed_response("This user id does not exist")
    user_courses_objs = []
    print(len(responses))
    for response in responses:
        user_course_obj = {
            "course_id": response.course.id,
            "course_name": response.course.course_name,
            "course_progress": response.course_progress,
            "course_instructor": response.course.instructor,
            "course_descriptions": response.course.course_description,
            'thumbnail': response.course.thumbnail
        }
        user_courses_objs.append(user_course_obj)

    if not user_courses_objs:
        return failed_response("This user does not have any courses")

    return JsonResponse({
        "message": "successfully fetched all user courses",
        "user_courses" : user_courses_objs
    })
@csrf_exempt
def login(req):
    data = json.loads(req.body)
    email = data.get('email')
    password = data.get('password')
    print(email)
    print(password)
    if not email or not password:
        return failed_response("Email and password are required")

    user = User.objects.filter(email = email).first()

    if not user:
        return failed_response("This user does not exist")

    user_password = user.password

    if password == user_password:
        token = generate_token(16)

        save_token = Token.objects.create(token = token,user=user,issue_at = datetime.now(),expired_at=datetime.now()+timedelta(hours=1))

        return JsonResponse({
            "message": "You have successfully logged in to your account",
            "token": save_token.token,
            "issue_at": save_token.issue_at,
            "expired_at": save_token.expired_at,
            "success": "true",

            "user":{
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "contact_no": user.contact_no,
                "account_type": user.account_type,
                "is_active": user.is_active,
                "gender": user.gender,
                "dob": user.dob,
                "about": user.about
            }

        })
    else:
        return failed_response("You have entered wrong passwords")









