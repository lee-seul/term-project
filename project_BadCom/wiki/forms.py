# coding: utf-8

from django import forms
from wiki.models import User

class SignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput, label='이메일')
    password1 = forms.CharField(widget=forms.PasswordInput, label='비밀번호')
    password2 = forms.CharField(widget=forms.PasswordInput, label='비밀번호(확인)')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('비밀번호가 다릅니다. 동일한 비밀번호를 입력해주세요.')

        return self.cleaned_data

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']



