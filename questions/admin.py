from django.contrib import admin

from questions.models import Profile, Question, Answer, Tag

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass