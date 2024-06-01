from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer_text = models.TextField('Ответ в текстовом виде')
    answer_img = models.ImageField(upload_to='answers/', blank=True, null=True)
    answer_test = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text or 'Ответ с изображением'

class Test(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name='tests')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        f" {self.user.username} - {self.test.title} - {self.score} "