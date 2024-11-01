from django import forms
from .models import CustomUser


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150,label="First Name", required=True)
    last_name = forms.CharField(max_length=150, label="Last Name", required=True)
    usr_name = forms.CharField(max_length=150, label="User Name", required=True)
    usr_pass = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)
    usr_roll = forms.CharField(max_length=20, label="Roll Number", required=True)
    usr_dob = forms.DateField(label="Date of Birth", required=True, widget=forms.SelectDateWidget(years=range(1900, 2025)))
    usr_email = forms.EmailField(label="Email Address", required=True)






    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'usr_name', 'usr_pass', 'usr_roll', 'usr_dob', 'usr_email']



class LoginForm (forms.Form) :
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)