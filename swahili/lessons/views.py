from django.shortcuts import render
from django.http import HttpResponse

from models import Verb, ChartWord, Tags, Adjective, SubjectPronoun, Noun
import random 
import json
import copy

# Create your views here.

"""
Dictionary format
verb_dict = 
{
'subject': subject_pronoun,
'verb': sp: subject_prefix/string
tm: tense_marker,
op: object_prefix
vr: verb_root,}
"""
# urls
def conjugate_verb(verb_dict, tense):
    """
    takes a tense
    returns a dictionary with correct verb root and tense marker
    """
    TENSE_MARKER = {
        'present': 'na',
        'past': 'li',
        'future': 'ta',
        'past_perfect': 'me',
    }
    tense_marker = TENSE_MARKER[tense]
    verb_dict['tm'] = tense_marker
    return verb_dict          

# sentence form 
#{'subject': subject_pronoun, 'verb': verb_dict, 'obj': noun}
#
# How do we encode rules?
# set_verb_prefix(based on subject, set subject prefix in verb)

# fix a subject given sprefix
# fix a sprefix given a subject 
# generate a random correct sentence (what is a sentence)
# randomly choose this part

def get_chart_type(w_type):
    """
    returns the ChartWord object of the correct type
    e.g. w_type = 'possesive', ''
    """
    return ChartWord.objects.get(word_type=w_type)

def get_chart_prefix(w_type, n_class):
    """
    helper function to get the chart prefix for a word type and a noun class
    e.g., w_type = 'sp' (subject_prefix), n_class = 4 -> 'i'
    """
    chart_type = get_chart_word(w_type)
    prefix = getattr(chart_type, 'nc' + str(n_class))
    return prefix 

def set_subject_pronoun_from_prefix(sentence):
    """
    Assumes that the sp corresponds to a pronoun  
    """
    #TODO: allow arbitrary subject prefix, populate with a random noun from that class
    sp = sentence['verb']['sp'] 
    subject = SubjectPronoun.objects.filter(subject_prefix=sp)[0]
    sentence['subject'] = subject
    return sentence

def set_subject_prefix(sentence):
    """
    sets the correct subject prefix given the subject of the input sentence 
    subject is either a subject_prefix object or a noun 
    """
    subject = sentence['subject']
    if isinstance(subject, SubjectPronoun): 
        sp = subject.subject_prefix
    elif isinstance(subject, Noun):
        sp = get_chart_prefix('sp', subject.noun_class)
    else:
        raise Exception("Not supported subject type (pronoun, noun)")
    sentence['verb']['sp'] = sp
    return sentence 

def set_object_prefix(sentence):
    """
    @input 
    assume sentence has object
    want to update object prefix of the verb
    Allows object to be a noun or a pronoun (mimi, wewe, etc.)
    """
    obj = sentence['obj']
    if isinstance(obj, SubjectPronoun):
        op = obj.object_prefix
    elif isinstance(obj, Noun):
        op = get_chart_prefix('op', obj,noun_class)
    else:
        raise Exception("Not supported object type (pronoun, noun)")

    sentence['verb']['op'] = op
    return sentence

# if you change subject, we need to change the subject prefix accordingly 
# {'subject_pronoun': {}} 
# fix that cases on what was changed, and calls the right function to fix it 
def fix(sentence, changed_elt):
    if changed_elt == 'subject':
        return set_subject_prefix(sentence)
    elif changed_elt == 'sp':
        return set_subject_from_prefix(sentence)
    #TODO: below cases
    elif changed_elt == 'verb':
        return None
    elif changed_elt == 'obj':
        return None
    
def empty_sentence():
    return {"subject": None, "verb": None, "obj": None}

def empty_verb():
    return {'sp': '', 'tm': '', 'op': '', 'vr': None }

TENSES = ['present',
          'past',
          'past_perfect',
          'future']
TENSE_MARKERS = ['na', 'ta', 'li', 'me']

def random_tense():
    return random.choice(TENSES)

def gen_random_sentence():
    """
    creates a random valid simple sentence 
    """
    sentence = empty_sentence()

    # get random subject
    subject = SubjectPronoun.objects.order_by('?')[0] 
    sentence['subject'] = subject 

    # get random verb
    verb = Verb.objects.order_by('?')[0] 
    verb_dict = empty_verb()
    verb_dict['vr'] = verb
    # get random tense
    tense = random_tense()
    verb_dict = conjugate_verb(verb_dict, tense)
    sentence['verb'] = verb_dict

    # make resulting sentence grammatical
    sentence = fix(sentence, 'subject')
    
    #TODO: add logic to deal with noun/verb tags
    # 1. get all objects that are allowable for this verb
    # objects = Noun.objects.filter(tags_in=verb.tags).distinct()
    obj = Noun.objects.order_by('?')[0]
    sentence['obj'] = obj
    return sentence

def gen_all_sentences():
    """
    want to return to the frontend a list of all of the choices 
    """
    all_subjects = list(SubjectPronoun.objects.all())
    sps = [sb.subject_prefix for sb in all_subjects]
    subjects = [sb.pronoun for sb in all_subjects]
    verbs = [verb.infinitive for verb in Verb.objects.all()]
    nouns = [n.noun for n in list(Noun.objects.all())]
    all_sentences = {'subjects': subjects, 
                        'verbs':{
                            'sps': sps,
                            'tms': TENSE_MARKERS, 
                            'ops': [],
                            'vrs': verbs},
                     'objs': nouns}
    return all_sentences

NEG_TENSE_MARKER = {'na': '', 'me': 'ja', 'li': 'ku', 'ta': 'ta'}
REV_NEG_TENSE_MARKER = {v: k for k, v in NEG_TENSE_MARKER.items()}

def un_negate_sentence(sentence):
    """
    input: negated sentence
    output: positive version of sentence
    """
    pos_sentence = copy.copy(sentence)
    pos_sentence['neg'] = False
    subject = sentence['subject']
    verb_dict = sentence['verb']
    # present tense, revert to standard verb root 
    if verb_dict['tm'] == '':
        pos_sentence['verb']['vr'].infinitive = verb_dict['vr'].infinitive[:-1] + 'a'

    # set the right tense marker 
    pos_sentence['verb']['tm'] = REV_NEG_TENSE_MARKER[verb_dict['tm']] 
    # set the right subject prefix given the subject
    pos_sentence = fix(pos_sentence, 'subject')
    return pos_sentence

def negate_sentence(sentence):
    """
    negation rules
    """
    if sentence.get('neg'):
        return un_negate_sentence(sentence) 
        
    neg_sentence = copy.copy(sentence) 
    subject = sentence['subject']
    verb_dict = sentence['verb']
    #neg_sentence['verb'] = verb_dict
    neg_sentence['verb']['sp'] = subject.neg_prefix
       
    # present tense modify verb root
    if verb_dict['tm'] == 'na':
        neg_sentence['verb']['vr'].infinitive = verb_dict['vr'].infinitive[:-1] + 'i'
        
    neg_sentence['verb']['tm'] = NEG_TENSE_MARKER[verb_dict['tm']]
    neg_sentence['neg'] = True
    return neg_sentence

def sentence_to_text(sentence):
    """
    input is sentence dictionary and output is dictionary for front end 
    """
    text = {}
    text['subject'] = sentence['subject'].pronoun
    text['verb'] = sentence['verb']
    text['verb']['vr'] = text['verb']['vr'].infinitive
    text['obj'] = sentence['obj'].noun
    if sentence.get('neg'):
        text['neg'] = True
    else:
        text['neg'] = False
    return text

#
# VIEW FUNCTIONS
#
def lesson_home(request):
    rand_sentence = gen_random_sentence()
    rand_sentence = rand_sentence
    data = {'sentence': sentence_to_text(rand_sentence)}
    data['all_data'] = gen_all_sentences()
    return HttpResponse(json.dumps(data), content_type='application/json')

def lesson_change(request):
    """
    when something dynamic happens, we need the sentence after the change, and the position marker that changed 
    """
    changed_elt = json.loads(request.POST.get('changed'))
    sentence = json.loads(request.POST.get('sentence'))
    fixed_sentence = sentence_to_text(fix(sentence, changed_marker))
    data = {'sentence': fixed_sentence}
    return HttpResponse(json.dumps(data), content_type='application/json')


#############################################################################################
"""
Past simple sentences, we want to allow the reflexive, question words
"""

# noun phrases:
"""
{'noun': Noun object,
'adjs' = [Adjective objects],
'possesive' = 
'demonstrative' = 
}
"""
