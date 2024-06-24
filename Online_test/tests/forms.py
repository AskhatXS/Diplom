from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer
from .models import Test


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# forms.py

from django import forms
from .models import Test, Question, Answer

from django import forms
from .models import Test, Question, Answer

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'author', 'is_published']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'image', 'test']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'answer_img', 'answer_test', 'question', 'user', 'is_correct']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
