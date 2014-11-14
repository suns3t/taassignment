from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from taassignment.users import views as users
from taassignment.courses import views as courses
from . import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.home , name='home'),

    url(r'^users/list$', users.list_, name='users-list'),
    url(r'^users/create$', users.create, name='users-create'),
    url(r'^users/edit/(?P<userid>\d+)$' , users.edit, name='users-edit'),
    url(r'^users/delete/(?P<userid>\d+)$', users.delete, name='users-delete'),
    url(r'^users/clear_tas$', users.clear_tas, name='users-clear-tas'),
    url(r'^users/clear_faculty$', users.clear_faculty, name='users-clear-faculty'),
    url(r'^users/upload/', users.upload, name='users-upload' ),

    url(r'^courses/list$', courses.list_, name='courses-list'),
    url(r'^courses/upload/',courses.upload, name='courses-upload' ),
    url(r'^courses/create$', courses.create, name='courses-create'),
    url(r'^courses/edit/(?P<courseid>\d+)$' , courses.edit, name='courses-edit'),
    url(r'^courses/delete/(?P<courseid>\d+)$', courses.delete, name='courses-delete'),
    url(r'^courses/clear$', courses.clear, name='courses-clear'),
    url(r'^courses/change_tas/$', courses.change_tas, name='courses-change-tas'),
    url(r'^courses/download/$', courses.csv_courses_download, name='courses-download'),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.USE_CAS:
    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'djangocas.views.login', name='account-login'),
        url(r'^accounts/logout/$', 'djangocas.views.logout', name='account-logout'),
    )
    