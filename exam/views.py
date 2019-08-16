from django.shortcuts import render
from .models import Certificate, Test, Question, Choice, Subject
from django.http import HttpResponseRedirect
from django.urls import reverse

def show_certificates(request):
    certificates = Certificate.objects.all()
    return render(request, 'exam/list.html', {'list':certificates})

def show_tests(request, id):
    tests = Test.objects.filter(certificate_id=id)
    return render(request, 'exam/list.html', {'list':tests})

def show_detail(request, id):
    subjects = []
    test = Test.objects.get(id=id)
    subject_models = Subject.objects.filter(certificate_id=test.certificate_id)
    scope = {
        1:[1,20],
        2:[21,40],
        3:[41,60],
        4:[61,80],
        5:[81,100],
    }
    for subject_model in subject_models:
        questions = Question.objects.filter(test_id=id, question_num__range=scope[subject_model.order])
        question_sets = make_questions_sets(questions)
        subject = TestSubject(subject_model.name, subject_model.order,question_sets)
        subjects.append(subject)

    return render(request, 'exam/detail.html', {'test':test, 'subjects':subjects})

def show_report(request, id):
    if request.method == 'POST':
        questions = Question.objects.filter(test_id=id)
        test = questions[0].test
        report = Report()
        for question in questions:
            choices = Choice.objects.filter(question_id=question.id)
            checked = request.POST.get(str(question.question_num))
            if checked:
                checked = int(checked)

            if question.answer == checked: #정답일경우
                report.point += 1
                report.o.append(Question_set(question, choices, checked))
            else:#오답일경우
                report.x.append(Question_set(question, choices, checked))

        return render(request, 'exam/report.html', {'report':report, 'test':test})

    else:
        return HttpResponseRedirect(reverse('exam:detail',args=[id]))

def test(request):
    return render(request, 'exam/test.html')

def make_questions_sets(questions):
    question_sets = []
    for question in questions:
        choice = Choice.objects.filter(question_id=question.id)
        question_set = Question_set(question, choice)
        question_sets.append(question_set)
    return question_sets

def get_questions_by_subject_order(questions, order):
    scope = {
        1:range(1,20),
        2:range(21,40),
        3:range(41,60),
        4:range(61,80),
        5:range(81,100),
    }
    pass_questions = []
    for question in questions:
        if question.question_num in scope[order]:
            pass_questions.append(question)
        if len(pass_questions)==20:
            break
    return pass_questions

class Question_set():
    def __init__(self, question, choices, checked=None):
        self.question = question
        self.choices = choices
        self.checked = checked

class Report():
    def __init__(self):
        self.point=0
        self.o=[]
        self.x=[]

    def result(self):
        if self.point >= 60:
            return "평균 {}점으로 합격하셨습니다.".format(self.point)
        else:
            return "평균 {}점으로 불합격하셨습니다.".format(self.point)

class TestSubject():
    def __init__(self, name, order, questions_sets):
        self.name = name
        self.order = order
        self.question_sets = questions_sets

