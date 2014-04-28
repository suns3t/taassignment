from django.shortcuts import render
from django.contrib.auth import decorators
from taassignment.course.models import Course
from taassignment.users.models import User
from taassignment.course.forms import UploadFileForm
from django.db.models import Count, Min
#from django.contrib.auth.models import User
from django.conf import settings

# Course view of the pag
def teacher_view_list(request):
    current_user  = request.user
 #   courses       = Course.objects.all().filter(faculties__username=current_user.username).annotate(total=Count('tas')).order_by('course_name')
    courses       = Course.objects.all().annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)

    return render(request, "course/teacher_view_list.html", {
        "courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
        })

def request_csv_tas_upload(file):
    users = User()
#    users.objects.all().delete()
    for r in csv.reader(file):
        Oidn = r
        users.username = Oidn
        users.is_ta  = true
        users.is_active = true
        users.save()

def request_csv_courses_upload(file):
    courses = Course()
#    courses.objects.all().delete()
    for r in csv.reader(file):
        course_no, course_name, Oidn = r
        courses.course_no = course_no
        courses.course_name = course_name
        courses.facutlies.username = Oidn
        courses.faculties.is_faculty = true
        courses.facutlies.is_active = true
        courses.save()


    # Upload Courses
def upload_courses(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request_csv_courses_upload(request.FILES['file'])
    else:
        form = UploadFileForm()
        return render(request,'admin/upload_courses_import.html', {'form': form})

# Upload Tas
def upload_tas(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request_csv_tas_upload(request.FILES['file'])
    else:
        form = UploadFileForm()
        return render(request,'admin/upload_tas_import.html', {'form': form})



# Course view of the pag
def course_teacher_view_list(request):
    courses       = Course.objects.all().filter(faculties__username=request.GET['username']).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)

    return render(request, "course/course_tas_view_list.html", {
        "courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
        })


    # Course view of the pag
def course_tas_view_list(request):
    courses       = Course.objects.all().filter(course_no=request.GET['course']).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)

    return render(request, "course/course_tas_view_list.html", {
        "courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
        })


    # Public view of the page, also act as homepage
def public_view_list(request):
    current_user  = request.user
    courses       = Course.objects.all().annotate(total=Count('tas')).order_by('course_name')
 #   courses       = Course.objects.all().filter(faculties__username=current_user.username).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)

    return render(request, "course/public_view_list.html", {
        "courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
        })

    # Faculty home page
@decorators.permission_required('course.change_ta',raise_exception=True)
def faculty_view_list(request):
    courses = Course.objects.filter(faculties=request.user)
    no_of_courses = len(courses)

    return render(request, "course/public_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course,
        })
