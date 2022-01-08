from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields

from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from ajax_select.fields import AutoCompleteField, AutoCompleteSelectField

from .models import Genre

User = get_user_model()

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data




class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Почта'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net', 'xyz']:
            raise forms.ValidationError(f'Регистрация для домена {domain} невозможна')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый адрес уже зарегистрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято. Попробуйте другое.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'phone', 'email']



class SearchForm(forms.Form):
    GENRE_CHOICES = (
        (g['slug'], g['name']) for g in Genre.objects.all().values('slug', 'name')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].label = 'Жанр'
        self.fields['artist'].help_text = ""
        self.fields['release_date_from'].label = 'Дата релиза (с)'
        self.fields['release_date_to'].label = 'Дата релиза (по)'

        self.helper = FormHelper()
        self.helper.form_class = 'form-check form-check-inline'
        self.helper.layout = Layout(InlineCheckboxes(['genre']))
    
    artist = AutoCompleteSelectField('artist', required=False, help_text='Начните набор текста, чтобы увидеть результат')
    genre = forms.MultipleChoiceField(choices=GENRE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    release_date_from = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False
    )
    release_date_to = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False
    )