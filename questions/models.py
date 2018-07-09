
#from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

# Create your models here.

class ModelManager(models.Manager):

    def new(self):
        return self.order_by('-created')

    def hot(self):
        return self.order_by('-rating')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()
    avatar = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    author = models.ForeignKey(Profile, blank=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ModelManager()
    answers_count = models.IntegerField()

    def num_of_ans(self):
        a = Question.objects.filter(id=self.id).annotate(num=Count('answers'))
        return a[0].num

    def like(self, user):
        try:
            Like.objects.get(user=user, q_id=self.id)
            return
        except:
            new_like = Like(user=user, q_id=self.id)
            new_like.save()
        self.rating += 1
        self.save()

    def dislike(self, user):
        try:
            Like.objects.get(user=user, q_id=self.id)
            return
        except:
            new_like = Like(user=user, q_id=self.id)
            new_like.save()
        self.rating -= 1
        self.save()

    def make_tags(self, request):
        tags = request.POST["tags"].split(", ")

        for _tag in tags:
            try:
                current_tag = Tag.objects.get(title=_tag)
            except:
                current_tag = Tag(title=_tag)
                current_tag.save()
            self.save()
            current_tag.question.add(self)

    def __str__(self):
        return self.title

def init_questions():
    questions = Question.objects.all()
    for q in questions:
        q.answers_count = q.num_of_ans()
        q.save()


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name="answers")
    text = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def mark(self):
        if self.correct is True:
            self.correct = False
        else:
            self.correct = True

        self.save()

    def __str__(self):
        return self.text

class Tag(models.Model):
    title = models.CharField(max_length=64)
    question = models.ManyToManyField(Question, related_name="tags", related_query_name="tag")
    objects = ModelManager()

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    q_id = models.IntegerField(default=0)

