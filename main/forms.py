from django import forms
from .models import Product, UserProfile, Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'old_price', 'image', 'images', 'specifications', 'is_hit', 'is_sale']

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=False)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', max_length=20, required=True)
    birth_date = forms.DateField(label='Дата рождения', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(label='Пол', required=False, choices=[('', 'Не указан'), ('male', 'Мужской'), ('female', 'Женский'), ('other', 'Другой')])
    subscribe_news = forms.BooleanField(label='Я хочу получать информацию о новинках, акциях и специальных предложениях', required=False)
    agree_terms = forms.BooleanField(label='Я согласен с Условиями использования и Политикой конфиденциальности', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['TextInput', 'EmailInput', 'DateInput', 'PasswordInput', 'NumberInput']:
                field.widget.attrs['class'] = 'form-control'
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'password1', 'password2', 'subscribe_news', 'agree_terms')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует')
        return phone

    def clean_agree_terms(self):
        agree = self.cleaned_data.get('agree_terms')
        if not agree:
            raise forms.ValidationError('Вы должны согласиться с условиями использования и политикой конфиденциальности')
        return agree

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                birth_date=self.cleaned_data['birth_date'],
                gender=self.cleaned_data['gender'],
                subscribe_news=self.cleaned_data['subscribe_news'],
            )
        return user

class LoginForm(AuthenticationForm):
    captcha = forms.CharField(label='Введите капчу', max_length=6)

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['TextInput', 'EmailInput', 'NumberInput', 'Textarea']:
                field.widget.attrs['class'] = 'form-control'
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ == 'ClearableFileInput':
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'pros', 'cons', 'comment', 'photos']

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}))
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон', 'required': True}),
        } 