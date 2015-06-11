from django.shortcuts import render
from django.http import HttpResponse

from models import Verb, ChartWord, Tags, Adjective, SubjectPronoun, Noun, Possessive
from models import QuestionWord
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

def get_verb_objects(verb_root):
    verb_tabs = verb_root.tags.all()
    return list(Noun.objects.filter(tags__in=verb_tabs).distinct())

def get_object_verbs(obj):
    obj_tabs = obj.tags.all()
    return list(Verb.objects.filter(tags__in=obj_tabs).distinct())

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
    chart_type = get_chart_type(w_type)
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
        return set_subject_pronoun_from_prefix(sentence)
    #TODO: below cases
    elif changed_elt == 'verb':
        # call get_verb_objects on new verb, pass up list of new allowed objects
        return sentence
    elif changed_elt == 'obj':
        # call get_object_verbs on new object, pass up list of new allowed verbs
        # fix object prefix
        return sentence
    elif changed_elt == 'negation':
        if sentence['negation']==True:
            return negate_sentence(sentence)
        else:
            return un_negate_sentence(sentence)
    else:
        return sentence

def empty_sentence():
    return {"subject": None, "verb": None, "obj": None, "negation": False}

def empty_verb():
    return {'sp': '', 'tm': '', 'op': '', 'vr': None }

TENSES = ['present',
          'past',
          'past_perfect',
          'future']
TENSE_MARKERS = ['na', 'ta', 'li', 'me', 'ku', 'ja', 'ta']

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

    is_negative = random.randint(0,1)

    if is_negative:
        sentence["negative"] = True

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
    sps = [sb.subject_prefix for sb in all_subjects] + [sb.neg_prefix for sb in all_subjects]
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

def sentence_to_dictionary(sentence):
    dictionary = {}

    dictionary["verb"] = {}
    dictionary["verb"]["tm"] = sentence["verb"]["tm"]
    dictionary["verb"]["vr"] = sentence["verb"]["vr"].infinitive
    dictionary["verb"]["sp"] = sentence["verb"]["sp"]
    dictionary["verb"]["op"] = sentence["verb"]["op"]

    dictionary["obj"] = sentence["obj"].noun

    dictionary["subject"] = sentence["subject"].pronoun

    dictionary["negation"] = sentence["negation"]

    return dictionary

def dictionary_to_sentence(dictionary):
    sentence = {}

    sentence["verb"] = {}
    sentence["verb"]["tm"] = dictionary["verb"]["tm"]
    sentence["verb"]["vr"] = Verb.objects.get(infinitive=dictionary["verb"]["vr"])
    sentence["verb"]["sp"] = dictionary["verb"]["sp"]
    sentence["verb"]["op"] = dictionary["verb"]["op"]

    sentence["obj"] = Noun.objects.get(noun=dictionary["obj"])

    sentence["subject"] = SubjectPronoun.objects.get(pronoun=dictionary["subject"])
    
    sentence["negation"] = dictionary["negation"]

    return sentence

#
# VIEW FUNCTIONS
#
# this sends a random sentence to the frontend
def lesson_home(request):
    rand_sentence = gen_random_sentence()
    rand_sentence_dictionary = sentence_to_dictionary(rand_sentence)

    data = {'sentence': json.dumps(rand_sentence_dictionary)}
    data['sentence_text'] = sentence_to_text(rand_sentence)
    data['all_sentences'] = gen_all_sentences()
    #return HttpResponse(json.dumps(data), content_type='application/json')
    return render(request, "lessons/home.html", data)

def lesson_change(request):
    """
    when something dynamic happens, we need the sentence after the change, and the position marker that changed
    """
    changed_elt = json.loads(request.POST.get('changed'))
    sentence_dictionary = json.loads(request.POST.get('sentence'))

    #fills in the op, as it is currently blank
    sentence_dictionary['verb']['op'] = ''

    sentence = dictionary_to_sentence(sentence_dictionary)
   
    fixed_sentence = fix(sentence, changed_elt)

    fixed_sentence_dictionary = sentence_to_dictionary(fixed_sentence)

    data = {'sentence': fixed_sentence_dictionary}
    return HttpResponse(json.dumps(data), content_type='application/json')

def random_sentence(request):
    rand_sentence = gen_random_sentence()
    rand_sentence_dictionary = sentence_to_dictionary(rand_sentence)

    data = {'sentence': rand_sentence_dictionary}
    return HttpResponse(json.dumps(data), content_type='application/json')

#############################################################################################
"""
Noun phrases
"""

# noun phrases:
"""
noun before demonstrative
mtoto huyu
demonstrative before possessive
mtoto huyu wako
-ingini (other) after possessive
-ingi after possessive (doesn't matter relative to ingini)

noun_phrase dict =
{'noun': Noun object,
'adjs' = [Adjective objects],
'pos' = Possessive
'dem' = get_prefix('d', n_class)
'mod' = 'ingi/ingine'??
}
"""

def fix_adjp(adj_p, adj):
    #TODO: handle exceptions (like when the adjective starts with vowel, CHF PKT, etc
    return adj_p

def fix_noun_phrase(noun_phrase):
    """
    depending on input noun class, makes the
    """
    #TODO: support modifiers ingi/ingine
    noun_class = noun_phrase['noun'].noun_class
    # adjective prefixes
    adj_p = get_chart_prefix('ap', noun_class)
    noun_phrase['adjps'] = [fix_adjp(adj_p, adj) for adj in noun_phrase['adjs']]
    if noun_phrase.get('pos'):
        noun_phrase['posp'] = get_chart_prefix('p', noun_class)
    if noun_phrase.get('dem'):
        noun_phrase['dem'] = get_chart_prefix('d', noun_class)
    return noun_phrase

def random_noun_phrase():
    """
    generate a random noun phrase with one adjective and perhaps possesive and demonstrative
    """
    noun_phrase = {}
    # necessary choices
    random_noun = Noun.objects.order_by('?')[0]
    random_adj = Adjective.objects.order_by('?')[0]
    # optional choices
    random_pos = random.choice([Possessive.objects.order_by('?')[0], None])
    random_dem = random.choice([get_chart_prefix('d', random_noun.noun_class), None])
    noun_phrase['noun'] = random_noun
    noun_phrase['adjs'] = [random_adj]
    if random_pos:
        noun_phrase['pos'] = random_pos
    if random_dem:
        noun_phrase['dem'] = random_dem
    return fix_noun_phrase(noun_phrase)

def random_noun_phrase_text():
    noun_phrase = random_noun_phrase()
    sentence = ""
    sentence += noun_phrase['noun'].noun
    assert(len(noun_phrase['adjs']) == len(noun_phrase['adjps']))
    for adj_p, adj in zip(noun_phrase['adjps'], noun_phrase['adjs']):
        sentence += " " + adj_p + adj.stem
    if noun_phrase.get('dem'):
        sentence += " " + noun_phrase['dem']
    if noun_phrase.get('pos'):
        sentence += " " + noun_phrase['posp'] + noun_phrase['pos'].stem
    return sentence

############## VIEWS #####################################################



###########################################################################
"""
Question words, just tack on a question word to the sentence representation, who's default is None/empty
if the question word is active, the sentence becomes a question. Otherwise, it is declarative
"""
def gen_random_question():
    """
    generate a random valid sentence
    """
    q_word = QuestionWord.objects.order_by('?')[0]
    sentence = gen_random_sentence()
    sentence["qword"] =  q_word
    return sentence

def sentence_to_text(sentence):
    text = ""
    subj = sentence['subject']
    if isinstance(subj, Noun):
        text += sentence['subject'].noun
    elif isinstance(subj, SubjectPronoun):
        text += sentence['subject'].pronoun
    text += " " + sentence['verb']['sp']
    text += sentence['verb']['tm']
    text += sentence['verb']['op']
    text += sentence['verb']['vr'].infinitive
    text += " " + sentence['obj'].noun
    if sentence.get('qword'):
        text += " " + sentence['qword'].word
        text += "?"
    return text

def lesson_random_nphrase(request):
    rand_sentence = random_noun_phrase_text()
    rand_sentence = gen_random_question()
    rand_sentence = sentence_to_text(rand_sentence)
    return HttpResponse(rand_sentence)

def lesson_random_question(request):
    rand_sentence = random_noun_phrase_text()
    rand_sentence = gen_random_question()
    return HttpResponse(rand_sentence)


"""
reflexive, 'ji' goes in object prefix part, if it is changed to this remove the object.
"""


