from django.contrib.auth.models import User
from django.db import models


class Answer(models.Model):
    answer_text = models.TextField('Ответ в текстовом виде')
    answer_img = models
    answer_test = models.BooleanField(default=False)


class Question(models.Model):
    question = models.CharField(max_length=25)
    image = models.ImageField(upload_to='question/')
    answer_connect = models.ForeignKey(Answer,on_delete=models.CASCADE)


class Test(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


