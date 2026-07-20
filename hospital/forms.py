from django import forms
from .models import Doctor, Patient
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class DoctorForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    class Meta:
        model = Doctor
        fields = [
            "username",
            "doctor_name",
            "specialization",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username


class PatientForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    class Meta:
        model = Patient
        fields = [
            "username",
            "patient_name",
            "age",
            "disease",
            "doctor",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username
    
class GroupForm(forms.ModelForm):

    class Meta:
        model = Group

        fields = [
            "name"
        ]