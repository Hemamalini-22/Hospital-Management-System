from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Patient
from .forms import DoctorForm, PatientForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupForm


def home(request):
    return redirect('doctor_list')

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request,'doctor_list.html',{'doctors': doctors})

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def doctor_add(request):

    if request.method == "POST":

        form = DoctorForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            # Password is same as username
            password = username

            user = User.objects.create_user(
                username=username,
                password=password
            )

            doctor = form.save(commit=False)
            doctor.user = user

            last_doctor = Doctor.objects.order_by("-id").first()

            if last_doctor:
                number = int(last_doctor.doctor_id.replace("DOC", "")) + 1
            else:
                number = 1

            doctor.doctor_id = f"DOC{number:03d}"

            doctor.save()

            messages.success(
                request,
                f"""
Doctor added successfully.

Username : {username}
Password : {password}
                """
            )

            return redirect("doctor_list")

    else:

        form = DoctorForm()

    return render(
        request,
        "doctor_form.html",
        {
            "form": form
        }
    )

def doctor_edit(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    form = DoctorForm(request.POST,instance=doctor)

    if form.is_valid():
        doctor.save()
        messages.success( request, "Doctor updated successfully.")
        return redirect("doctor_list")
    return render(request,'doctor_form.html',{'form': form})

def doctor_delete(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.user.delete()
    messages.success(request,"Doctor deleted successfully.")
    return redirect("doctor_list")


def patient_list(request):
    patients = Patient.objects.all()
    return render(request,'patient_list.html',{'patients': patients})

def patient_add(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            # Password = Username
            user = User.objects.create_user(
                username=username,
                password=username
            )

            patient = form.save(commit=False)
            patient.user = user

            last_patient = Patient.objects.order_by("-id").first()

            if last_patient:
                number = int(last_patient.patient_id.replace("PAT", "")) + 1
            else:
                number = 1

            patient.patient_id = f"PAT{number:03d}"

            patient.save()

            messages.success(
                request,
                f"Patient Added Successfully.\n"
                f"Username : {username}\n"
                f"Password : {username}"
            )

            return redirect("patient_list")

    else:

        form = PatientForm()

    return render(
        request,
        "patient_form.html",
        {
            "form": form
        }
    )

def patient_edit(request, id):
    patient = get_object_or_404(Patient,id=id)
    form = PatientForm(request.POST,instance=patient)

    if form.is_valid():
        patient.save()
        messages.success(request,"Patient updated successfully.")
        return redirect("patient_list")
    return render(request,'patient_form.html',{'form': form})

def patient_delete(request, id):
    patient = get_object_or_404(Patient, id=id)
    user = patient.user
    patient.delete()
    user.delete()
    messages.success(request, "Patient deleted successfully.")
    return redirect("patient_list")

from .forms import LoginForm
def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            # Doctor
            if Doctor.objects.filter(user=user).exists():
                return redirect("doctor_dashboard")
            # Patient
            elif Patient.objects.filter(user=user).exists():
                return redirect("patient_dashboard")
            # dean
            elif user.is_superuser:
                return redirect("dashboard")
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, "login.html",{"form": form})

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect("login")
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    return render(request,"dashboard.html",
        {
            "doctor_count":doctor_count,
            "patient_count":patient_count,
            
        }
    )
    
@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor,user=request.user)
    patients = Patient.objects.filter( doctor=doctor)
    context = {
        "doctor": doctor,
        "patients": patients,
        
    }
    return render(request,"doctor_dashboard.html",context)

@login_required
def patient_dashboard(request):
    patient = Patient.objects.get( user=request.user)
    context = {  
        "patient": patient,
        
    }
    return render( request, "patient_dashboard.html", context)

@login_required
def group_list(request):

    groups = Group.objects.all()

    return render(
        request,
        "group_list.html",
        {
            "groups": groups
        }
    )

@login_required
def group_add(request):

    if not request.user.is_superuser:
        return redirect("login")

    if request.method == "POST":

        form = GroupForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Group Added Successfully."
            )

            return redirect("group_list")

    else:

        form = GroupForm()

    return render(
        request,
        "group_form.html",
        {
            "form": form
        }
    )

@login_required
def group_edit(request, id):

    if not request.user.is_superuser:
        return redirect("login")

    group = get_object_or_404(Group, id=id)

    if request.method == "POST":

        form = GroupForm(
            request.POST,
            instance=group
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Group Updated Successfully."
            )

            return redirect("group_list")

    else:

        form = GroupForm(instance=group)

    return render(
        request,
        "group_form.html",
        {
            "form": form
        }
    )

@login_required
def group_delete(request, id):

    if not request.user.is_superuser:
        return redirect("login")

    group = get_object_or_404(Group, id=id)

    group.delete()

    messages.success(
        request,
        "Group Deleted Successfully."
    )

    return redirect("group_list")

def logout_view(request):
    logout(request)
    return redirect("login")

