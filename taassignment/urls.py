from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from taassignment.users import views as user
from taassignment.users import views as users
from taassignment.courses import views as courses
from . import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.home , name='home'),

    url(r'^admin/list_users$', users.list_, name='staff-home-users'),
    url(r'^admin/add_user$', users.create, name='staff-add-user'),
    url(r'^admin/edit_user/(?P<userid>\d+)$' , users.edit, name='staff-edit-user'),
    url(r'^admin/delete_user/(?P<userid>\d+)$', users.delete, name='staff-delete-user'),
    url(r'^admin/delete_all_tas$', users.clear_tas, name='staff-delete-all-tas'),
    url(r'^admin/delete_all_faculties$', users.clear_faculty, name='staff-delete-all-faculties'),
    url(r'^admin/upload_tas/',users.upload, name='upload-tas' ),

    url(r'^admin/list_courses$', courses.list_, name='staff-home-courses'),
    url(r'^admin/upload_courses/',courses.upload, name='upload-courses' ),
    url(r'^admin/add_course$', courses.create, name='staff-add-course'),
    url(r'^admin/edit_course/(?P<courseid>\d+)$' , courses.edit, name='staff-edit-course'),
    url(r'^admin/delete_course/(?P<courseid>\d+)$', courses.delete, name='staff-delete-course'),
    url(r'^admin/delete_all_courses$', courses.clear, name='staff-delete-all-courses'),
    url(r'^faculty/$', courses.change_tas, name='faculty-home'),
)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'djangocas.views.login', name='account-login'),
    url(r'^accounts/logout/$', 'djangocas.views.logout', name='account-logout'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
