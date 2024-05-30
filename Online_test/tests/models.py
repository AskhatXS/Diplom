from django.contrib.auth.models import User
from django.db import models


class Answer(models.Model):
    answer_text = models.TextField('Ответ в текстовом виде')
    answer_img = models.ImageField(upload_to='answers/', blank=True, null=True)
    answer_test = models.BooleanField(default=False)


class Question(models.Model):
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    answer_connect = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Test(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    is_published = models.BooleanField(default=False)

    def str(self):
        return self.title


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        f" {self.user.username} - {self.test.title} - {self.score} "