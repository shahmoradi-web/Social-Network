
from django.core.exceptions import ValidationError

from social.models import User
from django import forms
from .models import *

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label=' Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'phone')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError('پسورد ها مطابقت ندارد')
        return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('phone already exists')
        return phone


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',
                  'phone','bio','data_of_brith','job', 'photo']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('phone already exists')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('username already exists')
        return username


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد','پیشنهاد'),
        ('انتقاد','انتقاد'),
        ('گزارش','گزارش')
    )
    message = forms.CharField(required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
