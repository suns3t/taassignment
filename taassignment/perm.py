from taassignment.users.models import User 

def faculty_member_check(user):
    try:
        if user.is_faculty:
            return True
        return False
    except:
        return False

def admin_member_check(user):
    try:
        if user.is_staff:
            return True
        return False
    except:
        return False

def ta_member_check(user):
    try:
        if user.is_ta:
            return True
        return False
    except:
        return False