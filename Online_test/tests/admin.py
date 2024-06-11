from django.contrib import admin
from .models import Test, Answer, Question,TestResult

admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(TestResult)