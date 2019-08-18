from django.shortcuts import render
from .models import Certificate, Test, Question, Choice, Subject
from django.http import HttpResponseRedirect
from django.urls import reverse

def show_certificates(request):
    certificates = Certificate.objects.all()
    return render(request, 'exam/certificates.html', {'select_box':certificates})

def show_tests(request, id):
    tests = Test.objects.filter(certificate_id=id)
    subjects = Subject.objects.filter(certificate_id=id)
    return render(request, 'exam/tests.html', {'select_box':tests, 'check_box':subjects})


def show_detail(request, id):
    subjects = [int(selected) for selected in request.GET]
    request.session['selected_subjects'] = subjects
    test = Test.objects.get(id=id)

    subjects = Subject.objects.filter(certificate_id=test.certificate_id, order__in=subjects).order_by('order')
    questions = [test.questions.filter(question_num__range=s.range()) for s in subjects]
    subjects_questions = zip(subjects,questions)

    return render(request, 'exam/detail.html', {'test':test, 'subjects':subjects, 'subjects_questions':subjects_questions})


def show_report(request, id):
    if request.method == 'POST':
        subjects = request.session['selected_subjects']
        answer = request.POST
        test = Test.objects.get(id=id)
        #session content 만들기 .. 다음뷰에서 저장하면 세션딕셔너리를 그대로 저장.. report 모델에..


        return render(request, 'exam/report.html', {'test': test})
    else:
        return HttpResponseRedirect(reverse('exam:detail',args=[id]))



def test_marking(test, answer):
    test.point = 0
    test.o = []
    test.x = []
    for subject in test.subjects():
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
        test.point += subject.point
        test.o += subject.o
        test.x += subject.x
    return test








