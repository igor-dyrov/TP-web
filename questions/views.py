from django.shortcuts import render, redirect, get_object_or_404
from questions.models import *
from questions.forms import *
from django.contrib import auth
from questions.forms import AskForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404

import logging
logging.basicConfig()
logger = logging.getLogger("__name__")

def index(request):
    questions = Question.objects.new()
    questions = paginate(questions, request)
    id_ = 1
    context = {
        'questions': questions,
        'id_': id_,
        'tags': Tag.objects.all()[:7],
        'users': User.objects.all()[:5],
    }
    return render(request, 'index.html', context)

def hot(request):

    questions = Question.objects.hot()
    questions = paginate(questions, request)
    _id = 2
    context = {
        'questions': questions,
        'id_': _id,
        'tags': Tag.objects.all()[:7],
        'users': User.objects.all()[:5],
    }

    return render(request, 'hot.html', context)

def search(request):
    return tag(request, request.POST["tag"])
def settings(request):
    try:
        form = ProfileForm()
        context = {
            'tags': Tag.objects.all()[:7],
            'users': User.objects.all()[:5],
            'form': form,
            'user': request.user,
            'image': ProfileImageForm(instance=request.user.profile),
        }
        return render(request, 'settings.html', context)
    except:
        raise Http404

@login_required()
def change_profile(request):
    form = ProfileForm(request.POST, request.FILES)
    image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid() and image_form.is_valid():
        if request.POST.get('login') is not '':
            user = request.user
            user.username = request.POST.get('login')
            user.save()
        if request.POST.get('email') is not '':
            user = request.user
            user.email = request.POST.get('email')
            user.save()
        if request.FILES:
            image_form.save()
        return redirect('index')
    else:
        return render(request, 'settings.html', {
            'tags': Tag.objects.all()[:7],
            'users': User.objects.all()[:5],
            'form': form,
            'user': request.user,
            'image': image_form,
        })

def login(request):
    context = {
        'tags': Tag.objects.all()[:7],
        'users': User.objects.all()[:5],
        'form': LoginForm,
    }
    return render(request, 'login.html', context)

def auth_user(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=request.POST.get('login'),
                password=request.POST.get('password'),
            )
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                form.add_error('login', 'Wrong login or password')
                context = {
                    'form': form,
                    'tags': Tag.objects.all()[:7],
                    'users': User.objects.all()[:5],
                }
                return render(request, 'login.html', context)
    return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')

def ask(request):
    form = AskForm()
    context = {
        'form': form,
        'tags': Tag.objects.all()[:7],
        'users': User.objects.all()[:5],
    }
    return render(request, 'ask.html', context)

def registration(request):
    context = {
        'tags': Tag.objects.all()[:7],
        'users': User.objects.all()[:5],
        'form': RegForm(),
    }
    return render(request, 'registration.html', context)

def make_new_user(request):
    if request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['nick'], request.POST['email'],
                                            request.POST['password'])
            user.save()
            prof = Profile(user=user, rating=0)
            prof.save()
            auth.authenticate(
                username=request.POST.get('nick'),
                password=request.POST.get('password'),
            )
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration.html', {
                'tags': Tag.objects.all()[:7],
                'users': User.objects.all()[:5],
                'form': form,
            })

def question(request, question_id):
        question = get_object_or_404(Question, id=question_id)
        context = {
            'question': question,
            'tags': Tag.objects.all()[:7],
            'users': User.objects.all()[:5],
        }

        return render(request, 'answer-listing.html', context)

def question_like(request, question_id, id_):
    question = get_object_or_404(Question, id=question_id)
    try:
        question.like(request.user)
    except:
        return redirect('login')
    if int(id_) == 1:
        return redirect('index')
    elif int(id_) == 2:
        return redirect('hot')
    else:
        return redirect('hot')

def question_save(request) :
    try:
        new_q = Question(author=request.user.profile,
                         title=request.POST["title"],
                         text=request.POST["text"],
                         rating=0,
                         answers_count=0)
        new_q.make_tags(request)
        return redirect('answer', new_q.id)
    except:
        return redirect('login')

def question_dislike(request, question_id, id_):
    question = get_object_or_404(Question, id=question_id)
    try:
        question.dislike(request.user)
    except:
        return redirect('login')
    if int(id_) == 1:
        return redirect('index')
    elif int(id_) == 2:
        return redirect('hot')
    else:
        return redirect('hot')


def answer_like(request, ans_id):
    answer = get_object_or_404(Answer, id=ans_id)
    answer.like()

    return redirect('answer', answer.question.id)

def answer_dislike(request, ans_id):
    answer = get_object_or_404(Answer, id=ans_id)
    answer.dislike()

    return redirect('answer', answer.question.id)

def answer_mark(request, ans_id):
    answer = get_object_or_404(Answer, id=ans_id)
    answer.mark()

    return redirect('answer', answer.question.id)

def answer(request, q_id):
    try:
        ans = Answer(author=request.user.profile,
                     question=Question.objects.get(id=q_id),
                     rating=0,
                     text=request.POST["text"])
        ans.save()
        ans.question.answers.add(ans)
        ans.question.answers_count = ans.question.num_of_ans()
        ans.question.save()
        return redirect('answer', q_id)
    except:
        return redirect('login')

def tag(request, tag_name):
    current_tag = get_object_or_404(Tag, title=tag_name)
    questions = Question.objects.new().filter(tag=current_tag)
    questions = paginate(questions, request)

    context = {
        'questions': questions,
        'tag': current_tag,
        "id_": 3,
        'tags': Tag.objects.all()[:7],
        'users': User.objects.all()[:5],
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



