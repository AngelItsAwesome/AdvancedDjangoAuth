from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from accounts.forms import CustomUserLogin, forgotPasswordForm, RecoveryPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import secrets

# Create your views here.
def index(request):

    #Using the created form
    form = CustomUserLogin()
    if request.method == 'POST':
        #Using the info gived by user
        email = request.POST['email']
        password = request.POST['password']
        #if email exists we get the saved user
        if(CustomUser.objects.filter(email=email)).exists():
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                #login the current User
                login(request, user)
                return redirect('authenticated')
            else:
                #Adding error messages
                messages.add_message(request, messages.INFO, 'Incorrect password')
        else:
            # Adding error messages
            messages.add_message(request, messages.INFO, 'User does not exist')
    return render(request,'accounts/login.html', {'form': form})

class RegisterView(CreateView):
    #Template
    template_name = 'accounts/register.html'
    #form
    form_class = CustomUserCreationForm
    #Redirecting the user if the form is valid
    success_url = reverse_lazy("message")

def forgotPasswd(request):
    form = forgotPasswordForm()
    if request.method == 'POST':
        email = request.POST["email"]
        if CustomUser.objects.filter(email=email).exists():
            #Send recover password method
            user = CustomUser.objects.get(email=email)
            token = secrets.token_hex(50)
            user.token = token
            user.save()
            #Sending email
            subject = 'PASSWORD RECOVERING'
            message = f"<html> <body>Here is your link! <a href='localhost:8000/recovery?token={token}'>Click Here DO NOT SHARE this link</a> </body> </html>"
            from_email = 'from@angel.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('message')
        else:
            messages.add_message(request, messages.INFO, 'User does not exist')


    return render(request, 'accounts/forgot.html', {'form' : form})

def message(request):
    return render(request, 'accounts/message.html')


def success(request):
    token = request.GET.get('token')

    valid = False
    if(CustomUser.objects.filter(token=token).exists() ):
        valid = True
        User = CustomUser.objects.get(token=token)
        User.verified = 1
        User.token = ''

        User.save()
    return render(request, 'accounts/success.html', {'token': valid})

def updatePassword(request):
    form = RecoveryPasswordForm()
    token = request.GET.get('token')
    valid = False
    if CustomUser.objects.filter(token=token).exists():
        valid = True

    if request.method == 'POST':
        password = request.POST.get('password')
        user = CustomUser.objects.get(token=token)
        user.set_password(password)
        user.token = ''
        user.save()
        return redirect('login')
    return render(request, 'accounts/recovery.html', {'form': form, 'valid': valid})


@login_required(login_url='/')
def au(request):
    return render(request, 'accounts/completed.html')

def log(request):
    logout(request)
    return redirect('login')