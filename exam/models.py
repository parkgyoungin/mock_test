from django.db import models
from django.urls import reverse
'''
odict_keys(['CERTIFICATE_ID', 'NAME'])
odict_keys(['CERTIFICATE_ID', 'TEST_ID', 'YEAR', 'NUM'])
odict_keys(['TEST_ID', 'QUESTION_ID', 'QUESTION_NUM', 'CONTENTS', 'ANSWER', 'IMG'])
odict_keys(['QUESTION_ID', 'CHOICE_ID', 'CHOICE_NUM', 'CHOICE_CONTENTS', 'IMG'])
'''
class Certificate(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exam:tests', args=[self.id])

class Test(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='tests')
    year = models.PositiveIntegerField()
    num = models.PositiveIntegerField()

    def __str__(self):
        return "{}년 {}회차".format(self.year, self.num)

    def get_absolute_url(self):
        return reverse('exam:detail', args=[self.id])

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_num = models.PositiveIntegerField()
    contents = models.CharField(max_length=200)
    answer = models.PositiveIntegerField()
    img = models.ImageField(upload_to='questions/%Y/%m/%d', blank=True)

    def __str__(self):
        return str(self.test_id) + " {}번문제".format(self.question_num)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_num = models.PositiveIntegerField()
    contents = models.CharField(max_length=200)
    img = models.ImageField(upload_to='choices/%Y/%m/%d', blank=True)

    def __str__(self):
        return str(self.question_id) + " 보기{}".format(self.choice_num)