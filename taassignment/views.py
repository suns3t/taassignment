from taassignment.courses.models import Course
from django.shortcuts import render, get_object_or_404

# Public view of the page, also act as homepage
def home(request):
    courses = Course.objects.all()
    no_of_course = Course.objects.count()
    section = "home"

    return render(request, "home.html", {
        "courses" : courses,
        "has_courses" : no_of_course ,
        "section" : section,
    })
