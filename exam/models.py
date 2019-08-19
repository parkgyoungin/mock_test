from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
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

class Subject(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='subjects')
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.certificate.name + '_' + str(self.order) + '_' + self.name

    def range(self):
        return [20*(self.order-1)+1, 20*self.order]


class Test(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='tests')
    year = models.PositiveIntegerField()
    num = models.PositiveIntegerField()

    def __str__(self):
        return "{}년 {}회차".format(self.year, self.num)

    def get_absolute_url(self):
        return reverse('exam:detail', args=[self.id])

    def subjects(self):
        subjects = Subject.objects.filter(certificate_id=self.certificate_id, order__in=self.selected_subjects)
        new_subjects = []
        for subject in subjects:
            subject.questions = Question.objects.filter(test_id=self.id, question_num__range=subject.range())
            new_subjects.append(subject)
        return new_subjects

    def marking(self, answer):
        self.point = 0
        self.o = []
        self.x = []
        for subject in self.subjects():
            subject.point = 0
            subject.o = []
            subject.x = []
            for question in subject.questions:
                user_ans = answer.get(str(question.question_num))
                if user_ans:
                    question.checked = int(user_ans)
                if question.answer == None or str(question.answer) != user_ans:
                    subject.x.append(question)
                else:
                    subject.o.append(question)
                    subject.point += 1
            self.point += subject.point
            self.o += subject.o
            self.x += subject.x

    def get_selected_questions(self):
        questions = []
        for subject in self.subjects():
            questions += subject.questions
        return questions


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_num = models.PositiveIntegerField()
    contents = models.CharField(max_length=200)
    answer = models.PositiveIntegerField()
    img = models.ImageField(upload_to='questions/%Y/%m/%d', blank=True)

    def __str__(self):
        return str(self.test_id) + " {}번문제".format(self.question_num)

    def get_answer(self):
        special_characters=['①','②','③','④']
        return special_characters[self.answer-1]




class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_num = models.PositiveIntegerField()
    contents = models.CharField(max_length=200)
    img = models.ImageField(upload_to='choices/%Y/%m/%d', blank=True)

    def __str__(self):
        return str(self.question_id) + " 보기{}".format(self.choice_num)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created = models.DateTimeField(auto_now_add=True)

class SubmitQuestion(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submitted')
    answer = models.PositiveIntegerField(null=True)


