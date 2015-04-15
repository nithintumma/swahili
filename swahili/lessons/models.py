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
            ('op', 'object_prefix'),
            ('na', 'neg_adjective')
            )
    word_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    nc1 = models.CharField(max_length=200)
    nc2 = models.CharField(max_length=200)
    nc3 = models.CharField(max_length=200)
    nc4 = models.CharField(max_length=200)
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
    neg_prefix = models.CharField(max_length=200, default='ha')
    def __unicode__(self):
        return self.pronoun

class Noun(models.Model):
    noun = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    noun_class = models.IntegerField()
    def __unicode__(self):
        return self.noun
