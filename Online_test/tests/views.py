from django.contrib.auth import login, logout, authenticate
from .forms import TestForm, QuestionForm, LoginForm, RegistrationForm, ProfileForm

from .models import User, Profile
from .forms import AnswerForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Test, Question, Answer, TestResult
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, DetailView


def home(request):
    return render(request, 'head/home.html')


def not_authorized(request):
    return render(request, 'register/not_authorized.html')


def article1(request):
    return render(request, 'articles/article1.html')


def survey(request):
    return render(request, 'head/about_survey.html')

def about_us(request):
    return render(request, 'head/about_us.html')


def about_us2(request):
    return render(request, 'head/about_us2.html')

def article2(request):
    return render(request, 'articles/article2.html')


def article3(request):
    return render(request, 'articles/article3.html')
def base(request):
    return render(request, 'head/base.html')


def unauthenticated(request):
    return render(request, 'register/unauth.html')


def document(request):
    return render(request, 'head/document.html')


@login_required(login_url='not_authorized/')
def profile_view(request):
    profile = Profile.objects.first()
    return render(request, 'head/profile.html', {'profile': profile})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                return render(request, 'register/login.html', {
                    'form': form,
                    'error': 'Invalid username or password'
                })
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register/register.html', {'form': form})


@login_required(login_url='not_authorized/')
def logout_view(request):
    logout(request)
    return redirect('home')


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

@login_required
def test_list(request):

        user_tests = Test.objects.filter(author=request.user)
        other_tests = Test.objects.exclude(author=request.user)

        return render(request, 'head/test_list.html', {'user_tests': user_tests, 'other_tests': other_tests})


@login_required(login_url='not_authorized/')
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test_DETAIL/test_detail.html', {'test': test})


class TestCreateView(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'test_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add_questions', args=[self.object.id])

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.username
        return initial


@login_required(login_url='not_authorized/')
def add_questions(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            question.save()
            return redirect('add_questions', test_id=test_id)  # Обновляем страницу для добавления нового вопроса
    else:
        question_form = QuestionForm()
        questions = Question.objects.filter(test=test)  # Получаем уже добавленные вопросы
    return render(request, 'question_create.html', {'test': test, 'question_form': question_form, 'questions': questions})


@login_required(login_url='not_authorized/')
def add_answers(request, test_id, question_id):
    test = get_object_or_404(Test, pk=test_id)
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST, request.FILES)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.user = request.user  # Присваиваем текущего пользователя
            answer.save()
            return redirect('add_answers', test_id=test_id, question_id=question_id)  # Обновляем страницу с теми же параметрами
    else:
        answer_form = AnswerForm()
        answers = Answer.objects.filter(question=question)  # Получаем уже добавленные ответы

    return render(request, 'answer_create.html', {
        'test': test,
        'question': question,
        'answer_form': answer_form,
        'answers': answers
    })


@login_required(login_url='not_authorized/')
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        answer.delete()
    return redirect('add_answers', test_id=answer.question.test.id, question_id=answer.question.id)


@login_required(login_url='not_authorized/')
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        test_id = question.test.id
        question.delete()
        return redirect('add_questions', test_id=test_id)
    return redirect('')


@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.user != test.author and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this test.")
        return redirect('test_detail', test_id=test.id)

    if request.method == 'POST':
        test.delete()
        messages.success(request, "Test deleted successfully.")
        return redirect('test_list')

    return render(request, 'test_DETAIL/delete_test.html', {'test': test})



