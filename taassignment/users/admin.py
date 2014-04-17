from django.contrib import admin
from taassignment.users.models import User 
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	
	# This changes UserAdmin list form
    list_display = ('username','is_staff','is_faculty','is_ta')

admin.site.register(User, UserAdmin)

