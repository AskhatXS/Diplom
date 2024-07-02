from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer
from .models import Test


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'is_published']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'is_published': 'Опубликован',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание'}),
            'is_published': forms.CheckboxInput(),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question',]
        labels = {
            'question': 'Вопрос',
        }
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'Введите вопрос'})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']
        labels = {
            'question': 'Вопрос',
            'user': 'Пользователь',
            'is_correct': 'Правильный ли'
        }


#fekw
