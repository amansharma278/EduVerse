from django.urls import path

from project_admin.views import (add_user, add_course, add_section, add_sub_section, get_sections,
                                 generate_invoice, user_course, add_tag, course_tag, get_all_user, get_all_courses,
                                 get_user_by_id, get_course_by_id, get_section_by_id, get_sub_section,
                                 get_sub_section_by_id, get_all_invoices, get_invoices_by_id, get_all_tag,
                                 get_tag_by_id)

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
    path('get_all_courses/',get_all_courses),
    path('get_user_by_id/',get_user_by_id),
    path('get_course_by_id/',get_course_by_id),
    path('get_sections/',get_sections),
    path('get_section_by_id/',get_section_by_id),
    path('get_sub_section/',get_sub_section),
    path('get_sub_section_by_id/',get_sub_section_by_id),
    path('get_all_invoices/',get_all_invoices),
    path('get_invoices_by_id/',get_invoices_by_id),
    path('get_all_tag/',get_all_tag),
    path('get_tag_by_id/',get_tag_by_id),






]