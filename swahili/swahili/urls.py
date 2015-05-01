from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'swahili.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^demo/', 'lessons.views.lesson_home'),
    url(r'^lessonchange/', 'lessons.views.lesson_change'),
    url(r'^randomsentence/', 'lessons.views.random_sentence'),
    url(r'^lessonrandomnphrase', 'lessons.views.lesson_random_nphrase'),
    url(r'^lessonquestion', 'lessons.views.lesson_random_question'),
    url(r'^admin/', include(admin.site.urls)),
]
