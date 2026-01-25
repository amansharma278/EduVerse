from django.urls import path

from project_admin.views import (add_user,add_course,add_section,add_sub_section,
generate_invoice,user_course,add_tag,course_tag,get_all_user,get_all_courses)

urlpatterns=[
    path('adduser/', add_user),
    path('addcourse/',add_course),
    path('addsection/',add_section),
    path('addsubsection/',add_sub_section),
    path('generateInvoices/',generate_invoice),
    path('userCourse/',user_course),
    path('addtag/',add_tag),
    path('coursetag/',course_tag),
    path('get_all_user/',get_all_user),
    path('get_all_courses/',get_all_courses)


]