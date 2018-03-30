from django.shortcuts import render, redirect
from questions.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404

def index(request):

    questions = Question.objects.new()
    questions = paginate(questions, request)
    id_ = 1
    context = {
        'questions': questions,
        'id_': id_,
    }

    return render(request, 'index.html', context)

def hot(request):

    questions = Question.objects.hot()
    questions = paginate(questions, request)
    _id = 2
    context = {
        'questions': questions,
        'id_': _id,
    }

    return render(request, 'hot.html', context)

def settings(request):

    return render(request, 'settings.html')

def login(request):

    return render(request, 'login.html')

def ask(request):

    return render(request, 'ask.html')

def registration(request):

    return render(request, 'registration.html')

def question(request, question_id):
    question = Question.objects.get(id=question_id)

    context = {
        'question': question
    }

    return render(request, 'answer-listing.html', context)

def question_like(request, question_id, id_):
    question = Question.objects.get(id=question_id)
    question.like()
    if int(id_) == 1:
        return redirect('index')
    elif int(id_) == 2:
        return redirect('hot')
    else:
        return redirect('tag')

def question_dislike(request, question_id, id_):
    question = Question.objects.get(id=question_id)
    question.dislike()
    if int(id_) == 1:
        return redirect('index')
    elif int(id_) == 2:
        return redirect('hot')
    else:
        return redirect('tag')


def answer_like(request, ans_id):
    answer = Answer.objects.get(id=ans_id)
    answer.like()

    return redirect('answer', answer.question.id)

def answer_dislike(request, ans_id):
    answer = Answer.objects.get(id=ans_id)
    answer.dislike()

    return redirect('answer', answer.question.id)

def answer_mark(request, ans_id):
    answer = Answer.objects.get(id=ans_id)
    answer.mark()

    return redirect('answer', answer.question.id)

def tag(request, tag_name):
    try:
        current_tag = Tag.objects.get(name=tag_name)
    except:

        raise Http404

    questions = Question.objects.filter(tag=current_tag)
    questions = paginate(questions, request)

    context = {
        'questions': questions,
        'tag': current_tag
    }

    return render(request, 'tag-search.html', context)


def paginate(objects_list, request):

    paginator = Paginator(objects_list, 3)

    try:
        questions = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(1)

    return questions



