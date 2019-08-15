from django.shortcuts import render
from .models import Certificate, Test, Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse

def show_certificates(request):
    certificates = Certificate.objects.all()
    return render(request, 'exam/list.html', {'list':certificates})

def show_tests(request, id):
    tests = Test.objects.filter(certificate_id=id)
    return render(request, 'exam/list.html', {'list':tests})

def show_detail(request, id):
    question_sets = []
    questions = Question.objects.filter(test_id=id)
    test = questions[0].test
    for question in questions:
        choices = Choice.objects.filter(question_id=question.id)
        question_sets.append(Question_set(question, choices))

    return render(request, 'exam/detail.html', {'question_sets':question_sets, 'test':test})

def show_report(request, id):
    if request.method == 'POST':
        questions = Question.objects.filter(test_id=id)
        test = questions[0].test
        report = Report()
        for question in questions:
            choices = Choice.objects.filter(question_id=question.id)
            try:
                if question.answer == int(request.POST[str(question.question_num)]):
                    report.point += 1
                    report.o.append(Question_set(question, choices))
                else:
                    report.x.append(Question_set(question, choices))
            except:
                report.x.append(Question_set(question, choices))
            report.checked.append(request.POST.get(str(question.question_num)))

        return render(request, 'exam/report.html', {'report':report, 'test':test})

    else:
        return HttpResponseRedirect(reverse('exam:detail',args=[id]))


class Question_set():
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices

class Report():
    def __init__(self):
        self.point=0
        self.o=[]
        self.x=[]
        self.checked=[]