from django.contrib.auth import login, logout, authenticate
from django.views import View

from .forms import RegistrationForm, LoginForm, AnswerForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Test
from .forms import TestForm


def home(request):
    return render(request, 'head/home.html')


def dash(request):
    return render(request, 'head/dash.html')


def unauthenticated(request):
    return render(request, 'register/unauth.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash')
            else:

                return render(request, 'register/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()

    return render(request, 'register/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
        return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# @login_required
# def create_test(request):
#     if request.method == 'POST':
#         form = TestForm(request.POST)
#         if form.is_valid():
#             test = form.save(commit=False)
#             test.author = request.user
#             test.save()
#             return redirect('test_list')
#     else:
#         form = TestForm()
#     return render(request, 'create_test.html', {'form': form})


@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('test_detail', test_id=test.id)
    else:
        form = TestForm(instance=test)

    return render(request, 'test_DETAIL/edit_test.html', {'form': form, 'test': test})


@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.delete()
    return redirect('test_list')


@login_required
def publish_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.user != test.author:
        return HttpResponse('You are not allowed to publish this test.')
    test.is_published = True
    test.save()
    return redirect('test_detail', test_id=test.id)


def take_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    if request.method == 'POST':
        form = AnswerForm(test.questions.all(), request.POST, request.FILES)
        if form.is_valid():

            return redirect('test_result')
    else:
        form =  (test.questions.all())
    context = {
        'test': test,
        'form': form,
    }
    return render(request, 'take_test.html', context)

@login_required
def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    results = test.get_results()  #
    return render(request, 'test_results.html', {'test': test, 'results': results})


# @login required
def test_list(request):

        user_tests = Test.objects.filter(author=request.user)
        other_tests = Test.objects.all()

        return render(request, 'test_list.html', {'user_tests': user_tests, 'other_tests': other_tests})

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test_DETAIL/test_detail.html', {'test': test})

from django.shortcuts import render, redirect
from .forms import *
from django.shortcuts import render, redirect
from .forms import TestForm, QuestionForm, AnswerForm
from .models import Test, Question, Answer
from django.forms import modelformset_factory

def create_test(request):
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=1, can_delete=True)
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1, can_delete=True)

    if request.method == 'POST':
        test_form = TestForm(request.POST)
        question_formset = QuestionFormSet(request.POST, request.FILES, prefix='questions')
        answer_formset = AnswerFormSet(request.POST, request.FILES, prefix='answers')

        if test_form.is_valid() and question_formset.is_valid() and answer_formset.is_valid():
            test = test_form.save()
            questions = question_formset.save(commit=False)

            for question in questions:
                question.save()
                test.questions.add(question)
                answers = [answer for answer in answer_formset.save(commit=False) if answer.question_id == question.id]
                for answer in answers:
                    answer.question = question
                    answer.save()

            return redirect('test_list')

    else:
        test_form = TestForm()
        question_formset = QuestionFormSet(prefix='questions')
        answer_formset = AnswerFormSet(prefix='answers')

    return render(request, 'create_test.html', {
        'test_form': test_form,
        'question_formset': question_formset,
        'answer_formset': answer_formset,
    })



