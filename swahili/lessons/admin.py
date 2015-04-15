from django.contrib import admin
from lessons.models import Tags, Verb, Noun, SubjectPronoun, ChartWord, Adjective
                          

# Register your models here
admin.site.register(Tags)
admin.site.register(Verb)
admin.site.register(Noun)
admin.site.register(SubjectPronoun)
admin.site.register(ChartWord)
admin.site.register(Adjective)
