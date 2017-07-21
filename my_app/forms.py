from django import forms
from django.contrib.auth.models import User
from passwords.validators import (
    DictionaryValidator, LengthValidator, ComplexityValidator)


class CreateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[
                                   DictionaryValidator(words=['banned_word'], threshold=0.9),
                                   LengthValidator(min_length=8),
                                   ComplexityValidator(complexities=dict(
                                       UPPER=1,
                                       LOWER=1,
                                       DIGITS=1,
                                       SPECIAL=1
                                   )),
                               ]
                               )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Retype password', 'label': 'Retype yor Password'}))

    def clean(self):
        all_data = super().clean()
        vmail = all_data.get('email')
        pass1 = all_data.get('password')
        pass2 = all_data.get('password2')
        is_exist = User.objects.filter(email=vmail)
        if len(is_exist) > 0:
            raise forms.ValidationError('Email is already used by someone else.')
        if pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError('Passwords did not match.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserLogin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    username = forms.CharField(widget=forms.TextInput(attrs={'label': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'label': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'password')
