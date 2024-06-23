from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import CustomUser
from django.contrib.auth import forms
from django import forms
import secrets


class CustomUserCreationForm(UserCreationForm):

    #Meta class for the relationship of model and fields for form
    class Meta:
        model = CustomUser
        fields = ('username','email','celphone','password1', 'password2')

    #Email Custom Validation
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')

        return email
    #Celphone Custom Validation
    def clean_celphone(self):
        celphone = self.cleaned_data['celphone']
        if CustomUser.objects.filter(celphone=celphone).exists():
            raise forms.ValidationError('A user with that celphone already exist')
        return celphone

    """
        Here i overrided the save method for send a email when the user form valid Function is called
    """
    def save(self, commit=True):
        user = super().save(commit=False) #Taking the current user info without saving into database
        email = self.cleaned_data['email']
        token = secrets.token_hex(50)
        user.token = token
        if commit:
            user.save()

            #Sending Email
            from django.core.mail import send_mail

            subject = 'Thanks for registering on my SPECIAL SITE HEHE'
            message = f"<html> <body>Here is your link! <a href='localhost:8000/token?token={token}'>Click Here</a> </body> </html>"
            from_email = 'from@angel.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return user

    #PlaceHolder for each of fields
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label


#Custom Login Form
class CustomUserLogin(forms.Form):

    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class forgotPasswordForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

class RecoveryPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new Password'}))

