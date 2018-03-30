
#from __future__ import unicode_literals

from django.db import models

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

    def __str__(self):
        return self.user.username

class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.IntegerField()
    num_of_ans = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    objects = ModelManager()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def make_tags(self, request):
        tags = request.POST["question_tags"].split(", ")

        for tag in tags:
            try:
                current_tag = Tag.objects.get(name=tag)

            except:
                current_tag = Tag(name=tag)
                current_tag.save()
            self.save()
            current_tag.question.add(self)

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name="answers")
    title = models.CharField(max_length=64)
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
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=64)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name="tags", related_query_name="tag")

    def __str__(self):
        return self.title
