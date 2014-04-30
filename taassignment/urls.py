from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from taassignment.course import views as course
from taassignment.users import views as user
admin.autodiscover()

urlpatterns = patterns('',
	
	url(r'^$', course.public_view_list , name='home'),
    url(r'^admin/$', user.staff_view_list, name='staff-home'),
    url(r'^teacher/',course.teacher_view_list, name='teachers' ),
    url(r'^upload_tas/',course.upload_tas, name='upload-tas' ),
    url(r'^upload_courses/',course.upload_courses, name='upload-courses' ),
    url(r'^admin/course/tas/',course.course_tas_view_list, name='course-tas' ),
    url(r'^admin/course/teachers/',course.course_teacher_view_list, name='course-teacher' ),
    url(r'^admin/add_user$', user.staff_add_user, name='staff-add-user'),
    url(r'^admin/edit_user/(?P<userid>\w{0,5})$' , user.staff_edit_user, name='staff-edit-user'),
    url(r'^admin/delete_user/(?P<userid>\w{0,5})$', user.staff_delete_user, name='staff-delete-user'),
    url(r'^faculty/', course.faculty_view_list, name='faculty-home'),
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
