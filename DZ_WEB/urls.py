"""DZ_WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import questions.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', questions.views.index, name='index'),
    url(r'^ask/$', questions.views.ask, name='ask'),
    url(r'^login/$', questions.views.login, name='login'),
    url(r'^auth/$', questions.views.auth_user, name='auth'),
    url(r'^logout/$', questions.views.logout, name='logout'),
    url(r'^registration/$', questions.views.registration, name='registration'),
    url(r'^question/(?P<question_id>[0-9]+)$', questions.views.question, name='answer'),
    url(r'^question/like/(?P<question_id>[0-9]+)/(?P<id_>[0-9]*)$', questions.views.question_like,
        name='question_like'),
    url(r'^question/dislike/(?P<question_id>[0-9]+)/(?P<id_>[0-9]*)$',
        questions.views.question_dislike, name='question_dislike'),
    url(r'^save_question/$', questions.views.question_save, name='question_save'),
    url(r'^answer/(?P<ans_id>[0-9]+)/ans_like$', questions.views.answer_like, name='ans_like'),
    url(r'^answer/(?P<ans_id>[0-9]+)/ans_dislike$', questions.views.answer_dislike, name='ans_dislike'),
    url(r'^answer/(?P<ans_id>[0-9]+)/ans_mark$', questions.views.answer_mark, name='ans_mark'),
    url(r'^settings/$', questions.views.settings, name='settings'),
    url(r'^tag/(?P<tag_name>[a-z A-Z 0-9 . _ +]+)$', questions.views.tag, name='tag'),
    url(r'^hot/$', questions.views.hot, name='hot'),
    url(r'^search/$', questions.views.search, name='search'),
    url(r'^answer/(?P<q_id>[0-9]+)$', questions.views.answer, name='make_answer'),
    url(r'^make_new_user/$', questions.views.make_new_user, name='make_new_user'),
    url(r'^change/$', questions.views.change_profile, name='change_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
