from django.shortcuts import render, HttpResponse
from .models import *
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
    test.selected_subjects = subjects

    return render(request, 'exam/detail.html', {'test':test})


def show_report(request, id):
    if request.method == 'POST':
        test = Test.objects.get(id=id)
        #session content 만들기 .. 다음뷰에서 저장하면 세션딕셔너리를 그대로 저장.. report 모델에..
        test.selected_subjects = request.session['selected_subjects']
        test.marking(request.POST)

        request.session['answer'] = request.POST

        return render(request, 'exam/report.html', {'test': test})
    else:
        return HttpResponseRedirect(reverse('exam:detail',args=[id]))

def save_report(request, id):
    if request.method == 'POST' and request.session['answer']:
        report = Report(user_id=request.POST['user_id'])
        report.save()

        test = Test.objects.get(id=id)
        test.selected_subjects = request.session['selected_subjects']
        questions = test.get_selected_questions()

        for question in questions:
            ans = request.session['answer'].get(str(question.question_num))
            if ans:
                ans = int(ans)
            SubmitQuestion(report_id=report.id, question=question, answer=ans).save()

        request.session['answer'] = None
        return HttpResponse("저장되었습니다.")
    else:
        return HttpResponseRedirect(reverse("exam:certificate"))











