from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from taassignment.course import views as course
from taassignment.users import views as user

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', course.public_view_list , name='home'),
    url(r'^admin/list_courses$', user.staff_courses_view_list, name='staff-home-courses'),
    url(r'^admin/list_users$', user.staff_users_view_list, name='staff-home-users'),
    url(r'^admin/upload_tas/',course.upload_tas, name='upload-tas' ),
    url(r'^admin/upload_courses/',course.upload_courses, name='upload-courses' ),
    url(r'^admin/add_user$', user.staff_add_user, name='staff-add-user'),
    url(r'^admin/edit_user/(?P<userid>\w{0,5})$' , user.staff_edit_user, name='staff-edit-user'),
    url(r'^admin/delete_user/(?P<userid>\w{0,5})$', user.staff_delete_user, name='staff-delete-user'),
    url(r'^admin/add_course$', course.staff_add_course, name='staff-add-course'),
    url(r'^admin/edit_course/(?P<courseid>\w{0,5})$' , course.staff_edit_course, name='staff-edit-course'),
    url(r'^admin/delete_course/(?P<courseid>\w{0,5})$', course.staff_delete_course, name='staff-delete-course'),
    url(r'^admin/delete_all_courses$', course.staff_delete_all_courses, name='staff-delete-all-courses'),
    url(r'^admin/delete_all_tas$', user.staff_delete_all_tas, name='staff-delete-all-tas'),
    url(r'^admin/delete_all_faculties$', user.staff_delete_all_faculties, name='staff-delete-all-faculties'),
    url(r'^faculty/$', course.faculty_view_list, name='faculty-home'),
)

# djangocas
if settings.USE_CAS:
    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'djangocas.views.login', name='account-login'),
        url(r'^accounts/logout/$', 'djangocas.views.logout', name='account-logout'),
        )

    # urlpatterns = patterns('django.views.generic.simple', ('^admin/logout/$', 'redirect_to' ,
    #         {'url': '../../accounts/logout'})) + urlpatterns
# end djangocas

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
