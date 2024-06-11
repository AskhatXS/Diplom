from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer
from .models import Test


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_test']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(AnswerForm, self).__init__(*args, **kwargs)
        if question:
            self.fields['answers'] = forms.ModelMultipleChoiceField(
                queryset=Answer.objects.filter(question=question),
                widget=forms.CheckboxSelectMultiple(),
                required=False
            )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'image']


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'author', 'is_published']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
