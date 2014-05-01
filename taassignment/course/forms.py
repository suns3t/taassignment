from django import forms
from taassignment.course.models import Course 
from taassignment.users.models import User 

class CourseForm(forms.ModelForm):

    course_no = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Course No.', 'class' : 'form-control'}))
    course_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Course Name', 'class' : 'form-control'}))
    faculties = forms.MultipleChoiceField(label="Teacher", required=True)
    tas = forms.MultipleChoiceField(label="TA", required=False)


    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

        list_of_faculties = User.objects.filter(is_faculty=True).values('id','first_name', 'last_name')
        faculties_choices = tuple((str(faculty['id']), str(faculty['first_name']) + ' ' + str(faculty['last_name'])) for faculty in list_of_faculties)

        list_of_tas = User.objects.filter(is_ta=True).values('id','first_name', 'last_name')
        tas_choices = tuple((str(faculty['id']), str(faculty['first_name']) + ' ' + str(faculty['last_name'])) for faculty in list_of_tas)

        self.fields['faculties'] = forms.MultipleChoiceField(label="Teacher", required=True, choices=faculties_choices)
        self.fields['tas'] = forms.MultipleChoiceField(label="TA", required=False, choices=tas_choices)
        self.fields['faculties'].widget.attrs['class'] = 'form-control'
        self.fields['tas'].widget.attrs['class'] = 'form-control'

    def clean_faculties(self):
        faculties = self.cleaned_data.get('faculties')
        
        return User.objects.filter(id__in=faculties)

    def clean_tas(self):
        tas = self.cleaned_data.get('tas')

        return User.objects.filter(id__in=tas)

    class Meta:
        model = Course
        fields = (
            'course_no',
            'course_name',
            'faculties',
            'tas'
        )