from django import forms
from taassignment.users.models import User 
import datetime

class UserForm(forms.ModelForm):

    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Odin username'}))
    
    is_staff = forms.BooleanField(label="Staff", initial=False, required=False)
    is_faculty = forms.BooleanField(label='Faculty', initial=False, required=False)
    is_ta = forms.BooleanField(label='TA' ,initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        
        user.email = user.username + '@pdx.edu'
        user.last_login = datetime.datetime.now()
        user.set_password('')

        if commit:
            user.save()
        return user 

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'is_faculty',
            'is_ta',
            'is_staff'
        )

