from django.db import models
from jsonfield import JSONField

# Create your models here.

class Tags(models.Model):
    tag = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.tag

class Verb(models.Model):
    infinitive = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    exceptions = JSONField(blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    def __unicode__(self):
        return self.infinitive

class ChartWord(models.Model):
    TYPE_CHOICES = (
            ('p', 'possesive'),
            ('d', 'demonstrative'),
            ('sp', 'subject_prefix'),
            ('np', 'negative_prefix'),
            ('op', 'object_prefix'),
            ('ap', 'adjective_prefix')
            )
    word_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    nc1 = models.CharField(max_length=200, default='h')
    nc2 = models.CharField(max_length=200, default='h')
    nc3 = models.CharField(max_length=200, default='h')
    nc4 = models.CharField(max_length=200, default='h')
    nc5 = models.CharField(max_length=200, default='h')
    nc6 = models.CharField(max_length=200, default='h')
    nc7 = models.CharField(max_length=200, default='h')
    nc8 = models.CharField(max_length=200, default='h')
    nc9 = models.CharField(max_length=200, default='h')
    nc10 = models.CharField(max_length=200, default='h')
    nc11 = models.CharField(max_length=200, default='h')
    nc12 = models.CharField(max_length=200, default='h')
    nc13 = models.CharField(max_length=200, default='h')
    nc14 = models.CharField(max_length=200, default='h')
    nc15 = models.CharField(max_length=200, default='h')
    nc16 = models.CharField(max_length=200, default='h')
    nc17 = models.CharField(max_length=200, default='h')
    nc18 = models.CharField(max_length=200, default='h')

    def __unicode__(self):
        return self.word_type

class Adjective(models.Model):
    adjective = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    exceptions = JSONField(blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    def __unicode__(self):
        return self.adjective

class SubjectPronoun(models.Model):
    pronoun = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    subject_prefix = models.CharField(max_length=200)
    object_prefix = models.CharField(max_length=200, default='w')
    neg_prefix = models.CharField(max_length=200, default='ha')
    def __unicode__(self):
        return self.pronoun

class Noun(models.Model):
    noun = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    noun_class = models.IntegerField()
    def __unicode__(self):
        return self.noun

class QuestionWord(models.Model):
    word = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    # denotes wether the word should appear at the end of the question
    end = models.BooleanField(default=True)

