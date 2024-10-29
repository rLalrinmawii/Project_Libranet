from django import forms


class UserRegistrationForm(forms.Form):
    usr_name = forms.CharField(max_length=150, label="Name", required=True)
    usr_pass = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)
    usr_roll = forms.CharField(max_length=20, label="Roll Number", required=True)
    usr_dob = forms.DateField(label="Date of Birth", required=True, widget=forms.SelectDateWidget(years=range(1900, 2025)))
    usr_email = forms.EmailField(label="Email Address", required=True)


class LoginForm (forms.Form) :
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)