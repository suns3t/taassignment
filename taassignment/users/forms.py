import ldap
import datetime

from django import forms
from django.conf import settings

from .models import User

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="Name",required=True,widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(label="Username",required=True,widget=forms.TextInput(attrs={'placeholder': 'Odin username'}))

    is_staff = forms.BooleanField(label="Admin", initial=False, required=False)
    is_faculty = forms.BooleanField(label='Faculty', initial=False, required=False)
    is_ta = forms.BooleanField(label='TA' ,initial=False, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'

        if self.instance.pk is not None:
            self.fields["username"].widget.attrs['readonly'] = 'readonly'


        # staff users can't remove themselves as staff members
        if user == self.instance:
            self.fields.pop("is_staff")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            # Check if this username is an valid Odin username
            ld = ldap.initialize(settings.LDAP_URL)
            ld.simple_bind_s()
            results = ld.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "uid=" + username)
            record = results[0][1]

        except IndexError:
            raise forms.ValidationError('This Odin username is invalid.')

        return username

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

