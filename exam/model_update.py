import csv
import os
from django.core.files.images import ImageFile


def get_csv(path, columns):
    reader = csv.DictReader(open(path, 'rt'))

    dict_list = []

    for line in reader:
        if is_available(line):
            dict_list.append(choice_columns(line, columns))
    return dict_list

def is_available(dic):
    for key,val in dic.items():
        if val is '':
            return False
        break
    return True

def choice_columns(dic, columns):
    ans = {}
    for key,val in dic.items():
        if key in columns:
            ans[key] = val
    return ans

def update_model_from_dict(dics, model):
    for dic in dics:
        if int(dic['question_id'])<= 638:
            continue
        if dic.get('img') in [None, '']:
            try:
                del dic['img']
            except:
                pass
            instance = model(**dic)
        else:
            img = dic['img']
            del dic['img']
            instance = model(**dic)
            name = get_name(img)
            file = ImageFile(open(img, 'rb'))
            instance.img.save(name, file, save=True)
        instance.save()
        print('{} 완료..'.format(dic))
#from exam.model_update import update_model

def get_name(path):
    first = 36
    last = path.find('/bindata/')
    name1 = path[first:last]
    first = path.find('/BIN') + 4
    last = first + 4
    name2 = path[first:last]
    return name1 + '_' + name2 + '.jpg'

def update_model():
    from exam.models import Certificate, Test, Question, Choice
    test_keys = [
        'certificate_id',
        'year',
        'num',
    ]
    question_keys = [
        'test_id',
        'question_num',
        'contents',
        'answer',
        'img',
    ]
    choice_keys = [
        'question_id',
        'choice_num',
        'contents',
        'img',
    ]
    #TEST = get_csv('F:/2019/project/mock_test/TEST.csv', test_keys)
    #QUESTION = get_csv('F:/2019/project/mock_test/QUESTION.csv', question_keys)
    CHOICE = get_csv('F:/2019/project/mock_test/CHOICE.csv', choice_keys)
    #update_model_from_dict(TEST, Test)
    #update_model_from_dict(QUESTION, Question)
    update_model_from_dict(CHOICE, Choice)


def config():
    from exam.models import Test
    tests = Test.objects.all()
    y = 2001
    n = 1
    ban_list = [(2006,1),
                (2008,1),
                (2009,2),
                (2012,3),
                (2015,3),
                (2016,1),
                (2017,3),
                (2019,2),
                (2019,3),
                (2013,3)]
    for test in tests:
        while (y,n) in ban_list:
            n += 1
            if n == 4:
                y += 1
                n = 1
        test.year=y
        test.num=n
        test.save()
        n+=1
        if n==4:
            y+=1
            n=1



