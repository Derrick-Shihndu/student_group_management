from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name1','name2','name3','email','phone','courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple
        }

class AdminUnlockForm(forms.Form):
    master_password = forms.CharField(widget=forms.PasswordInput, label="Admin master password")
