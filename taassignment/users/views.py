from django.shortcuts import render, get_object_or_404
from django.contrib.auth import decorators
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from taassignment.course.models import Course
from taassignment.users.models import User
from .forms import UserForm

# Create your views here.
@decorators.login_required
def staff_view_list(request):
    courses = Course.objects.all()
    users = User.objects.all()
    
    user_form = UserForm()

    return render(request, 'admin/staff_view_list.html', {
        'courses' : courses,
        'users' : users,
        'user_form' : user_form,
    })


@decorators.login_required
def staff_add_user(request):
    title = "Add New User"

    if request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('staff-home'))
    else:
        user_form = UserForm()

    return render(request, 'admin/staff_add_user.html', {
        'user_form' : user_form,
        'title' : title,
    })

@decorators.login_required
def staff_edit_user(request, userid):
    user = get_object_or_404(User, pk=userid)
    title = "Edit Existing User"

    if request.POST:
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('staff-home'))
    else:
        user_form = UserForm(instance=user)

    return render(request, 'admin/staff_add_user.html', {
        'user_form' : user_form,
        'title' : title
    })

@decorators.login_required
def staff_delete_user(request, userid):
    user = get_object_or_404(User, pk=userid)
    title = "Deleting User"

    if request.POST:
        user.delete()
        return HttpResponseRedirect(reverse("staff-home"))
