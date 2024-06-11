from django.contrib.auth import login, logout, authenticate
from .forms import *
from .forms import TestForm, QuestionForm
from django.forms import modelformset_factory
from .models import User
from .forms import AnswerForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Test, Question, Answer, TestResult
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
                return redirect('test_list')
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
def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.all()

    if request.method == 'POST':
        user = request.user
        score = 0
        total_questions = questions.count()

        for question in questions:
            user_answer_id = request.POST.get(f'question_{question.id}')

            if user_answer_id:
                try:
                    user_answer = Answer.objects.get(id=user_answer_id, question=question)
                    correct_answer = Answer.objects.filter(question=question, is_correct=True).first()

                    if user_answer == correct_answer:
                        score += 1
                except Answer.DoesNotExist:
                    continue

        score_percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        TestResult.objects.update_or_create(
            user=user,
            test=test,
            defaults={'score': score_percentage}
        )

        messages.success(request, f'Вы завершили тест "{test.title}" с результатом {score_percentage:.2f}%')
        return redirect(reverse('test_results', kwargs={'user_id': user.id, 'test_id': test.id}))

    return render(request, 'take_test.html', {'test': test, 'questions': questions})


@login_required
def test_results(request, user_id, test_id):
    user = get_object_or_404(User, pk=user_id)
    test = get_object_or_404(Test, pk=test_id)
    result = get_object_or_404(TestResult, user=user, test=test)
    return render(request, 'test_results.html', {'result': result, 'user': user, 'test': test})


def retake_test(request, test_id):
    Answer.objects.filter(question__in=Test.objects.get(id=test_id).questions.all(), user=request.user).delete()
    return redirect('take_test', test_id=test_id)

@login_required
def test_list(request):

        user_tests = Test.objects.filter(author=request.user)
        other_tests = Test.objects.exclude(author=request.user)

        return render(request, 'test_DETAIL/test_list.html', {'user_tests': user_tests, 'other_tests': other_tests})

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test_DETAIL/test_detail.html', {'test': test})


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



