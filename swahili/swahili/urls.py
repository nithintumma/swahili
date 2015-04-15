from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'swahili.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^lesson/', 'lessons.views.lesson_home'),
    url(r'^lessonchange/', 'lessons.views.lesson_change'),
    url(r'^admin/', include(admin.site.urls)),
]
