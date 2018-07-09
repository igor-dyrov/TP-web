from django import forms
from questions.models import *

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets={
            'avatar': forms.FileInput
        }


class ProfileForm(forms.Form):
    login = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'askme-main-content-settings-offset'
    }))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'askme-main-content-settings-offset'
    }))
    def clean(self):
        try:
            User.objects.get(username=self.cleaned_data.get('login'))
            self.add_error('login', 'User with a such nick is already registered!')
        except:
            pass
        return self.cleaned_data

class AskForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'askme-main-content-ask-title askme-main-content-settings-offset form-control',
        'placeholder': 'Question`s title',
    }))
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'askme-main-content-ask-text askme-main-content-settings-offset form-control',
        'placeholder': 'Type here',
    }))
    tags = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'askme-main-content-ask-title askme-main-content-settings-offset form-control',
        'placeholder': 'Type your question`s tags splited by ,',
    }))
    pass

class RegForm(forms.Form):
    nick = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'askme-registration-login form-control',
        'style': 'margin-bottom: 20px',
        'placeholder': 'Enter your nick',
            }))
    email = forms.CharField(initial='example.me@mail.ru', widget=forms.TextInput(attrs={
        'class': 'askme-registration-login form-control',
        'style': 'margin-bottom: 20px',
            }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'askme-registration-login form-control',
        'style': 'margin-bottom: 20px',
    }))
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'askme-registration-login form-control',
        'style': 'margin-bottom: 20px',
    }))

    def clean(self):
        try:
            User.objects.get(username=self.cleaned_data.get('nick'))
            self.add_error('nick', 'User with a such nick is already registered!')
        except:
            pass
        if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
            self.add_error('password', 'Passwords must be equivalent!')
            raise forms.ValidationError('Passwords must be equivalent!')
        return self.cleaned_data

class LoginForm(forms.Form):
    login = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'askme-login-input',
        'placeholder': 'Nickname',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'askme-login-input',
        'placeholder': 'Password',
    }))

    def clean(self):
        return self.cleaned_data